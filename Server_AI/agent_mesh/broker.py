# Agent Mesh Communication Protocol (AMCP) & RTX 2070 VRAM Governor
# Manages asynchronous pub/sub event mesh between Godot 4 and AI agents (Ollama, ComfyUI, RVC, RL).

import asyncio
import json
import time
from typing import Dict, Any, Callable, List

class VRAMGovernor:
    """Monitors and caps GPU VRAM usage to strictly under 7.5 GB for RTX 2070."""
    def __init__(self, max_vram_gb: float = 7.5):
        self.max_vram_gb = max_vram_gb
        self.active_models: Dict[str, float] = {} # model_name -> estimated_vram_gb

    def request_allocation(self, model_name: str, estimated_vram_gb: float) -> bool:
        current_used = sum(self.active_models.values())
        if current_used + estimated_vram_gb <= self.max_vram_gb:
            self.active_models[model_name] = estimated_vram_gb
            print(f"[VRAMGovernor] Allocated {estimated_vram_gb}GB for {model_name}. Total VRAM: {current_used + estimated_vram_gb:.2f}GB / {self.max_vram_gb}GB")
            return True
        else:
            print(f"[VRAMGovernor] WARNING: Cannot allocate {estimated_vram_gb}GB for {model_name}. VRAM limit reached ({current_used:.2f}GB used).")
            return False

    def release_allocation(self, model_name: str):
        if model_name in self.active_models:
            freed = self.active_models.pop(model_name)
            print(f"[VRAMGovernor] Released {freed}GB from {model_name}.")

class AgentMeshBroker:
    """Asynchronous Event Broker routing messages across AI agents and Godot 4 simulation."""
    def __init__(self):
        self.vram_governor = VRAMGovernor()
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue: asyncio.Queue = asyncio.Queue()

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
                asyncio.create_task(handler(payload))

# Global Broker Singleton
mesh_broker = AgentMeshBroker()
