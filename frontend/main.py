import streamlit as st
from pages.home import home_page
from pages.candidate import candidate_page
from pages.admin import admin_page

# Configuration globale de l'app
st.set_page_config(page_title="CareerMatch", page_icon="target", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    [data-testid="stSidebarNav"], [data-testid="stMainMenu"], footer, header,
    .stDeployButton, button[title="View fullscreen"], [data-testid="stToolbar"],
    [data-testid="stDecoration"] { display: none !important; }
    .main-header { font-size: 3.5rem; color: #1E3A8A; text-align: center; font-weight bold; margin: 2rem 0; }
    .highlight { background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%); padding: 2.5rem; border-radius: 15px; text-align: center; margin: 2rem 0; }
    .block-container { padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Accueil"

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:1.5rem;">
        <h1 style="color:#1E3A8A; margin:0;">CareerMatch</h1>
        <p style="color:#666; margin:5px 0 0;">Recrutement Intelligent</p>
    </div>
    <hr style="margin:1rem 0;">
    """, unsafe_allow_html=True)

    if st.button("Accueil", use_container_width=True, type="primary" if st.session_state.page == "Accueil" else "secondary"):
        st.session_state.page = "Accueil"
        st.rerun()
    if st.button("Candidat", use_container_width=True, type="primary" if st.session_state.page == "Candidat" else "secondary"):
        st.session_state.page = "Candidat"
        st.rerun()
    if st.button("RH", use_container_width=True, type="primary" if st.session_state.page == "RH" else "secondary"):
        st.session_state.page = "RH"
        st.rerun()

# ROUTING 
if st.session_state.page == "Accueil":
    home_page()
elif st.session_state.page == "Candidat":
    candidate_page()
elif st.session_state.page == "RH":
    admin_page()