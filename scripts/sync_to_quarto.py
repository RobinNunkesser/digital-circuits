#!/usr/bin/env python3
"""
Synchronizes .dig and .svg files from digital-circuits into md/quarto/gdi/simulations/.
"""
import shutil
from pathlib import Path

def sync():
    base_dir = Path(__file__).resolve().parent.parent
    work_repo = base_dir.parents[3]
    quarto_sim_dir = work_repo / "md" / "quarto" / "gdi" / "simulations"
    quarto_sim_dir.mkdir(parents=True, exist_ok=True)

    print(f"Syncing digital circuits to {quarto_sim_dir}...")
    copied = 0
    for ext in ["*.dig", "*.svg"]:
        for file_path in base_dir.rglob(ext):
            if "scripts" in file_path.parts:
                continue
            dest = quarto_sim_dir / file_path.name
            shutil.copy2(file_path, dest)
            copied += 1
            print(f"  {file_path.name} -> {dest}")

    print(f"Synced {copied} files.")

if __name__ == "__main__":
    sync()
