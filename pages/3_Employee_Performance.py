
import streamlit as st, pandas as pd, numpy as np
from utils import load_data
from pathlib import Path
from nav import top_nav
top_nav(active="Employees")

st.set_page_config(page_title="Employee Performance", page_icon="🧑‍🔧", layout="wide")

st.markdown("""
<style>
/* Ocultar sidebar completamente */
section[data-testid="stSidebar"] {display: none;}
/* Ajustar el ancho del contenido para ocupar toda la pantalla */
div.block-container {padding-left: 3rem; padding-right: 3rem;}
</style>
""", unsafe_allow_html=True)

st.markdown(f"<style>{(Path(__file__).resolve().parents[1] / 'assets' / 'theme.css').read_text()}</style>", unsafe_allow_html=True)

sessions, employees, sites, versions, users = load_data()

st.markdown("<div class='big-title'>Employee Performance</div>", unsafe_allow_html=True)

site = st.selectbox("Site", options=sites["site"].tolist())
df = sessions[sessions["site"] == site]

st.markdown("#### Top 3 by Efficiency")
lb = df.groupby("employee")[["EBT_min","ABT_min"]].mean()
lb["Efficiency"] = lb["EBT_min"]/lb["ABT_min"]
lb = lb.sort_values("Efficiency", ascending=False).head(3)[["Efficiency"]]
st.table(lb.style.format({"Efficiency":"{:.2f}"}))

c1, c2 = st.columns(2)
with c1:
    st.markdown("#### EBT vs. ABT by Category")
    st.scatter_chart(df, x="ABT_min", y="EBT_min", color="category")
with c2:
    st.markdown("#### Distribution of Actual Build Times")
    hist, edges = np.histogram(df["ABT_min"], bins=10)
    st.bar_chart(pd.DataFrame({"count": hist}))

st.markdown("#### Detail")
detail = df.groupby(["employee","employee_id"]).agg(
    site=("site","first"),
    ABT=("ABT_min","mean"),
    EBT=("EBT_min","mean")
)
detail["Efficiency"] = detail["EBT"]/detail["ABT"]
detail = detail.drop(columns=["EBT"]).sort_values("Efficiency", ascending=False)
st.dataframe(detail.reset_index())
