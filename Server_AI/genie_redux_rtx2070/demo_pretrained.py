#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Demo with Pretrained Model
Demonstrates the world model concept with a trained or pretrained checkpoint.
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


def load_model(checkpoint_path: str, device: str = "cuda"):
    """Load TinyWorldModel from checkpoint."""
    try:
        from model import TinyWorldModel
        
        model = TinyWorldModel(action_dim=5, hidden_dim=64).to(device)
        
        if Path(checkpoint_path).exists():
            state_dict = torch.load(checkpoint_path, map_location=device)
            model.load_state_dict(state_dict)
            print(f"[GenieRedux] ✓ Loaded checkpoint: {checkpoint_path}")
        else:
            print(f"[GenieRedux] ⚠ Checkpoint not found: {checkpoint_path}")
            print(f"[GenieRedux] Using untrained model (random weights)")
        
        model.eval()
        return model
    except Exception as e:
        print(f"[GenieRedux] Failed to load model: {e}")
        return None


def demo_with_model(checkpoint_path: str, num_frames: int = 300, fps: int = 25):
    """Run demo with trained model."""
    if not TORCH_AVAILABLE:
        print("[GenieRedux] PyTorch not available, falling back to simulation...")
        return demo_simulation(num_frames, fps)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GenieRedux] Device: {device}")
    
    model = load_model(checkpoint_path, device)
    if model is None:
        return demo_simulation(num_frames, fps)
    
    # Initialize state
    ball_x, ball_y = 0.5, 0.5
    frame_np = create_frame(ball_x=ball_x, ball_y=ball_y)
    current_frame = torch.from_numpy(frame_np).permute(2, 0, 1).float() / 255.0
    current_frame = current_frame.unsqueeze(0).to(device)
    
    print("[GenieRedux] ╔════════════════════════════════════════════╗")
    print("[GenieRedux] ║  GenieRedux - World Model Demonstration    ║")
    print("[GenieRedux] ╚════════════════════════════════════════════╝")
    print()
    print("[GenieRedux] Generating frames with trained world model...")
    print(f"[GenieRedux] Target: {num_frames} frames @ {fps} FPS")
    print(f"[GenieRedux] Estimated duration: {num_frames / fps:.1f} seconds")
    print()
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while frame_count < num_frames:
            # Random action
            action = np.random.randint(0, 5)
            action_name = ["noop", "left", "right", "up", "down"][action]
            
            # Apply action to ground truth for visualization
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
            
            # Progress output
            if frame_count % 50 == 0 or frame_count == 1:
                elapsed = time.time() - start_time
                fps_actual = frame_count / elapsed if elapsed > 0 else 0
                print(f"[GenieRedux] Frame {frame_count:3d}/{num_frames} | "
                      f"Action: {action_name:6s} | "
                      f"Ball: ({ball_x:.2f}, {ball_y:.2f}) | "
                      f"FPS: {fps_actual:.1f}")
            
            # Frame timing
            time.sleep(1.0 / fps)
        
        elapsed = time.time() - start_time
        print()
        print("[GenieRedux] ✓ Demo complete!")
        print(f"[GenieRedux] Generated {frame_count} frames in {elapsed:.1f}s ({frame_count/elapsed:.1f} FPS)")
        
    except KeyboardInterrupt:
        print(f"\n[GenieRedux] Demo stopped after {frame_count} frames.")


def demo_simulation(num_frames: int = 300, fps: int = 25):
    """Run demo with physics simulation (no GPU)."""
    print("[GenieRedux] ╔════════════════════════════════════════════╗")
    print("[GenieRedux] ║  GenieRedux - Physics Simulation Demo      ║")
    print("[GenieRedux] ║  (No GPU required)                         ║")
    print("[GenieRedux] ╚════════════════════════════════════════════╝")
    print()
    print("[GenieRedux] Running physics simulation...")
    print(f"[GenieRedux] Target: {num_frames} frames @ {fps} FPS")
    print(f"[GenieRedux] Estimated duration: {num_frames / fps:.1f} seconds")
    print()
    
    ball_x, ball_y = 0.5, 0.5
    speed = 0.04
    frame_count = 0
    start_time = time.time()
    
    try:
        while frame_count < num_frames:
            # Random action
            action = np.random.randint(0, 5)
            action_name = ["noop", "left", "right", "up", "down"][action]
            
            dx, dy = ACTIONS[action]
            ball_x = max(0.05, min(0.95, ball_x + dx * speed + np.random.uniform(-0.01, 0.01)))
            ball_y = max(0.05, min(0.95, ball_y + dy * speed + np.random.uniform(-0.01, 0.01)))
            
            frame_count += 1
            
            # Progress output
            if frame_count % 50 == 0 or frame_count == 1:
                elapsed = time.time() - start_time
                fps_actual = frame_count / elapsed if elapsed > 0 else 0
                print(f"[GenieRedux] Frame {frame_count:3d}/{num_frames} | "
                      f"Action: {action_name:6s} | "
                      f"Ball: ({ball_x:.2f}, {ball_y:.2f}) | "
                      f"FPS: {fps_actual:.1f}")
            
            # Frame timing
            time.sleep(1.0 / fps)
        
        elapsed = time.time() - start_time
        print()
        print("[GenieRedux] ✓ Demo complete!")
        print(f"[GenieRedux] Simulated {frame_count} frames in {elapsed:.1f}s ({frame_count/elapsed:.1f} FPS)")
        
    except KeyboardInterrupt:
        print(f"\n[GenieRedux] Demo stopped after {frame_count} frames.")


def main():
    parser = argparse.ArgumentParser(description="GenieRedux Demo with Pretrained Model")
    parser.add_argument("--checkpoint", type=str, 
                       default=r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\checkpoints\best_model.pt",
                       help="Path to model checkpoint")
    parser.add_argument("--frames", type=int, default=300,
                       help="Number of frames to generate")
    parser.add_argument("--fps", type=int, default=25,
                       help="Target FPS")
    parser.add_argument("--mode", type=str, choices=["auto", "pytorch", "simulation"], 
                       default="auto",
                       help="Demo mode")
    args = parser.parse_args()
    
    print()
    
    if args.mode == "auto":
        if TORCH_AVAILABLE and torch.cuda.is_available():
            print("[GenieRedux] PyTorch + CUDA detected, using GPU mode...")
            demo_with_model(args.checkpoint, args.frames, args.fps)
        elif TORCH_AVAILABLE:
            print("[GenieRedux] PyTorch available but no CUDA, using CPU mode...")
            demo_with_model(args.checkpoint, args.frames, args.fps)
        else:
            print("[GenieRedux] PyTorch not available, using simulation mode...")
            demo_simulation(args.frames, args.fps)
    elif args.mode == "pytorch":
        demo_with_model(args.checkpoint, args.frames, args.fps)
    else:
        demo_simulation(args.frames, args.fps)
    
    print()


if __name__ == "__main__":
    main()
