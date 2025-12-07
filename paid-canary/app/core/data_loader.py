from __future__ import annotations
from functools import lru_cache
from typing import Dict
import json
import pandas as pd
from pathlib import Path

@lru_cache(maxsize=1)
def load_all(data_dir: str) -> Dict[str, pd.DataFrame]:
    base = Path(data_dir)
    portfolio = pd.read_json(base / 'portfolio.json', orient='records')
    customers = pd.read_json(base / 'customers.json', orient='records')
    incidents = pd.read_json(base / 'incidents.json', orient='records')
    changes = pd.read_json(base / 'changes.json', orient='records')
    return {
        'portfolio': portfolio,
        'customers': customers,
        'incidents': incidents,
        'changes': changes,
    }
