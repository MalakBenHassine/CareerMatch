import streamlit as st
import requests
from typing import List, Dict, Any, Optional

API_URL = "http://backend:8000"
TIMEOUT = 120

def _handle_error(e: Exception, action: str):
    st.error(f"Erreur lors de {action} : {str(e)}")
    return None

def get_jobs() -> List[Dict]:
    try:
        r = requests.get(f"{API_URL}/jobs", timeout=30)
        r.raise_for_status()
        return r.json()
    except:
        return []

def create_job(data: Dict) -> Optional[Dict]:
    try:
        r = requests.post(f"{API_URL}/jobs", data=data, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _handle_error(e, "la création de l'offre")
        return None

def submit_cv(name: str, email: str, phone: str, job_id: str, cv_file) -> Optional[Dict]:
    try:
        files = {"cv_file": (cv_file.name, cv_file, "application/pdf")}
        data = {"name": name, "email": email, "phone": phone, "job_id": job_id}
        r = requests.post(f"{API_URL}/candidates", data=data, files=files, timeout=180)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        _handle_error(e, "l'envoi du CV")
        return None

def get_candidates(job_id: str) -> Optional[Dict]:
    try:
        r = requests.get(f"{API_URL}/jobs/{job_id}/candidates", timeout=90)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.warning("Impossible de charger les candidatures.")
        return None

def generate_questions(job_id: str, candidate_id: str) -> Optional[Dict]:
    try:
        r = requests.post(
            f"{API_URL}/generate-questions",
            data={"job_id": job_id, "candidate_id": candidate_id},
            timeout=300
        )
        r.raise_for_status()
        return r.json()
    except Exception as e:
        st.error("Échec génération des questions (Ollama peut être occupé)")
        return None