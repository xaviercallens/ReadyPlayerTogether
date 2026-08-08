#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Interactive Demo
Control a generated ball with keyboard (arrow keys) and see the world model
predict the next frame in real-time.
"""

import os
import time
import argparse
import numpy as np
import torch
import cv2
from pathlib import Path

from model import TinyWorldModel
from dataset import create_frame


ACTION_KEYS = {
    0: None,
    81: 1,   # Qt left arrow -> left
    83: 2,   # Qt right arrow -> right
    82: 3,   # Qt up arrow -> up
    84: 4,   # Qt down arrow -> down
}

# OpenCV key codes
CV_KEYS = {
    ord('a'): 1,
    ord('d'): 2,
    ord('w'): 3,
    ord('s'): 4,
    81: 1,  # left arrow
    83: 2,  # right arrow
    82: 3,  # up arrow
    84: 4,  # down arrow
    27: -1, # ESC to quit
}


def action_onehot(action: int) -> torch.Tensor:
    a = torch.zeros(5)
    if 0 <= action < 5:
        a[action] = 1.0
    return a


def frame_to_image(tensor: torch.Tensor) -> np.ndarray:
    """Convert (3, 64, 64) tensor to (64, 64, 3) BGR uint8."""
    img = tensor.detach().cpu().permute(1, 2, 0).numpy()
    img = np.clip(img * 255, 0, 255).astype(np.uint8)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img


def run_demo(checkpoint_path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GenieRedux Demo] Running on {device}")

    model = TinyWorldModel(action_dim=5, hidden_dim=64).to(device)

    if Path(checkpoint_path).exists():
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
        print(f"[GenieRedux Demo] Loaded checkpoint from {checkpoint_path}")
    else:
        print(f"[GenieRedux Demo] No checkpoint found at {checkpoint_path}, using random model")

    model.eval()

    # Initial state
    ball_x, ball_y = 0.5, 0.5
    frame_np = create_frame(ball_x=ball_x, ball_y=ball_y)
    current_frame = torch.from_numpy(frame_np).permute(2, 0, 1).float() / 255.0
    current_frame = current_frame.unsqueeze(0).to(device)

    print("[GenieRedux Demo] Controls: WASD or Arrow keys. ESC to quit.")

    while True:
        # Render current frame
        img = frame_to_image(current_frame[0])
        img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("GenieRedux RTX2070 - World Model Demo", img)

        # Poll key
        key = cv2.waitKey(100) & 0xFF
        action = 0
        if key in CV_KEYS:
            val = CV_KEYS[key]
            if val == -1:
                break
            action = val

        # Apply action to current state (ground truth simulator)
        speed = 0.06
        dx, dy = {0: (0, 0), 1: (-1, 0), 2: (1, 0), 3: (0, -1), 4: (0, 1)}[action]
        ball_x = max(0.05, min(0.95, ball_x + dx * speed))
        ball_y = max(0.05, min(0.95, ball_y + dy * speed))

        # World model predicts next frame
        with torch.no_grad():
            a = action_onehot(action).unsqueeze(0).to(device)
            pred = model(current_frame, a)
            current_frame = pred.clamp(0, 1)

        time.sleep(0.02)

    cv2.destroyAllWindows()
    print("[GenieRedux Demo] Exited.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, default=r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\checkpoints\best_model.pt")
    args = parser.parse_args()
    run_demo(args.checkpoint)
