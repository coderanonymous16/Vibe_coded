# ExamRAG

ExamRAG is a SaaS-oriented academic RAG platform built for university students, starting with AKTU B.Tech CSE support and Hinglish/Hindi/English queries.

## Current implementation status

This repository is being built in phases based on the project specification stored in the repository documentation files.

Current active phase:
- Phase 16–20: frontend shell, admin scaffolding, queueing, rate limiting, and usage tracking

## Structure

- `backend/` — FastAPI application and Python services
- `frontend/` — Next.js frontend (scaffold placeholder)
- `data/` — raw/processed data and evaluation sets
- `scripts/` — utility scripts
- `evaluation/` — retrieval evaluation assets

## Local backend startup

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Health endpoint

```bash
curl http://localhost:8000/api/v1/health
```

## Environment

Copy `.env.example` or `backend/.env.example` and update values before running large integrations.
