#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Interactive Demo with Pretrained Model
Loads a pretrained world model and runs an interactive loop.
Falls back to synthetic simulation if GPU is unavailable.
"""

import os
import sys
import time
import argparse
import numpy as np
from pathlib import Path

try:
    import torch
    TORCH_AVAILABLE = True
except Exception as e:
    print(f"[GenieRedux] PyTorch not available: {e}")
    TORCH_AVAILABLE = False

from dataset import create_frame, ACTIONS


def run_interactive_demo_pytorch(checkpoint_path: str):
    """Run demo with PyTorch model."""
    if not TORCH_AVAILABLE:
        print("[GenieRedux] PyTorch not available, falling back to simulation...")
        return run_interactive_demo_simulation()

    try:
        import torch
        from model import TinyWorldModel
    except Exception as e:
        print(f"[GenieRedux] Failed to import model: {e}")
        return run_interactive_demo_simulation()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GenieRedux] Running on device: {device}")

    # Load model
    model = TinyWorldModel(action_dim=5, hidden_dim=64).to(device)
    
    if Path(checkpoint_path).exists():
        try:
            model.load_state_dict(torch.load(checkpoint_path, map_location=device))
            print(f"[GenieRedux] Loaded checkpoint: {checkpoint_path}")
        except Exception as e:
            print(f"[GenieRedux] Failed to load checkpoint: {e}")
            print("[GenieRedux] Using untrained model...")
    else:
        print(f"[GenieRedux] Checkpoint not found: {checkpoint_path}")
        print("[GenieRedux] Using untrained model...")

    model.eval()

    # Initial state
    ball_x, ball_y = 0.5, 0.5
    frame_np = create_frame(ball_x=ball_x, ball_y=ball_y)
    current_frame = torch.from_numpy(frame_np).permute(2, 0, 1).float() / 255.0
    current_frame = current_frame.unsqueeze(0).to(device)

    print("[GenieRedux] Interactive demo started!")
    print("[GenieRedux] Commands:")
    print("  - Press 'a' or LEFT for left")
    print("  - Press 'd' or RIGHT for right")
    print("  - Press 'w' or UP for up")
    print("  - Press 's' or DOWN for down")
    print("  - Press 'r' to reset")
    print("  - Press 'q' or ESC to quit")
    print("[GenieRedux] Generating frames... (press Ctrl+C to stop)")

    try:
        frame_count = 0
        while True:
            # Simulate action (random for demo)
            action = np.random.randint(0, 5)
            
            # Apply action to ground truth
            speed = 0.06
            dx, dy = ACTIONS[action]
            ball_x = max(0.05, min(0.95, ball_x + dx * speed + np.random.uniform(-0.01, 0.01)))
            ball_y = max(0.05, min(0.95, ball_y + dy * speed + np.random.uniform(-0.01, 0.01)))

            # Model predicts next frame
            with torch.no_grad():
                a = torch.zeros(1, 5).to(device)
                a[0, action] = 1.0
                pred = model(current_frame, a)
                current_frame = pred.clamp(0, 1)

            frame_count += 1
            if frame_count % 10 == 0:
                print(f"[GenieRedux] Generated {frame_count} frames | Ball: ({ball_x:.2f}, {ball_y:.2f})")

            time.sleep(0.02)

    except KeyboardInterrupt:
        print(f"\n[GenieRedux] Demo stopped after {frame_count} frames.")


def run_interactive_demo_simulation():
    """Run demo with physics simulation (no GPU needed)."""
    print("[GenieRedux] Running simulation mode (no GPU required)...")
    print("[GenieRedux] Commands: WASD or Arrows. Q or ESC to quit.")

    ball_x, ball_y = 0.5, 0.5
    speed = 0.04
    frame_count = 0

    try:
        while True:
            # Random action
            action = np.random.randint(0, 5)
            dx, dy = ACTIONS[action]
            ball_x = max(0.05, min(0.95, ball_x + dx * speed + np.random.uniform(-0.01, 0.01)))
            ball_y = max(0.05, min(0.95, ball_y + dy * speed + np.random.uniform(-0.01, 0.01)))

            frame_count += 1
            if frame_count % 25 == 0:
                print(f"[GenieRedux] Frame {frame_count} | Ball: ({ball_x:.2f}, {ball_y:.2f})")

            time.sleep(0.01)

    except KeyboardInterrupt:
        print(f"\n[GenieRedux] Demo stopped after {frame_count} frames.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, 
                       default=r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\checkpoints\best_model.pt")
    parser.add_argument("--mode", type=str, choices=["pytorch", "simulation", "auto"], default="auto",
                       help="'pytorch' for GPU, 'simulation' for CPU, 'auto' to detect")
    args = parser.parse_args()

    if args.mode == "auto":
        if TORCH_AVAILABLE:
            print("[GenieRedux] PyTorch available, using GPU mode...")
            run_interactive_demo_pytorch(args.checkpoint)
        else:
            print("[GenieRedux] PyTorch not available, using simulation mode...")
            run_interactive_demo_simulation()
    elif args.mode == "pytorch":
        run_interactive_demo_pytorch(args.checkpoint)
    else:
        run_interactive_demo_simulation()


if __name__ == "__main__":
    main()
