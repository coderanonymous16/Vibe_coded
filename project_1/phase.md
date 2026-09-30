# ExamRAG — Implementation Phases

## How to Use This File

ExamRAG must be developed sequentially.

The AI coding assistant must work on **one phase at a time**.

Do not jump to later phases unless explicitly requested.

Each phase has:
- Goal
- Scope
- Deliverables
- Files
- Tests
- Exit criteria

---

# Phase 0 — Project Foundation

## Goal

Create a clean repository and development environment.

## Tasks

- Initialize Git repository.
- Create backend directory.
- Create frontend directory.
- Create documentation files.
- Configure Python environment.
- Configure `.gitignore`.
- Create `.env.example`.
- Create basic README.
- Configure formatting/linting.

## Initial Structure

```text
examrag/
├── backend/
├── frontend/
├── data/
├── evaluation/
├── scripts/
├── PRD.md
├── architecture.md
├── rules.md
├── phase.md
├── README.md
├── .gitignore
└── .env.example
```

## Exit Criteria

- Repository runs locally.
- Python environment works.
- Git is configured.
- No secrets are committed.

---

# Phase 1 — FastAPI Backend Skeleton

## Goal

Create the backend API foundation.

## Tasks

- Create FastAPI application.
- Add `/health`.
- Add configuration management.
- Add environment loading.
- Add structured error handling.
- Add API versioning.
- Add basic logging.

## Required Files

```text
backend/app/main.py
backend/app/core/config.py
backend/app/core/logging.py
backend/app/core/exceptions.py
backend/app/api/health.py
```

## Exit Criteria

```text
GET /health
```

returns a successful response.

---

# Phase 2 — PostgreSQL + Database Layer

## Goal

Create persistent application state.

## Tasks

Set up:

```text
PostgreSQL
SQLAlchemy
Alembic
```

Initial models:

```text
User
University
Course
Semester
Subject
Unit
Document
```

## Exit Criteria

- Database connects.
- Migrations work.
- Tables can be created.
- Tests can use a test database.

---

# Phase 3 — PDF Ingestion

## Goal

Convert academic PDFs into clean, page-aware text.

## Pipeline

```text
PDF
 ↓
Extraction
 ↓
Cleaning
 ↓
Page-aware text
 ↓
Chunks
```

## Tasks

Implement:

```text
pdf_loader.py
pdf_parser.py
text_cleaner.py
chunker.py
```

## Output

Each chunk should contain:

```text
chunk_id
text
page
document_id
metadata
```

## Exit Criteria

Given a test PDF:

```text
PDF → chunks
```

works reliably and preserves page metadata.

---

# Phase 4 — Embeddings + ChromaDB

## Goal

Create semantic retrieval.

## Tasks

- Configure embedding provider.
- Generate embeddings.
- Create ChromaDB collection.
- Store chunks.
- Store metadata.
- Implement similarity search.

## Pipeline

```text
Chunk
 ↓
Embedding
 ↓
ChromaDB
```

## Exit Criteria

A query can retrieve semantically relevant chunks.

---

# Phase 5 — First Working RAG

## Goal

Build the simplest complete RAG pipeline.

## Pipeline

```text
Question
 ↓
Vector Search
 ↓
Top-K chunks
 ↓
Context
 ↓
Gemini
 ↓
Answer
```

## Tasks

Create:

```text
retriever.py
context_builder.py
prompts.py
generator.py
pipeline.py
```

## Requirements

- Ground answer in retrieved context.
- Do not fabricate unsupported facts.
- Handle insufficient context.
- Return source metadata.

## Exit Criteria

A real academic question receives a grounded answer.

---

# Phase 6 — Citations

## Goal

Make answers traceable.

## Tasks

- Preserve document/page metadata.
- Create citation objects.
- Return citations with answer.
- Ensure citations originate from retrieval results.

## Example

```text
Answer...

Sources:
[1] DBMS Notes — Page 27
[2] DBMS PYQ 2025 — Page 5
```

## Exit Criteria

Every source-grounded answer can identify its supporting chunks.

---

# Phase 7 — Hinglish Support

## Goal

Support natural Hinglish/Hindi/English queries.

## Test Queries

```text
What is normalization?

Normalization kya hota hai?

Normalization ko simple Hinglish me samjha.

2NF ko exam ke perspective se explain karo.
```

## Requirements

- Query language should not break retrieval.
- Response should follow requested style.
- Technical terms should remain accurate.

## Exit Criteria

The same academic concept can be queried naturally in multiple languages.

---

# Phase 8 — BM25 Retrieval

## Goal

Add lexical retrieval.

## Pipeline

```text
Query
 ↓
BM25
 ↓
Top-K lexical results
```

## Tasks

- Build BM25 index.
- Tokenize documents appropriately.
- Support index refresh/rebuild.
- Return normalized retrieval results.

## Exit Criteria

Exact terms and technical keywords are retrieved reliably.

---

# Phase 9 — Hybrid Retrieval

## Goal

Combine semantic and lexical retrieval.

## Pipeline

```text
              Query
             /     \
            ↓       ↓
          BM25    Vector
            ↓       ↓
            └───┬───┘
                ↓
             Fusion
                ↓
             Top-K
```

## Tasks

- Combine candidate sets.
- Implement configurable fusion.
- Keep retrieval scores.
- Remove duplicate chunks.
- Preserve metadata.

## Exit Criteria

Hybrid retrieval can be benchmarked independently against:
- BM25 only.
- Vector only.
- Hybrid.

---

# Phase 10 — Reranking

## Goal

Improve ordering of retrieved candidates.

## Pipeline

```text
BM25 + Vector
      ↓
Candidates
      ↓
Reranker
      ↓
Final Top-K
```

## Tasks

- Add reranker interface.
- Keep reranker replaceable.
- Evaluate before/after performance.

## Exit Criteria

Reranking results are measurable through the evaluation framework.

---

# Phase 11 — Retrieval Evaluation

## Goal

Measure RAG retrieval instead of guessing.

## Dataset

Create:

```text
evaluation/questions.json
evaluation/ground_truth.json
```

## Metrics

Required:

```text
Recall@1
Recall@3
Recall@5
Recall@10
MRR
```

## Experiments

Compare:

```text
Vector
BM25
Hybrid
Hybrid + Reranker
```

## Exit Criteria

Running one command produces reproducible evaluation results.

---

# Phase 12 — Chat API

## Goal

Expose the RAG pipeline through FastAPI.

## Endpoints

```text
POST /api/v1/chat

GET /api/v1/conversations

GET /api/v1/conversations/{id}

PATCH /api/v1/conversations/{id}

DELETE /api/v1/conversations/{id}
```

## Requirements

- Request validation.
- Authentication dependency placeholder if auth is not yet implemented.
- Error handling.
- RAG execution.
- Citation response.
- Latency logging.

## Exit Criteria

The complete RAG system can be used through an API.

---

# Phase 13 — Authentication

## Goal

Add secure user accounts.

## Features

- Registration.
- Login.
- Logout.
- Password hashing.
- Session/JWT handling.
- Google OAuth.
- Role support.

## Roles

```text
STUDENT
ADMIN
```

## Exit Criteria

Protected endpoints reject unauthenticated users.

---

# Phase 14 — Conversation Persistence

## Goal

Store chat history.

## Models

```text
Conversation
Message
Citation
```

## Pipeline

```text
User
 ↓
Question
 ↓
RAG
 ↓
Answer
 ↓
Persist
```

## Exit Criteria

Users can leave and return to a conversation.

---

# Phase 15 — Academic Filtering

## Goal

Make retrieval context-aware.

Support filters:

```text
University
Course
Semester
Subject
Unit
Document Type
```

Example:

```text
semester = 6
subject = DBMS
unit = 3
```

should limit retrieval to relevant academic content.

## Exit Criteria

Metadata filtering works in both lexical and vector retrieval.

---

# Phase 16 — Frontend MVP

## Goal

Build the student-facing web interface.

## Pages

```text
/
 /login
 /register
 /dashboard
 /subjects
 /chat
 /settings
```

## Chat Features

- Message list.
- Input box.
- Loading state.
- Error state.
- Citations.
- Conversation history.
- Subject context.

## Exit Criteria

A student can complete:

```text
Login
 ↓
Select subject
 ↓
Ask question
 ↓
Receive answer
 ↓
Open citation
```

---

# Phase 17 — Admin Dashboard

## Goal

Allow administrators to manage academic content.

## Features

- Upload PDF.
- Add metadata.
- View processing status.
- Delete document.
- Re-index document.
- View ingestion errors.
- Manage subjects.

## Exit Criteria

Admin can manage the complete document lifecycle without directly accessing the database.

---

# Phase 18 — Background Ingestion

## Goal

Move expensive PDF processing out of the request cycle.

## Pipeline

```text
Upload
 ↓
Create document
 ↓
Queue job
 ↓
Worker
 ↓
Parse
 ↓
Chunk
 ↓
Embed
 ↓
Index
 ↓
READY
```

## Technology

Possible:

```text
Redis + Celery
```

or:

```text
Redis + RQ
```

Choose one.

## Exit Criteria

Large documents do not block API requests.

---

# Phase 19 — Redis + Rate Limiting

## Goal

Protect the SaaS backend.

Implement:

```text
User rate limit
IP rate limit
Plan-based request limit
```

Also prepare Redis for:

```text
Caching
Background queues
```

## Exit Criteria

Excessive requests are rejected safely.

---

# Phase 20 — Usage and Cost Tracking

## Goal

Understand SaaS AI costs.

Track:

```text
user_id
request_id
model
input_tokens
output_tokens
estimated_cost
timestamp
latency
```

## Exit Criteria

Admin can calculate:

```text
AI cost/day
AI cost/month
cost/user
requests/user
```

---

# Phase 21 — SaaS Subscription Layer

## Goal

Introduce paid plans.

Example:

```text
FREE
PRO
PREMIUM
```

Plan configuration should control:

```text
monthly requests
daily requests
features
```

Payment provider can be:

```text
Razorpay
```

or:

```text
Stripe
```

## Exit Criteria

Subscription state is stored independently from the RAG engine.

---

# Phase 22 — Object Storage

## Goal

Move uploaded PDFs to durable cloud storage.

Store:

```text
PDF
 ↓
Object Storage
```

Database stores:

```text
object_key
document metadata
status
```

## Exit Criteria

PDFs survive backend restarts and can be securely retrieved.

---

# Phase 23 — Production Hardening

## Goal

Make the system deployment-ready.

Implement:

- Secure CORS.
- HTTPS.
- Proper secrets management.
- Health checks.
- Readiness checks.
- Structured logging.
- Error monitoring.
- Database backups.
- File validation.
- Dependency updates.
- Security checks.

## Exit Criteria

No known critical configuration/security issue remains.

---

# Phase 24 — Docker

## Goal

Containerize the application.

Services:

```text
frontend
backend
postgres
redis
chromadb
```

Development:

```text
docker-compose.yml
```

## Exit Criteria

Core stack can start using Docker.

---

# Phase 25 — CI/CD

## Goal

Automate testing and deployment.

Pipeline:

```text
Git Push
 ↓
Lint
 ↓
Unit Tests
 ↓
Integration Tests
 ↓
Build
 ↓
Deploy
```

## Exit Criteria

A valid main-branch change passes automated checks before deployment.

---

# Phase 26 — Observability

## Goal

Monitor the production system.

Track:

```text
API latency
RAG latency
LLM latency
Error rate
Token usage
AI cost
Retrieval metrics
Ingestion failures
```

Use an error monitoring system such as Sentry.

---

# Phase 27 — Production RAG Evaluation

## Goal

Continuously measure retrieval and answer quality.

Maintain a fixed benchmark.

Every major RAG change should compare:

```text
Before
vs
After
```

Metrics:

```text
Recall@K
MRR
Faithfulness
Answer relevance
Citation correctness
Latency
Cost
```

---

# Phase 28 — V1 Release

## V1 Must Include

```text
Authentication
Academic hierarchy
PDF ingestion
Embeddings
ChromaDB
BM25
Hybrid retrieval
Reranking
Gemini generation
Hinglish support
Citations
Conversation history
FastAPI
Frontend
Admin dashboard
Evaluation
Rate limiting
Usage tracking
Docker
Production deployment
```

## V1 Should NOT Require

```text
Mobile app
Voice
Multi-agent architecture
Kubernetes
Complex recommendation engine
Fine-tuning
```

---

# Phase 29 — Post-V1 Features

Only after V1 is stable:

```text
AI Quiz Generator
PYQ Practice Mode
Flashcards
Study Planner
Personalized Revision
Weak Topic Detection
OCR
Multimodal PDFs
Voice
Mobile Application
Institutional SaaS
Advanced Analytics
```

---

# Phase Completion Protocol

At the end of every phase, the AI coding assistant must report:

## 1. Implemented

List exactly what was built.

## 2. Files Changed

List created/modified files.

## 3. Tests

List tests executed and results.

## 4. Configuration

List new environment variables or configuration.

## 5. Known Issues

List unresolved issues.

## 6. Next Phase

State the next phase but do not implement it automatically.

---

# Phase Rules

The assistant must NOT:

- Skip evaluation because the feature appears to work.
- Implement multiple major phases together.
- Rewrite unrelated code.
- Remove tests to make a build pass.
- Hard-code secrets.
- Claim production readiness without testing.
- Add unrequested major dependencies.
- Introduce microservices prematurely.

The assistant MAY:

- Refactor code required by the current phase.
- Fix bugs discovered during the current phase.
- Add unit tests required by the current phase.
- Improve error handling required by the current phase.
- Update documentation affected by implementation.

---

# Recommended Build Milestone

The most important milestone is:

```text
Phase 1–7
     ↓
First reliable RAG prototype
     ↓
Phase 8–11
     ↓
Strong retrieval + measurable evaluation
     ↓
Phase 12–17
     ↓
Usable multi-user product
     ↓
Phase 18–26
     ↓
SaaS + production infrastructure
     ↓
Phase 27–29
     ↓
Production-quality ExamRAG
```
