import streamlit as st
import requests
from datetime import datetime

API_URL = "http://backend:8000"

def home_page():
    st.markdown('<h1 class="main-header">CareerMatch</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
        <h2 style="color:#1E3A8A; margin-bottom:1rem;">Votre plateforme intelligente de recrutement IA</h2>
        <p style="font-size:1.2rem;">Associez les meilleurs talents à vos opportunités grâce à l'intelligence artificielle</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats en temps réel ──
    try:
        data = requests.get(f"{API_URL}/health", timeout=10).json()
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stats-card"><h3>Offres actives</h3><h4>{data.get("jobs_count", 0)}</h4></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stats-card"><h3>Candidats</h3><h4>{data.get("candidates_count", 0)}</h4></div>', unsafe_allow_html=True)
    except:
        st.warning("Stats en temps réel indisponibles")

    # ── Fonctionnalités ──
    st.markdown("---")
    st.subheader("Fonctionnalités Clés")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <h4>Candidats</h4>
            <ul>
                <li>Matching intelligent</li>
                <li>Score de compatibilité en temps réel</li>
                <li>Analyse automatique du CV</li>
                <li>Processus en quelques clics</li>
            </ul>
        </div>
        
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="feature-card">
            <h4>Recruteurs</h4>
            <ul>
                <li>Génération automatique de questions</li>
                <li>Classement intelligent</li>
                <li>Analyse détaillée des compétences</li>
                <li>Gain de temps massif</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # ── Call to action ──
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### Prêt à transformer votre recrutement ?")
        st.markdown("Rejoignez la révolution de l'IA dans le recrutement !")
    with col2:
        if st.button("Commencer", type="primary", use_container_width=True):
            st.session_state.page = "RH"
            st.rerun()

    # Footer
    st.markdown(f"""
    <div style="text-align:center; color:#666; margin-top:4rem; padding:2rem;">
        <p><strong>CareerMatch</strong> – Plateforme de Recrutement Intelligent • {datetime.now().year}</p>
        <p>Powered by Malak Ben Hassine • Made with ❤️</p>
    </div>
    """, unsafe_allow_html=True)