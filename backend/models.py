from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid


class Job(BaseModel):
    """Modèle pour une offre d'emploi"""
    job_id: str = None
    title: str
    description: str
    requirements: str
    company: str
    location: str
    salary_range: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.job_id:
            self.job_id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now()

    def to_text(self) -> str:
        """Convertit l'offre en texte pour l'embedding"""
        return f"""Titre: {self.title}
Entreprise: {self.company}
Localisation: {self.location}
Description: {self.description}
Exigences: {self.requirements}
Salaire: {self.salary_range or 'Non spécifié'}""".strip()


class CV(BaseModel):
    """Modèle pour un CV de candidat"""
    candidate_id: str = None
    job_id: str
    name: str
    email: str
    phone: Optional[str] = None
    text_content: str
    file_name: str
    uploaded_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.candidate_id:
            self.candidate_id = str(uuid.uuid4())
        if not self.uploaded_at:
            self.uploaded_at = datetime.now()

    def to_text(self) -> str:
        """Convertit le CV en texte pour l'embedding"""
        return f"""Nom: {self.name}
Email: {self.email}
Téléphone: {self.phone or 'Non fourni'}
CV: {self.text_content}""".strip()
