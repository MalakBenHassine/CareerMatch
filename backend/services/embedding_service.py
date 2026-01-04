import pdfplumber
import logging
import re
import numpy as np
from sentence_transformers import SentenceTransformer
from fastapi import UploadFile

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("Chargement modèle embedding...")
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    async def extract_pdf_text(self, file: UploadFile) -> str:
        content = ""
        file.file.seek(0)
        try:
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        content += text + "\n"
        except:
            content = str(await file.read())
        return re.sub(r'\s+', ' ', content.strip())

    def encode_text(self, text: str):
        if not text.strip():
            return [0.0] * 384
        return self.model.encode(text, normalize_embeddings=True).tolist()

    def calculate_matching_score(self, cv_text: str, job_payload: dict) -> dict:
        job_text = f"{job_payload.get('title','')} {job_payload.get('description','')} {job_payload.get('requirements','')}"
        job_text = job_text.lower()
        cv_text = cv_text.lower()

        # 1. Similarité vectorielle
        if len(cv_text) > 50 and len(job_text) > 50:
            cv_vec = self.encode_text(cv_text)
            job_vec = self.encode_text(job_text)
            semantic = float(np.dot(cv_vec, job_vec)) * 100
        else:
            semantic = 30.0

        # 2. Compétences clés
        job_keywords = set(re.findall(r'\b[a-z]{3,15}\b', job_text))
        cv_keywords = set(re.findall(r'\b[a-z]{3,15}\b', cv_text))
        common = job_keywords.intersection(cv_keywords)
        tech_match = len(common)

        # Score final réaliste
        score = semantic * 0.6 + tech_match * 2.0
        score = min(94.0, max(15.0, score))

        return {
            "score": round(score, 1),
            "tech_count": tech_match,
            "matched_keywords": list(common)[:8]
        }

embedding = EmbeddingService()