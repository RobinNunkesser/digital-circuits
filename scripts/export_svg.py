#!/usr/bin/env python3
"""
Exports all .dig circuits in digital-circuits to .svg using Digital CLI.
"""
import os
import sys
import subprocess
from pathlib import Path

DIGITAL_JAR_CANDIDATES = [
    Path("/Applications/Digital/Digital.jar"),
    Path.home() / "Applications/Digital/Digital.jar",
    Path.home() / "Digital/Digital.jar",
]

def find_digital_jar() -> Path:
    env_jar = os.environ.get("DIGITAL_JAR")
    if env_jar and Path(env_jar).is_file():
        return Path(env_jar)
    for cand in DIGITAL_JAR_CANDIDATES:
        if cand.is_file():
            return cand
    raise FileNotFoundError("Digital.jar not found. Please set DIGITAL_JAR environment variable.")

def export_all():
    base_dir = Path(__file__).resolve().parent.parent
    digital_jar = find_digital_jar()
    print(f"Using Digital.jar: {digital_jar}")

    dig_files = list(base_dir.rglob("*.dig"))
    print(f"Found {len(dig_files)} circuit file(s) to export.")

    for dig_path in dig_files:
        svg_path = dig_path.with_suffix(".svg")
        cmd = [
            "java", "-cp", str(digital_jar), "CLI", "svg",
            "-dig", str(dig_path),
            "-svg", str(svg_path),
            "-highContrast"
        ]
        print(f"Exporting {dig_path.name} -> {svg_path.name}...")
        try:
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error exporting {dig_path}: {e.stderr.decode()}", file=sys.stderr)

    print("SVG export completed.")

if __name__ == "__main__":
    export_all()
