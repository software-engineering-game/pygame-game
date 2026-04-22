#!/usr/bin/env bash
# Prefer Python 3.11+ with pygame wheels; avoid 3.14+ until pygame publishes wheels.
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v python3.12 >/dev/null 2>&1; then
  PY=python3.12
elif command -v python3.11 >/dev/null 2>&1; then
  PY=python3.11
else
  PY=python3
fi
echo "Using: $($PY --version)"
$PY -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
echo "Done. Run: source .venv/bin/activate && python main.py"
