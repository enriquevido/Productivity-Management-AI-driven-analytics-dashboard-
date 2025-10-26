import streamlit as st, pandas as pd, numpy as np
import plotly.express as px
from utils import load_data
from pathlib import Path
from nav import top_nav

# ---- Configuración
st.set_page_config(page_title="Benchmark & Global", page_icon="🌍", layout="wide")

# ---- Navbar
top_nav(active="Benchmark")

# ---- Estilos
st.markdown("""
<style>
section[data-testid="stSidebar"] {display: none;}
div.block-container {padding-left: 3rem; padding-right: 3rem;}
</style>
""", unsafe_allow_html=True)

# (opcional) tema visual
st.markdown(
    f"<style>{(Path(__file__).resolve().parents[1] / 'assets' / 'theme.css').read_text()}</style>",
    unsafe_allow_html=True
)

# ---- Datos
sessions, employees, sites, versions, users = load_data()

st.markdown("<div class='big-title'>Benchmark & Global Comparison</div>", unsafe_allow_html=True)

g = sessions.groupby("site")
site_metrics = pd.DataFrame({
    "site": g.size().index,
    "accuracy": g.apply(lambda x: (x["ABT_min"].sub(x["EBT_min"]).abs() <= 0.5).mean()).values,
    "efficiency": g.apply(lambda x: (x["EBT_min"] / x["ABT_min"]).mean()).values,
    "bias_s": g.apply(lambda x: (x["ABT_min"] - x["EBT_min"]).mean() * 60.0).values,
    "avg_EBT": g["EBT_min"].mean().values,
    "avg_ABT": g["ABT_min"].mean().values,
})

# ---- Mapa global (Efficiency by Site)
airport_coords = {
    "CDG": (49.0097,   2.5479),   # Paris
    "FRA": (50.0379,   8.5622),   # Frankfurt
    "JFK": (40.6413, -73.7781),   # New York
    "ORD": (41.9742, -87.9073),   # Chicago
    "PER": (-31.9403,115.9670),   # Perth
}

map_df = site_metrics.copy()
map_df["lat"] = map_df["site"].map(lambda s: airport_coords.get(s, (None, None))[0])
map_df["lon"] = map_df["site"].map(lambda s: airport_coords.get(s, (None, None))[1])

st.markdown("#### Global Map (Efficiency by Site)")
fig = px.scatter_geo(
    map_df.dropna(subset=["lat","lon"]),
    lat="lat", lon="lon",
    color="efficiency", size="efficiency",
    size_max=28, projection="natural earth",
    hover_name="site",
    hover_data={"efficiency":":.2f", "lat":False, "lon":False},
    color_continuous_scale="Blues",
)
fig.update_layout(margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(fig, use_container_width=True)

# ---- Tabla comparativa
st.markdown("#### Site Table")
show = site_metrics.copy()
show["Accuracy (%)"] = (show["accuracy"]*100).round(1)
show["Efficiency"] = show["efficiency"].round(2)
show["Bias (s)"] = show["bias_s"].round(1)
show = show[["site","Accuracy (%)","Efficiency","Bias (s)","avg_EBT","avg_ABT"]]
show = show.rename(columns={"site":"Site","avg_EBT":"Avg EBT","avg_ABT":"Avg ABT"})
st.table(show)

# ---- Tendencia global
st.markdown("#### Global Trendline (rolling mean)")
tmp = sessions.sort_values("date").copy()
tmp["date"] = pd.to_datetime(tmp["date"])
roll = tmp.set_index("date")[["EBT_min","ABT_min"]].rolling("14D").mean().dropna()
st.line_chart(roll)
