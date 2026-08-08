#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Synthetic Interactive Dataset
Generates (frame, action, next_frame) triplets where a colored ball moves
according to keyboard-style actions.
"""

import os
import random
import numpy as np
from PIL import Image
from pathlib import Path

try:
    import torch
    from torch.utils.data import Dataset
except Exception:
    torch = None
    Dataset = object


ACTIONS = {
    0: (0, 0),    # noop
    1: (-1, 0),   # left
    2: (1, 0),    # right
    3: (0, -1),   # up
    4: (0, 1),    # down
}


def create_frame(width: int = 64, height: int = 64, ball_x: float = 0.5, ball_y: float = 0.5,
                 ball_radius: int = 5, bg_color: tuple = (30, 30, 40),
                 ball_color: tuple = (200, 80, 60)) -> np.ndarray:
    """Render a single 64x64 RGB frame with a ball."""
    img = np.full((height, width, 3), bg_color, dtype=np.uint8)
    x = int(ball_x * width)
    y = int(ball_y * height)

    yy, xx = np.ogrid[:height, :width]
    mask = (xx - x) ** 2 + (yy - y) ** 2 <= ball_radius ** 2
    img[mask] = ball_color
    return img


def generate_synthetic_trajectory(num_frames: int = 100, width: int = 64, height: int = 64,
                                  ball_radius: int = 5, max_speed: float = 0.08) -> tuple:
    """Generate a trajectory with random actions."""
    x = random.uniform(0.2, 0.8)
    y = random.uniform(0.2, 0.8)

    frames = []
    actions = []

    for _ in range(num_frames):
        action = random.choice(list(ACTIONS.keys()))
        dx, dy = ACTIONS[action]
        x = max(0.05, min(0.95, x + dx * max_speed + random.uniform(-0.01, 0.01)))
        y = max(0.05, min(0.95, y + dy * max_speed + random.uniform(-0.01, 0.01)))

        frame = create_frame(width, height, x, y, ball_radius)
        frames.append(frame)
        actions.append(action)

    return frames, actions


def generate_dataset(output_dir: str, n_trajectories: int = 500, frames_per_traj: int = 100):
    """Generate and save synthetic dataset as .npy files."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    all_frames = []
    all_actions = []

    print(f"[GenieRedux] Generating {n_trajectories} trajectories...")
    for i in range(n_trajectories):
        frames, actions = generate_synthetic_trajectory(frames_per_traj)
        all_frames.extend(frames)
        all_actions.extend(actions)

    all_frames = np.array(all_frames, dtype=np.uint8)  # (N, 64, 64, 3)
    all_actions = np.array(all_actions, dtype=np.int64)

    np.save(out / "frames.npy", all_frames)
    np.save(out / "actions.npy", all_actions)
    print(f"[GenieRedux] Saved {len(all_frames)} frames to {output_dir}")


class SyntheticWorldDataset(Dataset):
    """PyTorch dataset for synthetic world model."""

    def __init__(self, data_dir: str, split: str = "train", train_ratio: float = 0.9):
        data_dir = Path(data_dir)
        frames = np.load(data_dir / "frames.npy")  # (N, 64, 64, 3)
        actions = np.load(data_dir / "actions.npy")  # (N,)

        N = len(frames)
        split_idx = int(N * train_ratio)

        if split == "train":
            frames = frames[:split_idx]
            actions = actions[:split_idx]
        else:
            frames = frames[split_idx:-1]
            actions = actions[split_idx:-1]

        # Build (frame_t, action_t, frame_t+1) pairs
        self.frames = frames[:-1]
        self.next_frames = frames[1:]
        self.actions = actions[:-1]

    def __len__(self):
        return len(self.frames)

    def __getitem__(self, idx):
        frame = torch.from_numpy(self.frames[idx]).permute(2, 0, 1).float() / 255.0
        next_frame = torch.from_numpy(self.next_frames[idx]).permute(2, 0, 1).float() / 255.0
        action = torch.zeros(5)
        action[self.actions[idx]] = 1.0
        return frame, action, next_frame


if __name__ == "__main__":
    generate_dataset(r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\data")
