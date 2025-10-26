import streamlit as st
import pandas as pd
from utils import load_data
from pathlib import Path

st.set_page_config(page_title="gategroup • Productivity Analytics", page_icon="🛒", layout="wide")

st.markdown("""
<style>
/* Ocultar sidebar completamente */
section[data-testid="stSidebar"] {display: none;}
/* Ajustar el ancho del contenido para ocupar toda la pantalla */
div.block-container {padding-left: 3rem; padding-right: 3rem;}
</style>
""", unsafe_allow_html=True)

theme_path = Path(__file__).parent / "assets" / "theme.css"
st.markdown(f"<style>{theme_path.read_text()}</style>", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

sessions, employees, sites, versions, users = load_data()

st.markdown("<div class='big-title'>gategroup</div>", unsafe_allow_html=True)
st.title("Productivity Management")

col1, col2 = st.columns([2,1])
with col1:
    eid = st.text_input("Employee ID", placeholder="E001")
    pwd = st.text_input("Password", type="password", placeholder="demo")
    role = st.radio("Role", ["Operator","Supervisor","Admin"], horizontal=True)
    unit = st.selectbox("Unit / Site", options=sites["site"].tolist())
    if st.button("Log In", use_container_width=True):
        row = users.query("employee_id == @eid and password == @pwd")
        if not row.empty and (row.iloc[0]["role"] == role or role == "Admin"):
            st.session_state.user = {"employee_id":eid, "role": role, "site": unit, "name": row.iloc[0]["name"]}
            st.success(f"Welcome {row.iloc[0]['name']} — redirecting to dashboard...")
            # 🔁 Redirige a tu pantalla principal
            import time
            time.sleep(0.8)
            st.switch_page("pages/2_Overview_Dashboard.py")
        else:
            st.error("Invalid credentials or role.")
with col2:
    st.markdown("### Demo users")
    st.table(users.drop(columns=["password"]))

st.info("Open other pages from the left sidebar after login.")
