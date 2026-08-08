#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Tiny World Model
A lightweight CNN world model that predicts the next frame from the current frame + action.
Designed to fit and train on a single RTX 2070 8GB GPU.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


class TinyWorldModel(nn.Module):
    """
    Predicts next frame (64x64 RGB) from current frame and one-hot action.
    Actions: 0=noop, 1=left, 2=right, 3=up, 4=down
    """

    def __init__(self, action_dim: int = 5, hidden_dim: int = 64):
        super().__init__()
        self.action_dim = action_dim
        self.hidden_dim = hidden_dim

        # Encoder: frame (3, 64, 64) -> latent
        self.encoder = nn.Sequential(
            nn.Conv2d(3, 32, 4, 2, 1),  # 32x32
            nn.ReLU(),
            nn.Conv2d(32, 64, 4, 2, 1),  # 16x16
            nn.ReLU(),
            nn.Conv2d(64, hidden_dim, 4, 2, 1),  # 8x8
            nn.ReLU(),
        )

        # Action injection: broadcast action to 8x8 and concat
        self.action_proj = nn.Linear(action_dim, hidden_dim)

        # Decoder: latent -> frame (3, 64, 64)
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(hidden_dim * 2, 64, 4, 2, 1),  # 16x16
            nn.ReLU(),
            nn.ConvTranspose2d(64, 32, 4, 2, 1),  # 32x32
            nn.ReLU(),
            nn.ConvTranspose2d(32, 3, 4, 2, 1),  # 64x64
            nn.Sigmoid(),
        )

    def forward(self, frame: torch.Tensor, action: torch.Tensor) -> torch.Tensor:
        """
        frame: (B, 3, 64, 64)
        action: (B, action_dim) one-hot
        returns: (B, 3, 64, 64) next frame
        """
        # Encode
        z = self.encoder(frame)  # (B, hidden_dim, 8, 8)

        # Broadcast action
        B, _, H, W = z.shape
        a = self.action_proj(action)  # (B, hidden_dim)
        a = a.view(B, self.hidden_dim, 1, 1).expand(B, self.hidden_dim, H, W)

        # Concat
        z = torch.cat([z, a], dim=1)  # (B, hidden_dim*2, 8, 8)

        # Decode
        next_frame = self.decoder(z)
        return next_frame


if __name__ == "__main__":
    model = TinyWorldModel()
    x = torch.randn(2, 3, 64, 64)
    a = torch.zeros(2, 5)
    a[0, 1] = 1.0
    a[1, 2] = 1.0
    y = model(x, a)
    print("Input shape:", x.shape)
    print("Action shape:", a.shape)
    print("Output shape:", y.shape)
    print("Parameters:", sum(p.numel() for p in model.parameters()))
