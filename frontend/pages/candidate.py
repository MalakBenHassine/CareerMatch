import streamlit as st
from api import get_jobs, submit_cv

def candidate_page():
    st.markdown("<h1 style='text-align:center; color:#1E3A8A;'>Espace Candidat</h1>", unsafe_allow_html=True)
    st.markdown("---")

    with st.form("candidate_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Nom complet *", placeholder="Malak Ben Hassine")
            email = st.text_input("Email *", placeholder="benhassinemalak4@gmail.com")
        
        with col2:
            phone = st.text_input("Téléphone *", placeholder="+216 26 833 807")
            jobs = get_jobs()
            options = [f"{j['title']} - {j['company']}" for j in jobs] or ["Aucune offre disponible"]
            selected = st.selectbox("Offre visée *", ["Choisir une offre..."] + options)

        cv = st.file_uploader("Votre CV (PDF uniquement) *", type="pdf", help="PDF uniquement, max 10 Mo")

        submitted = st.form_submit_button("Postuler maintenant", type="primary", use_container_width=True)

        if submitted:
            if not all([name.strip(), email.strip(), phone.strip(), cv, selected != "Choisir une offre..."]):
                st.error("Tous les champs marqués d'une étoile (*) sont obligatoires.")
                return

            # Récupérer l'ID de l'offre
            job_id = next((j["job_id"] for j in jobs if f"{j['title']} - {j['company']}" == selected), None)
            if not job_id:
                st.error("Offre introuvable. Veuillez réessayer.")
                return

            with st.spinner("Analyse de votre CV en cours... (IA + scoring sémantique)"):
                result = submit_cv(name.strip(), email.strip(), phone.strip(), job_id, cv)

            if result and result.get("score", 0) > 0:
                score = result["score"]
                color = "#10B981" if score >= 70 else "#F59E0B" if score >= 50 else "#EF4444"
                st.markdown(f"""
                <div style="text-align:center; padding:2rem; background:#f8f9fa; border-radius:15px; border:3px solid {color}; margin:2rem 0;">
                    <h2>Félicitations ! Votre score : <strong style="color:{color};">{score:.1f}%</strong></h2>
                    <p>Plus votre score est élevé, plus vous correspondez à l'offre !</p>
                </div>
                """, unsafe_allow_html=True)
                st.success("Candidature envoyée avec succès ! Le recruteur vous contactera si votre profil est retenu.")
                st.balloons()
            else:
                st.error("Échec de l'envoi. Veuillez vérifier votre CV et réessayer.")