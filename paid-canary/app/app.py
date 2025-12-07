import streamlit as st
import pandas as pd
from pathlib import Path
from core.data_loader import load_all
from core.engine import PAIDEngine
import yaml

st.set_page_config(page_title="PAID Prototype", layout="wide")

# Load config
cfg = yaml.safe_load(open(Path(__file__).resolve().parents[1] / 'appsettings.yaml'))

st.title("PAID – Portfolio AI Driver (Prototype)")
st.caption("Global Blitz 2025 – demo with synthetic data")

# Sidebar controls
st.sidebar.header("Settings")
role = st.sidebar.selectbox("Role", ["internal", "customer"], index=0)
team = st.sidebar.selectbox("Team", ["OCC", "Product", "Exec", "Support", "Customer"], index=0)

# Load data
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
datasets = load_all(str(DATA_DIR))
engine = PAIDEngine(datasets, role=role)

col1, col2 = st.columns([2,1])
with col1:
    q = st.text_input("Ask PAID", value="Which customers use service Mosaic Retail?")
    if st.button("Ask"):
        res = engine.answer(q)
        st.subheader(f"Intent: {res.intent}")
        st.success(res.answer)
        if res.data:
            st.json(res.data)

with col2:
    st.subheader("Datasets")
    with st.expander("Portfolio"):
        st.dataframe(datasets['portfolio'])
    with st.expander("Customers"):
        st.dataframe(datasets['customers'].drop(columns=['services']))
    with st.expander("Incidents"):
        st.dataframe(datasets['incidents'])

st.markdown("---")
st.write("**Examples**: 'Which customers use service ConciergeIQ?', 'What service versions is customer JetBlue using that are to be sunset?', 'What services are impacted for customer Virgin Australia?', 'Show portfolio gaps for customer Aeromexico'.")
