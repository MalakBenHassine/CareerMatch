import streamlit as st
import time
from api import create_job, get_jobs, get_candidates, generate_questions

def admin_page():
    st.markdown("<h1 style='text-align:center; color:#1E3A8A;'>Espace RH – Recrutement Intelligent</h1>", unsafe_allow_html=True)
    st.markdown("---")

    # === 1. Créer une offre ===
    with st.expander("Publier une nouvelle offre d'emploi", expanded=True):
        with st.form("create_job"):
            c1, c2 = st.columns(2)
            with c1:
                title = st.text_input("Intitulé du poste *", placeholder="Développeur Fullstack")
                company = st.text_input("Entreprise *", placeholder="TechNova")
            with c2:
                location = st.text_input("Localisation *", placeholder="Paris / Remote")
                salary = st.text_input("Salaire (facultatif)", placeholder="50-70k €")

            description = st.text_area("Description du poste *", height=100)
            requirements = st.text_area("Compétences requises *", height=100)

            if st.form_submit_button("Publier l'offre", type="primary", use_container_width=True):
                if not all([title, company, location, description, requirements]):
                    st.error("Les champs obligatoires (*) doivent être remplis.")
                else:
                    with st.spinner("Publication en cours..."):
                        result = create_job({
                            "title": title, "company": company, "location": location,
                            "description": description, "requirements": requirements,
                            "salary_range": salary or "À négocier"
                        })
                    if result:
                        st.success("Offre publiée avec succès !")
                        st.balloons()
                        time.sleep(1.5)
                        st.rerun()

    st.markdown("---")

    # === 2. Liste des offres ===
    jobs = get_jobs()
    if not jobs:
        st.info("Aucune offre publiée pour le moment.")
        return

    for job in jobs:
        job_id = job["job_id"]
        title = job["title"]
        company = job["company"]

        with st.expander(f"{title} • {company} • {job.get('location', '')}", expanded=False):
            st.write(f"**Salaire :** {job.get('salary_range', 'À négocier')}")
            st.caption(job["description"][:300] + ("..." if len(job["description"]) > 300 else ""))

            if st.button("Voir les candidatures", key=f"view_{job_id}", use_container_width=True):
                st.session_state.selected_job = job_id
                st.rerun()

            if st.session_state.get("selected_job") == job_id:
                _show_candidates(job_id, title)

def _show_candidates(job_id: str, job_title: str):
    st.markdown("### Candidatures reçues")
    with st.spinner("Analyse des CVs en cours..."):
        data = get_candidates(job_id)

    if not data or not data.get("top_5"):
        st.info("Aucune candidature pour cette offre.")
        return

    st.success(f"**{data['total_candidates']}** candidature(s) reçue(s)")

    # Top 5
    for idx, cand in enumerate(data["top_5"], 1):
        score = cand["score"]
        color = "#10B981" if score >= 70 else "#F59E0B" if score >= 50 else "#EF4444"
        with st.container():
            st.markdown(f"""
            <div style="border:2px solid {color}; border-radius:12px; padding:15px; margin:10px ; background:#f9f9f9;">
                <h4 style="margin:0; color:{color};">{idx}. {cand['name']} → {score:.1f}%</h4>
                <p><strong>Email:</strong> {cand['email']} | <strong>Compétences:</strong> {cand['tech_count']}</p>
            </div>
            """, unsafe_allow_html=True)

            if score >= 60:
                key = f"gen_{job_id}_{cand['candidate_id']}"
                if st.button(f"Générer 10 questions d'entretien pour {cand['name']}", key=key):
                    with st.spinner("L'IA génère des questions personnalisées..."):
                        questions = generate_questions(job_id, cand['candidate_id'])
                        if questions and questions.get("questions"):
                            st.success("Questions générées !")
                            tech = questions["questions"][:5]
                            comp = questions["questions"][5:10]
                            c1, c2 = st.columns(2)
                            with c1:
                                st.markdown("#### Questions Techniques")
                                for i, q in enumerate(tech, 1):
                                    st.write(f"**{i}.** {q}")
                            with c2:
                                st.markdown("#### Questions Comportementales")
                                for i, q in enumerate(comp, 6):
                                    st.write(f"**{i}.** {q}")
                        else:
                            st.error("Échec de génération des questions.")