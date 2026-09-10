# CareerMatch — RAG-based HR Matching

Semantic candidate-to-job matching engine combining vector search (RAG) and a local LLM, with automatic generation of personalized interview questions.

## Features

- Semantic candidate-to-job matching (90% scoring accuracy)
- Automatic generation of 10 personalized interview questions per match, via Llama 3.2
- Vector search over resumes and job postings via Qdrant + Sentence-Transformers
- API exposed via FastAPI, demo interface in Streamlit

## Tech stack

- **Backend**: Python, FastAPI, Sentence-Transformers
- **Vector database**: Qdrant
- **LLM**: Llama 3.2 via Ollama (local inference)
- **Frontend**: Streamlit
- **Deployment**: Docker Compose

## Architecture

```
CareerMatch/
├── backend/          # FastAPI API, matching logic and LLM integration
├── frontend/         # Streamlit interface
└── docker-compose.yml
```

## Running the project

```bash
git clone https://github.com/MalakBenHassine/CareerMatch.git
cd CareerMatch
cp .env.example .env
docker-compose up --build
```

> Copy `.env.example` to `.env` before starting (see `docker-compose.yml` for the expected variables: Qdrant host, Ollama URL, models used). No real secrets are required — these are local service settings.

## Author

**Malak Ben Hassine** — [LinkedIn](https://www.linkedin.com/in/malak-ben-hassine-423611353/) · [GitHub](https://github.com/MalakBenHassine)
