#!/usr/bin/env python3
"""
format-code.py
Formats and lints code in the AI Polish Text Expert project.
"""

import subprocess
import sys
import os
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(cmd: list[str], label: str) -> bool:
    print(f"[*] {label}...")
    result = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] {label} failed:\n{result.stdout}\n{result.stderr}")
        return False
    print(f"[+] {label} passed.")
    return True


def main() -> int:
    ok = True

    # Format Python files with black
    py_files = list(ROOT.rglob("*.py"))
    if py_files:
        ok &= run(["black", "--check", "."], "Black formatter check")

    # Lint Python files with flake8
    if py_files:
        ok &= run(["flake8", "."], "Flake8 linter")

    # Format JS/TS files with prettier
    js_files = list(ROOT.rglob("*.js")) + list(ROOT.rglob("*.ts"))
    if js_files:
        ok &= run(["npx", "prettier", "--check", "."], "Prettier formatter check")

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
