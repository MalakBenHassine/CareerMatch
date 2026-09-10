# CareerMatch — Matching RH par RAG

Moteur de matching semantique candidat-offre combinant recherche vectorielle (RAG) et LLM local, avec generation automatique de questions d'entretien personnalisees.

## Fonctionnalites

- Matching semantique candidat-offre (90% de precision de scoring)
- Generation automatique de 10 questions d'entretien personnalisees par correspondance, via Llama 3.2
- Recherche vectorielle des CV et offres via Qdrant + Sentence-Transformers
- API exposee via FastAPI, interface de demonstration en Streamlit

## Stack technique

- **Backend** : Python, FastAPI, Sentence-Transformers
- **Base vectorielle** : Qdrant
- **LLM** : Llama 3.2 via Ollama (inference locale)
- **Frontend** : Streamlit
- **Deploiement** : Docker Compose

## Architecture

```
CareerMatch/
├── backend/          # API FastAPI, logique de matching et integration LLM
├── frontend/         # Interface Streamlit
└── docker-compose.yml
```

## Lancer le projet

```bash
git clone https://github.com/MalakBenHassine/CareerMatch.git
cd CareerMatch
docker-compose up --build
```

> Un fichier `.env` d'exemple sans secrets reels est requis a la racine (voir `docker-compose.yml` pour les variables attendues : hote Qdrant, URL Ollama, modeles utilises).

## Auteure

**Malak Ben Hassine** — [LinkedIn](https://www.linkedin.com/in/malak-ben-hassine-423611353/) · [GitHub](https://github.com/MalakBenHassine)
