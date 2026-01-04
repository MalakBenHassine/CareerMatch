from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from services.qdrant_service import qdrant
from services.embedding_service import embedding
from services.ollama_service import ollama


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CareerMatch API", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Route  de création d'offre appelle qdrant.create_job()
@app.post("/jobs")
async def create_job(
    title: str = Form(...),
    company: str = Form(...),
    location: str = Form(...),
    description: str = Form(...),
    requirements: str = Form(...),
    salary_range: str = Form(None)
):
    job_id = qdrant.create_job(title, company, location, description, requirements, salary_range)
    logger.info(f"Offre créée : {title} @ {company}")
    return {"job_id": job_id, "title": title, "company": company}

@app.get("/jobs")
def list_jobs():
    return qdrant.get_all_jobs()

# Route de candidature appelle qdrant.add_candidate() 
@app.post("/candidates")
async def submit_cv(
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    job_id: str = Form(...),
    cv_file: UploadFile = File(...)
):
    if not cv_file.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Seul le format PDF est accepté")
    job = qdrant.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Offre non trouvée")
    text = await embedding.extract_pdf_text(cv_file)
    # Si le texte est trop court, remplace par un message par défaut
    if len(text.strip()) < 100:
        text = f"[CV non lisible] Candidat: {name} | Email: {email}"
    # Calcule le score de matching entre le CV et l'offre
    score_data = embedding.calculate_matching_score(text, job.payload)
    # Calcule le vecteur embedding du CV
    vector = embedding.encode_text(text)
    # Ajoute le candidat dans Qdrant
    candidate_id = qdrant.add_candidate(
        job_id=job_id,
        name=name, email=email, phone=phone,
        text=text, file_name=cv_file.filename,
        vector=vector, score=score_data["score"], tech_count=score_data["tech_count"]
    )
    logger.info(f"Candidature {name} → {score_data['score']:.1f}%")
    return {
        "candidate_id": candidate_id,
        "score": score_data["score"],
        "tech_count": score_data["tech_count"],
        "message": "Candidature analysée avec succès"
    }

# Route liste candidats pour une offre appelle qdrant.search_candidates_by_job()
@app.get("/jobs/{job_id}/candidates")
def get_candidates(job_id: str):
    job = qdrant.get_job_by_id(job_id)
    if not job:
        raise HTTPException(404, "Offre non trouvée")
    # Recherche les candidats associés
    candidates = qdrant.search_candidates_by_job(job_id, limit=100)
    # Trie par score décroissant
    sorted_cands = sorted(candidates, key=lambda x: x["score"], reverse=True)
    return {
        "job_title": job.payload["title"],
        "total_candidates": len(sorted_cands),
        "top_5": sorted_cands[:5],
        "all_candidates": sorted_cands
    }
# Route génération questions Récupère job + candidat → appelle ollama.generate_questions()  
@app.post("/generate-questions")
def generate_questions(job_id: str = Form(...), candidate_id: str = Form(...)):
    job = qdrant.get_job_by_id(job_id)
    candidate = qdrant.get_candidate_by_id(candidate_id)
    if not job or not candidate:
        raise HTTPException(404, "Offre ou candidat introuvable")
    questions = ollama.generate_questions(
        job_title=job.payload["title"],
        company=job.payload["company"],
        cv_text=candidate["content"]
    )
    return {"questions": questions}

@app.get("/health")
def health():
    jobs = len(qdrant.get_all_jobs())
    candidates_count = len(qdrant.client.scroll(collection_name="cvs", limit=10000)[0])
    ollama_status = ollama.health_check()
    return {
        "status": "healthy" if ollama_status["ollama_accessible"] else "degraded",
        "jobs_count": jobs,
        "candidates_count": candidates_count,
        "ollama": ollama_status,
        "timestamp": datetime.now().isoformat()
    }

