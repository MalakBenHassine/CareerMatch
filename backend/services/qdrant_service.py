import os
import uuid
import logging
from datetime import datetime
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

from services.embedding_service import embedding

logger = logging.getLogger(__name__)

class QdrantService:
    def __init__(self):
        self.client = QdrantClient(host=os.getenv("QDRANT_HOST", "qdrant"), port=6333)
        self._setup_collections()

    def _setup_collections(self):
        existing = {c.name for c in self.client.get_collections().collections}
        for name, size in [("jobs", 384), ("cvs", 384)]:
            if name not in existing:
                self.client.create_collection(
                    collection_name=name,
                    vectors_config=VectorParams(size=size, distance=Distance.COSINE)
                )
                logger.info(f"Collection '{name}' créée")
                
    def _upsert(self, collection: str, id: str, vector: list, payload: dict):
        self.client.upsert(collection, points=[PointStruct(id=id, vector=vector, payload=payload)])

    def create_job(self, title, company, location, description, requirements, salary_range=None):
        job_id = str(uuid.uuid4())
        payload = {
            "job_id": job_id, "title": title, "company": company, "location": location,
            "description": description, "requirements": requirements,
            "salary_range": salary_range or "À négocier",
            "created_at": datetime.now().isoformat()
        }
        self._upsert("jobs", job_id, embedding.encode_text(f"{title} {description} {requirements}"), payload)
        return job_id
    
    def add_candidate(self, job_id, name, email, phone, text, file_name, vector, score, tech_count):
        cid = str(uuid.uuid4())
        payload = {
            "candidate_id": cid, "job_id": job_id, "name": name, "email": email,
            "phone": phone or "", "content": text, "file_name": file_name,
            "score": score, "tech_count": tech_count, "uploaded_at": datetime.now().isoformat()
        }
        self._upsert("cvs", cid, vector, payload)
        return cid

    def get_job_by_id(self, job_id):         return (self.client.retrieve("jobs", ids=[job_id]) or [None])[0]
    def get_candidate_by_id(self, cid):      return (self.client.retrieve("cvs", ids=[cid]) or [None])[0].payload if self.client.retrieve("cvs", ids=[cid]) else None

    def get_all_jobs(self):
        return [p.payload for p in self.client.scroll("jobs", limit=1000)[0]]
    def search_candidates_by_job(self, job_id, limit=50):
        job = self.get_job_by_id(job_id)
        if not job: return []
    
        vec = embedding.encode_text(f"{job.payload['title']} {job.payload['description']} {job.payload['requirements']}")
    
        hits = self.client.search(
            collection_name="cvs",
            query_vector=vec,
            query_filter=Filter(must=[FieldCondition(key="job_id", match=MatchValue(value=job_id))]),
            limit=limit
        )
        return [h.payload for h in hits]


qdrant = QdrantService()