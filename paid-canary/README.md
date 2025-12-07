# PAID – Portfolio AI Driver (Prototype)

> **Global Blitz 2025 – Working Demo (MVP)**

This is a runnable prototype of the PAID chatbot MVP that demonstrates:

- **Portfolio Data Dump & Query Engine** over synthetic sample data
- **Customer Subscription Intelligence** ("Which customers use service X?")
- **Service Impact & Change Awareness** (incidents & changes)
- **Gap Analysis & Optimization** (unused/at-risk services)
- **Restriction-aware responses** using simple role-based filtering

> **Note**: All datasets in `data/` are **synthetic** and created for demo purposes only.

---

## Quick Start (local)

### Option A – With Python
1. Ensure Python 3.10+ is installed
2. Create a virtual env and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
3. Run the app:
```bash
streamlit run app/app.py
```
4. Open the browser URL shown by Streamlit (typically http://localhost:8501)

### Option B – With Docker
```bash
docker build -t paid-prototype .
docker run --rm -p 8501:8501 paid-prototype
```

---

## What Can I Ask?
- *"Which customers use service X?"*
- *"What service versions is customer Y using that are to be sunset?"*
- *"What services are impacted for customer Z right now?"*
- *"Show portfolio gaps for customer Y"*

Use the left sidebar to set **role** (Internal vs Customer) and **team** (OCC, Product, Exec, etc.).

---

## Structure
```
paid-prototype/
├─ app/
│  ├─ app.py                # Streamlit UI entrypoint
│  ├─ core/
│  │  ├─ engine.py          # Query engine & NL intents
│  │  ├─ data_loader.py     # Data loader with caching
│  │  ├─ security.py        # Role-based redaction rules
│  │  └─ __init__.py
│  ├─ connectors/           # Stubs for future integrations
│  │  ├─ servicenow.py
│  │  ├─ profiles.py
│  │  └─ crm.py
│  └─ ui/
│     └─ styles.css
├─ data/
│  ├─ portfolio.json        # Services, versions, lifecycle
│  ├─ customers.json        # Customer portfolios
│  ├─ incidents.json        # Example incidents
│  └─ changes.json          # Example changes
├─ tests/
│  └─ test_engine.py        # Minimal tests
├─ requirements.txt
├─ Dockerfile
├─ appsettings.yaml         # App config (ports, flags)
└─ run_local.sh
```

---

## Security & Compliance (demo)
- Role-based response filtering: Internal roles may view impact metadata; customers see only non-privileged summaries.
- No PII or production data; demo uses **synthetic datasets**.

---

## Credits
Created for Global Blitz 2025 demo. Maintainers: Team **Get PAID**.
