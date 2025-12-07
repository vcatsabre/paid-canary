<!-- prettier-ignore -->
# PAID – Portfolio AI Driver (Prototype) 🛰️

> A nerdy, demo-grade assistant for exploring product portfolios, customers,
> incidents, and upgrade opportunities — lovingly built for Global Blitz 2025.

---

![sparkles](https://img.shields.io/badge/status-demo-orange) ![python](https://img.shields.io/badge/python-3.10%2B-blue)

Welcome to **PAID (Portfolio AI Driver)** — a small, opinionated prototype that
lets you ask plain-English questions about your service portfolio and
customer deployments. It's intentionally simple, delightfully nerdy, and
designed for demos and experimentation with synthetic data.

Why "paid-canary"? Think of this repo as a canary in the portfolio mine: it
alerts you to version drift, incidents, and opportunities before they become
real headaches.

**Quick vibes:** Streamlit UI + pandas dataframes + tiny NL intent engine.

---

**Highlights**
- Purpose-built demo for answering questions like:
	- "Which customers use service X?"
	- "What versions are being sunset for customer Y?"
	- "Which services have active incidents right now?"
	- "Where are upgrade gaps and optimization opportunities?"
- Role-aware responses (internal vs. customer) via simple redaction rules.
- Extensible connector stubs for ServiceNow / CRM / profile systems.

---

Getting started
---------------

Requirements: `python 3.10+`, `pip` (or Docker).

1. Create and activate a virtualenv, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r paid-canary/requirements.txt
```

2. Run the demo UI (Streamlit):

```bash
streamlit run paid-canary/app/app.py
```

3. Open the displayed URL (usually `http://localhost:8501`) and poke around.

Or with Docker:

```bash
docker build -t paid-prototype .
docker run --rm -p 8501:8501 paid-prototype
```

Quick test:

```bash
python -m pytest paid-canary/tests/test_engine.py
```

---

Project structure (short)
-------------------------

- `paid-canary/app/` — Streamlit UI, engine, connectors, styles
- `paid-canary/app/core/` — `engine.py`, `data_loader.py`, `security.py`
- `paid-canary/app/connectors/` — stubs for integrations (ServiceNow, CRM)
- `paid-canary/data/` — synthetic JSON datasets (portfolio, customers, incidents)
- `paid-canary/tests/` — small unit tests

---

How it works (brief)
--------------------

1. `load_all` reads the JSON datasets into in-memory pandas DataFrames.
2. `PAIDEngine.answer(q)` classifies the natural-language question into a
	 lightweight intent and dispatches to a handler.
3. Handlers perform pandas-based lookups, build a human-friendly answer, and
	 optionally return structured data (for display in the UI).
4. `security.redact` removes internal columns for the `customer` role.

---

Limitations (aka: the fun constraints)
-------------------------------------
- Rule-based intent parsing — fragile but easy to read.
- Flattened/embedded data model (service lists in DataFrame cells) — fine for
	demos, not for scale.
- Connectors are placeholders — integration is left as an exercise for the
	reader (or the next sprint).
- No auth, telemetry, or production-grade policy enforcement.

---

Roadmap & suggestions
---------------------
- Replace the rule classifier with a small NLP pipeline or LLM-backed intent
	classifier for better entity extraction.
- Normalize the dataset (flatten `services` into a separate table) for
	performant joins.
- Implement real connectors (ServiceNow, CRM) with mapping to the internal
	schema and robust error handling.
- Add CI, more tests, and a small auth layer for role enforcement.

---

Contribute
----------
PRs welcome. If you add a connector, include a small mock and tests.

License
-------
This demo contains synthetic data and is provided for educational/demo use.

---

Made with ❤️ for Global Blitz 2025 — stay nerdy, stay curious. ⚙️
