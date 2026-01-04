# backend/services/ollama_service.py
import requests
import os
import logging
import re

logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        self.url = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")
        self.model = os.getenv("LLM_MODEL", "llama3.2:1b")

    def generate_questions(self, job_title: str, company: str, cv_text: str) -> list:
        prompt = f"""### RÔLE
Tu es un Senior Technical Recruiter chez {company}, expert en évaluation de profils {job_title}.

### MISSION
Génère EXACTEMENT 10 questions d'entretien en français pour le candidat ci-dessous.

### RÈGLES STRICTES (à respecter à 100 %)
- Réponds UNIQUEMENT avec les 10 lignes numérotées ci-dessous
- Aucun texte avant, après, ni explication
- Format exact : 1. Question ?
- Questions 1 à 5 → techniques et très précises (doivent faire référence au CV ou au poste)
- Questions 6 à 10 → comportementales / situationnelles (leadership, collaboration, résolution de problèmes)

### CONTEXTE
Poste : {job_title}
Entreprise : {company}

### CV DU CANDIDAT (à exploiter obligatoirement)
{cv_text[:2800]}

### RÉPONDS EXACTEMENT COMME ÇA (10 lignes seulement) :
1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
9. 
10. """

        try:
            response = requests.post(
                f"{self.url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 800}
                },
                timeout=180
            )
            response.raise_for_status()
            text = response.json().get("response", "").strip()

            # Extraction ultra-robuste
            questions = []
            for line in text.split('\n'):
                line = line.strip()
                if re.match(r'^\d+\.\s+', line):
                    q = re.sub(r'^\d+\.\s+', '', line).strip()
                    if q and len(q) > 15 and q.endswith('?'):
                        questions.append(q)
            questions = questions[:10]

            # Fallback sécurisé
            while len(questions) < 10:
                questions.append("Question à approfondir lors de l'entretien technique.")

            return questions[:10]

        except Exception as e:
            logger.error(f"Ollama error: {e}")
            return [f"Question {i} (erreur de génération)" for i in range(1, 11)]

    def health_check(self):
        try:
            r = requests.get(f"{self.url}/api/tags", timeout=10)
            return {"ollama_accessible": r.status_code == 200}
        except:
            return {"ollama_accessible": False}


# Instance globale
ollama = OllamaService()