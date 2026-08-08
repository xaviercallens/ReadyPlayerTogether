#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Interactive Demo (No PyTorch fallback)
Runs a simple physics simulator if PyTorch is not available or broken.
Use this to validate the interactive loop while the GPU stack is being repaired.
"""

import time
import numpy as np
import cv2


CV_KEYS = {
    ord('a'): (-1, 0),
    ord('d'): (1, 0),
    ord('w'): (0, -1),
    ord('s'): (0, 1),
    81: (-1, 0),  # left arrow
    83: (1, 0),   # right arrow
    82: (0, -1),  # up arrow
    84: (0, 1),   # down arrow
    27: None,     # ESC to quit
}


def create_frame(ball_x: float, ball_y: float, width: int = 64, height: int = 64,
                 ball_radius: int = 5, bg_color: tuple = (30, 30, 40),
                 ball_color: tuple = (200, 80, 60)) -> np.ndarray:
    img = np.full((height, width, 3), bg_color, dtype=np.uint8)
    x = int(ball_x * width)
    y = int(ball_y * height)
    yy, xx = np.ogrid[:height, :width]
    mask = (xx - x) ** 2 + (yy - y) ** 2 <= ball_radius ** 2
    img[mask] = ball_color
    return img


def run_demo():
    print("[GenieRedux Demo] No-PyTorch fallback mode")
    print("[GenieRedux Demo] Controls: WASD or Arrow keys. ESC to quit.")

    ball_x, ball_y = 0.5, 0.5
    speed = 0.06
    noise = 0.01

    while True:
        # Render
        frame = create_frame(ball_x, ball_y)
        img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_NEAREST)

        # Overlay text
        cv2.putText(img, f"World Model Demo (fallback) - ball: ({ball_x:.2f}, {ball_y:.2f})",
                    (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(img, "Train the model to replace this simulator!",
                    (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

        cv2.imshow("GenieRedux RTX2070 - World Model Demo", img)

        # Poll key
        key = cv2.waitKey(50) & 0xFF
        if key in CV_KEYS:
            val = CV_KEYS[key]
            if val is None:
                break
            dx, dy = val
            ball_x = max(0.05, min(0.95, ball_x + dx * speed + np.random.uniform(-noise, noise)))
            ball_y = max(0.05, min(0.95, ball_y + dy * speed + np.random.uniform(-noise, noise)))

        time.sleep(0.01)

    cv2.destroyAllWindows()
    print("[GenieRedux Demo] Exited.")


if __name__ == "__main__":
    run_demo()
