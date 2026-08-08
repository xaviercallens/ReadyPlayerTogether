#!/usr/bin/env python3
"""
GenieRedux RTX 2070 - Training Script
Fits TinyWorldModel on synthetic data. Designed for RTX 2070 8GB.
"""

import os
import argparse
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from pathlib import Path

from model import TinyWorldModel
from dataset import SyntheticWorldDataset, generate_dataset


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[GenieRedux] Training on device: {device}")

    # Generate dataset if missing
    if not Path(args.data_dir).exists() or not (Path(args.data_dir) / "frames.npy").exists():
        print("[GenieRedux] Dataset not found, generating...")
        generate_dataset(args.data_dir, n_trajectories=args.n_trajectories)

    # Datasets
    train_ds = SyntheticWorldDataset(args.data_dir, split="train")
    val_ds = SyntheticWorldDataset(args.data_dir, split="val")

    train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=0)

    # Model
    model = TinyWorldModel(action_dim=5, hidden_dim=64).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=args.epochs)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    best_val_loss = float("inf")

    for epoch in range(args.epochs):
        model.train()
        train_loss = 0.0
        for frame, action, next_frame in train_loader:
            frame = frame.to(device)
            action = action.to(device)
            next_frame = next_frame.to(device)

            pred = model(frame, action)
            loss = F.mse_loss(pred, next_frame)

            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()

            train_loss += loss.item()

        train_loss /= len(train_loader)

        # Validation
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for frame, action, next_frame in val_loader:
                frame = frame.to(device)
                action = action.to(device)
                next_frame = next_frame.to(device)
                pred = model(frame, action)
                val_loss += F.mse_loss(pred, next_frame).item()
        val_loss /= len(val_loader)

        scheduler.step()

        print(f"[Epoch {epoch+1}/{args.epochs}] train_loss={train_loss:.4f} val_loss={val_loss:.4f} lr={scheduler.get_last_lr()[0]:.6f}")

        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), out_dir / "best_model.pt")
            print(f"  -> Saved best model (val_loss={val_loss:.4f})")

    # Save final
    torch.save(model.state_dict(), out_dir / "final_model.pt")
    print(f"[GenieRedux] Training complete. Models saved in {out_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default=r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\data")
    parser.add_argument("--output_dir", type=str, default=r"D:\xdev\Oasis\Server_AI\genie_redux_rtx2070\checkpoints")
    parser.add_argument("--n_trajectories", type=int, default=500)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--lr", type=float, default=1e-3)
    args = parser.parse_args()

    train(args)
