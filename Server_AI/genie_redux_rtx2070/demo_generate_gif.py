#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Generate Demo GIF (no PyTorch, no OpenCV GUI)
Creates a short animated GIF showing the world model concept.
"""

import random
import numpy as np
from pathlib import Path
from PIL import Image

from dataset import create_frame, ACTIONS


def generate_demo_gif(output_path: str, num_frames: int = 120, fps: int = 25):
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    ball_x, ball_y = 0.5, 0.5
    speed = 0.04
    frames = []

    # Random action sequence
    for _ in range(num_frames):
        action_id = random.choice(list(ACTIONS.keys()))
        dx, dy = ACTIONS[action_id]
        ball_x = max(0.05, min(0.95, ball_x + dx * speed + random.uniform(-0.01, 0.01)))
        ball_y = max(0.05, min(0.95, ball_y + dy * speed + random.uniform(-0.01, 0.01)))

        img_np = create_frame(ball_x=ball_x, ball_y=ball_y)
        img = Image.fromarray(img_np)
        img = img.resize((256, 256), Image.NEAREST)
        frames.append(img)

    duration = int(1000 / fps)
    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=0
    )
    print(f"[GenieRedux] Demo GIF saved to: {out}")


if __name__ == "__main__":
    generate_demo_gif(r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\output\demo.gif")
