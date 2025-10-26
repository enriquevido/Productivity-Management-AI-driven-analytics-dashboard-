
import streamlit as st, pandas as pd, numpy as np
from utils import load_data, kpi_table, accuracy, bias_seconds, efficiency, learning_trend
from pathlib import Path
from nav import top_nav
top_nav(active="Overview")

st.set_page_config(page_title="Overview Dashboard", page_icon="📊", layout="wide")

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

st.markdown("<div class='big-title'>Productivity Analytics</div>", unsafe_allow_html=True)

cols = st.columns(3)
site = cols[0].selectbox("Site", options=["Global"] + sites["site"].tolist())
cat = cols[1].multiselect("Category", options=sorted(sessions["category"].unique()), default=list(sorted(sessions["category"].unique())))
window = cols[2].slider("Days window", min_value=7, max_value=60, value=30, step=1)

df = sessions.copy()
cutoff = pd.Timestamp.today() - pd.Timedelta(days=window)
df["date"] = pd.to_datetime(df["date"])
df = df[df["date"] >= cutoff]
if site != "Global":
    df = df[df["site"] == site]
if len(cat) > 0:
    df = df[df["category"].isin(cat)]

c1, c2, c3 = st.columns(3)
c1.metric("Model Accuracy", f"{accuracy(df)*100:.1f} %")
c2.metric("Bias", f"{bias_seconds(df):+.0f} s")
c3.metric("Learning Trend (Δ acc.)", f"{learning_trend(versions):+.2f}")

st.write(" ")
lc, rc = st.columns([2,1])
with lc:
    st.markdown("#### AI Model Performance")
    st.area_chart(df.sort_values("date").set_index("date")[["EBT_min","ABT_min"]])

with rc:
    st.markdown("#### Operational Summary")
    st.metric("Avg. EBT (min)", f"{df['EBT_min'].mean():.2f}")
    st.metric("Avg. ABT (min)", f"{df['ABT_min'].mean():.2f}")
    st.markdown("##### Top Units (Efficiency)")
    top = sessions.groupby("site").apply(lambda x: (x["EBT_min"]/x["ABT_min"]).mean()).sort_values(ascending=False).head(3)
    st.table(top.rename("Efficiency"))

st.markdown("#### KPIs")
st.table(kpi_table(df))