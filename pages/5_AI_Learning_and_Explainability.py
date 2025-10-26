
import streamlit as st, pandas as pd, numpy as np
from utils import load_data
from pathlib import Path
from nav import top_nav
top_nav(active="AI Learning")

st.set_page_config(page_title="AI Learning & Explainability", page_icon="🧠", layout="wide")

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

st.markdown("<div class='big-title'>AI Learning & Model Explainability</div>", unsafe_allow_html=True)

st.markdown("##### Model versions")
st.dataframe(versions)

c1, c2, c3 = st.columns([1,1,1])
with c1:
    st.markdown("#### Feature Importance (latest)")
    last = versions.sort_values("version").iloc[-1]
    imp = pd.DataFrame({
        "feature":["ΔItems","ΔSKUs","Layout","Reachability","Cold Chain","Prepack Ratio"],
        "importance":[last["d_items"],last["d_skus"],last["layout"],last["reachability"],last["cold_chain"],last["prepack_ratio"]]
    })
    st.bar_chart(imp.set_index("feature"))
with c2:
    st.markdown("#### Accuracy Over Time")
    st.line_chart(versions.set_index("date")[["accuracy"]])
with c3:
    st.markdown("#### EBT vs. ABT Buckets (matrix)")
    df = sessions.copy()
    df["ABT_bucket"] = pd.cut(df["ABT_min"], bins=[0,4,6,8,100], labels=["0-4","4-6","6-8","8+"])
    df["EBT_bucket"] = pd.cut(df["EBT_min"], bins=[0,4,6,8,100], labels=["0-4","4-6","6-8","8+"])
    mat = df.pivot_table(index="EBT_bucket", columns="ABT_bucket", values="employee", aggfunc="count").fillna(0)
    st.dataframe(mat.astype(int))

st.divider()
st.markdown("### Retrain Simulator")
st.caption("Añade sesiones y crea una nueva versión del modelo con mejor accuracy.")

col_a, col_b = st.columns([1,2])
with col_a:
    add_n = st.number_input("New sessions to add", 10, 500, 200, step=10)
    if st.button("Trigger retrain"):
        latest_date = pd.to_datetime(sessions["date"]).max()
        sample = sessions.sample(int(add_n), replace=True).copy()
        sample["date"] = (latest_date + pd.Timedelta(days=1)).date().isoformat()
        sample["ABT_min"] = (sample["ABT_min"]*np.random.uniform(0.98,1.0,size=len(sample))).round(2)
        all_sessions = pd.concat([pd.read_csv("data/sessions.csv"), sample], ignore_index=True)
        all_sessions.to_csv("data/sessions.csv", index=False)
        last = versions.sort_values("version").iloc[-1]
        new = last.copy()
        new["version"] = int(last["version"]) + 1
        new["date"] = pd.Timestamp.today().date().isoformat()
        new["accuracy"] = float(min(0.99, last["accuracy"] + np.random.uniform(0.01,0.03)))
        new["bias_s"] = float(max(0, last["bias_s"] - np.random.uniform(0.5,2.0)))
        for f in ["d_items","d_skus","layout","reachability","cold_chain","prepack_ratio"]:
            new[f] = float(max(0.02, min(0.7, last[f] + np.random.normal(0,0.01))))
        cols = ["d_items","d_skus","layout","reachability","cold_chain","prepack_ratio"]
        s = sum(new[c] for c in cols)
        for c in cols:
            new[c] = float(new[c]/s)
        vv = pd.read_csv("data/model_versions.csv")
        vv = pd.concat([vv, pd.DataFrame([new])], ignore_index=True)
        vv.to_csv("data/model_versions.csv", index=False)
        st.success(f"Model retrained with +{int(add_n)} new sessions. Accuracy improved to {new['accuracy']:.3f}.")
        st.experimental_rerun()
with col_b:
    st.info("El retrain simulator duplica sesiones recientes con mejora sutil en ABT y agrega una nueva versión con accuracy ligeramente superior.")
