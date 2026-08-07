# Agent Mesh Communication Protocol (AMCP) & RTX 2070 VRAM Governor
# Manages asynchronous pub/sub event mesh between Godot 4 and AI agents.

import asyncio
import time
import traceback
from typing import Dict, Any, Callable, List

# Try to import pynvml for real GPU memory monitoring
try:
    import pynvml
    pynvml.nvmlInit()
    PYNVML_AVAILABLE = True
    print("[VRAMGovernor] pynvml initialized - real GPU monitoring enabled.")
except (ImportError, Exception):
    PYNVML_AVAILABLE = False
    print("[VRAMGovernor] WARNING: pynvml not available. Using estimated VRAM tracking only.")


class VRAMGovernor:
    """Monitors and caps GPU VRAM usage to strictly under a configurable limit.
    
    Uses pynvml for real VRAM readings when available, falls back to
    estimated self-reported allocations otherwise.
    """
    def __init__(self, max_vram_gb: float = 7.5, gpu_index: int = 0):
        self.max_vram_gb = max_vram_gb
        self.gpu_index = gpu_index
        self.active_models: Dict[str, float] = {}  # model_name -> estimated_vram_gb
        self._handle = None

        if PYNVML_AVAILABLE:
            try:
                self._handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_index)
                info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)
                total_gb = info.total / (1024 ** 3)
                print(f"[VRAMGovernor] GPU #{gpu_index}: {total_gb:.1f} GB total. Cap set to {max_vram_gb} GB.")
            except Exception as e:
                print(f"[VRAMGovernor] Could not get GPU handle: {e}")
                self._handle = None

    def get_real_vram_used_gb(self) -> float:
        """Query actual GPU memory usage via pynvml. Returns -1 if unavailable."""
        if self._handle is None:
            return -1.0
        try:
            info = pynvml.nvmlDeviceGetMemoryInfo(self._handle)
            return info.used / (1024 ** 3)
        except Exception:
            return -1.0

    def get_estimated_vram_used_gb(self) -> float:
        """Sum of self-reported allocations."""
        return sum(self.active_models.values())

    def get_effective_vram_used_gb(self) -> float:
        """Use real VRAM if available, otherwise estimated."""
        real = self.get_real_vram_used_gb()
        return real if real >= 0 else self.get_estimated_vram_used_gb()

    def request_allocation(self, model_name: str, estimated_vram_gb: float) -> bool:
        current_used = self.get_effective_vram_used_gb()
        if current_used + estimated_vram_gb <= self.max_vram_gb:
            self.active_models[model_name] = estimated_vram_gb
            new_total = self.get_effective_vram_used_gb()
            print(f"[VRAMGovernor] Allocated {estimated_vram_gb:.1f}GB for {model_name}. "
                  f"VRAM: {new_total:.2f}GB / {self.max_vram_gb}GB")
            return True
        else:
            print(f"[VRAMGovernor] BLOCKED: Cannot allocate {estimated_vram_gb:.1f}GB for {model_name}. "
                  f"VRAM limit reached ({current_used:.2f}GB / {self.max_vram_gb}GB).")
            return False

    def release_allocation(self, model_name: str):
        if model_name in self.active_models:
            freed = self.active_models.pop(model_name)
            print(f"[VRAMGovernor] Released {freed:.1f}GB from {model_name}. "
                  f"Remaining: {self.get_effective_vram_used_gb():.2f}GB")

    def status(self) -> dict:
        """Return current VRAM status for monitoring."""
        return {
            "max_vram_gb": self.max_vram_gb,
            "real_vram_used_gb": round(self.get_real_vram_used_gb(), 2),
            "estimated_vram_used_gb": round(self.get_estimated_vram_used_gb(), 2),
            "active_models": dict(self.active_models),
            "pynvml_available": PYNVML_AVAILABLE,
        }


class AgentMeshBroker:
    """Asynchronous Event Broker routing messages across AI agents and Godot 4 simulation.
    
    Includes proper error handling for subscriber callbacks to prevent
    silent failures in production.
    """
    def __init__(self):
        self.vram_governor = VRAMGovernor()
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()
        self.failed_events: List[dict] = []  # Dead-letter queue

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
        print(f"[AgentMeshBroker] Subscribed handler to event '{event_type}'")

    async def publish(self, event_type: str, payload: Dict[str, Any]):
        event = {"event_type": event_type, "timestamp": time.time(), "payload": payload}
        await self.event_queue.put(event)

        if event_type in self.subscribers:
            for handler in self.subscribers[event_type]:
                # Wrap each handler in error-safe task
                asyncio.create_task(self._safe_dispatch(handler, event_type, payload))

    async def _safe_dispatch(self, handler: Callable, event_type: str, payload: Dict[str, Any]):
        """Execute a handler with proper error catching and dead-letter logging."""
        try:
            await handler(payload)
        except Exception as e:
            error_entry = {
                "event_type": event_type,
                "payload": payload,
                "error": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": time.time(),
            }
            self.failed_events.append(error_entry)
            print(f"[AgentMeshBroker] ERROR in handler for '{event_type}': {e}")
            # Keep dead-letter queue bounded
            if len(self.failed_events) > 100:
                self.failed_events = self.failed_events[-50:]


# Global Broker Singleton
mesh_broker = AgentMeshBroker()
