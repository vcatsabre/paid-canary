import json
from app.core.data_loader import load_all
from app.core.engine import PAIDEngine


def test_basic_query():
    d = load_all('data')
    eng = PAIDEngine(d, role='internal')
    r = eng.answer('Which customers use service Mosaic Retail?')
    assert 'Customers using service' in r.answer
