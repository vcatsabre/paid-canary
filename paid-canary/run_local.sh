#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/app.py --server.port=$(yq '.server.port' appsettings.yaml)
