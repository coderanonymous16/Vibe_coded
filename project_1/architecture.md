# ExamRAG — System Architecture

## 1. Architecture Overview

ExamRAG is a SaaS-oriented Retrieval-Augmented Generation platform.

The initial architecture is a modular monolith with independently replaceable components. This avoids premature microservices while keeping clear boundaries between authentication, ingestion, retrieval, generation and SaaS functionality.

High-level architecture:

```text
                         ┌──────────────────────┐
                         │      Web Client      │
                         │   Next.js / React    │
                         └──────────┬───────────┘
                                    │ HTTPS
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         │   Authentication     │
                         │   Chat / Documents   │
                         │   Admin / Usage      │
                         └───────┬───────┬──────┘
                                 │       │
                    ┌────────────┘       └─────────────┐
                    ▼                                  ▼
             ┌──────────────┐                   ┌──────────────┐
             │ PostgreSQL   │                   │    Redis     │
             │ Users        │                   │ Cache        │
             │ Conversations│                  │ Rate limits  │
             │ Documents    │                   │ Queue        │
             │ Billing      │                   └──────────────┘
             └──────────────┘
                    │
                    │ metadata
                    ▼
             ┌─────────────────────────────────────────┐
             │                 RAG Core                │
             │                                         │
             │ Query → BM25 + Vector → Fusion → Rerank│
             │                  → Context → Gemini     │
             └───────────────┬──────────────┬──────────┘
                             │              │
                             ▼              ▼
                      ┌────────────┐   ┌──────────────┐
                      │ ChromaDB   │   │ Gemini API   │
                      │ Vectors    │   │ LLM + Embed  │
                      └────────────┘   └──────────────┘
                             ▲
                             │
                      ┌──────┴───────┐
                      │  Ingestion   │
                      │ PDF → chunks │
                      │ → embeddings │
                      └──────┬───────┘
                             │
                             ▼
                      ┌──────────────┐
                      │ Object Store │
                      │ PDF files    │
                      │ S3-compatible│
                      └──────────────┘
```

---

## 2. Architectural Principles

1. Modular design.
2. API-first backend.
3. Source-grounded generation.
4. Metadata-aware retrieval.
5. Replaceable model providers.
6. Configuration through environment variables.
7. Stateless API instances where possible.
8. Persistent state in databases/object storage.
9. Background processing for expensive ingestion.
10. Observability from the beginning.
11. Security by default.
12. Avoid premature microservices.

---

## 3. Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + TypeScript |
| UI | React |
| Backend | Python + FastAPI |
| Validation | Pydantic |
| Relational DB | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Vector Store | ChromaDB |
| Lexical Retrieval | BM25 |
| LLM | Gemini API |
| Embeddings | Configurable embedding provider |
| Cache | Redis |
| Background Jobs | Celery/RQ or equivalent |
| File Storage | S3-compatible object storage |
| Containers | Docker |
| CI/CD | GitHub Actions |
| Monitoring | Sentry + structured logs |

---

## 4. Repository Structure

```text
examrag/
│
├── frontend/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── services/
│   ├── types/
│   └── public/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── documents.py
│   │   │   ├── subjects.py
│   │   │   ├── users.py
│   │   │   ├── admin.py
│   │   │   └── health.py
│   │   │
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── logging.py
│   │   │   └── exceptions.py
│   │   │
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   ├── models/
│   │   │   └── migrations/
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── document.py
│   │   │   └── user.py
│   │   │
│   │   ├── rag/
│   │   │   ├── chunker.py
│   │   │   ├── embeddings.py
│   │   │   ├── vector_store.py
│   │   │   ├── bm25.py
│   │   │   ├── hybrid_search.py
│   │   │   ├── reranker.py
│   │   │   ├── retriever.py
│   │   │   ├── context_builder.py
│   │   │   ├── prompts.py
│   │   │   ├── generator.py
│   │   │   └── pipeline.py
│   │   │
│   │   ├── ingestion/
│   │   │   ├── pdf_loader.py
│   │   │   ├── pdf_parser.py
│   │   │   ├── text_cleaner.py
│   │   │   ├── metadata.py
│   │   │   └── ingestion_pipeline.py
│   │   │
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── chat_service.py
│   │   │   ├── document_service.py
│   │   │   ├── usage_service.py
│   │   │   └── billing_service.py
│   │   │
│   │   └── workers/
│   │       └── ingestion_worker.py
│   │
│   ├── tests/
│   │   ├── test_auth.py
│   │   ├── test_ingestion.py
│   │   ├── test_retrieval.py
│   │   ├── test_rag.py
│   │   └── test_api.py
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── evaluation/
│
├── evaluation/
│   ├── questions.json
│   ├── ground_truth.json
│   ├── evaluate_recall.py
│   └── evaluate_rag.py
│
├── scripts/
│   ├── ingest.py
│   ├── reindex.py
│   └── seed.py
│
├── docker-compose.yml
├── .gitignore
├── README.md
└── LICENSE
```

---

# 5. Backend Layers

## API Layer

Responsible for:
- HTTP requests.
- Authentication dependencies.
- Request validation.
- Response serialization.
- HTTP status codes.

It should NOT contain the RAG implementation directly.

---

## Service Layer

Responsible for business logic.

Examples:

```text
chat_service.py
document_service.py
auth_service.py
usage_service.py
billing_service.py
```

---

## RAG Layer

Responsible only for retrieval and generation.

The main pipeline:

```text
User Query
    ↓
Query preprocessing
    ↓
Metadata filters
    ↓
BM25 retrieval
    +
Vector retrieval
    ↓
Hybrid fusion
    ↓
Reranking
    ↓
Context builder
    ↓
Prompt construction
    ↓
Gemini
    ↓
Answer + citations
```

---

# 6. PDF Ingestion Architecture

```text
Admin Upload
     │
     ▼
FastAPI
     │
     ├── Validate
     │
     ▼
Object Storage
     │
     ▼
Document DB record
     │
     ▼
Background Job
     │
     ▼
PDF Parser
     │
     ▼
Text Cleaning
     │
     ▼
Chunking
     │
     ▼
Metadata Attachment
     │
     ▼
Embedding Generation
     │
     ▼
ChromaDB
     │
     ▼
Document status = READY
```

Ingestion should be idempotent.

A re-index operation should not create duplicate chunks.

---

# 7. Chunk Data Model

Each chunk should conceptually contain:

```json
{
  "chunk_id": "uuid",
  "document_id": "uuid",
  "text": "Normalization is...",
  "embedding": "...",
  "metadata": {
    "university": "AKTU",
    "course": "B.Tech CSE",
    "semester": 6,
    "subject": "DBMS",
    "unit": 3,
    "document_type": "notes",
    "page": 27,
    "source": "DBMS Notes.pdf"
  }
}
```

The actual embedding should be stored according to the vector-store implementation rather than duplicated in PostgreSQL.

---

# 8. Retrieval Architecture

## 8.1 Vector Retrieval

```text
Question
   ↓
Embedding model
   ↓
Query vector
   ↓
ChromaDB
   ↓
Top-K semantic results
```

---

## 8.2 BM25 Retrieval

```text
Question
   ↓
Tokenization
   ↓
BM25 index
   ↓
Top-K lexical results
```

BM25 is useful for:
- Exact technical terms.
- Acronyms.
- Course terminology.
- Numbers.
- Named protocols.
- Specific definitions.

---

## 8.3 Hybrid Retrieval

```text
                 Query
                   │
           ┌───────┴────────┐
           ▼                ▼
        BM25             Vector
           │                │
           ▼                ▼
       Top-K lexical    Top-K semantic
           │                │
           └───────┬────────┘
                   ▼
              Score Fusion
                   ▼
              Candidate Set
                   ▼
                Reranker
                   ▼
                Top-K
```

The fusion algorithm should be isolated so that weighting strategies can be evaluated independently.

---

# 9. Reranking

Reranking is optional in the first prototype.

Production pipeline:

```text
BM25 + Vector
      ↓
20–50 candidates
      ↓
Reranker
      ↓
Top 5–10
      ↓
Context builder
```

The reranker should not be coupled to the Gemini generation client.

---

# 10. Context Construction

The context builder should:

1. Select final chunks.
2. Remove duplicates.
3. Preserve source metadata.
4. Respect context limits.
5. Format citations.
6. Maintain chunk ordering where useful.

Example internal context:

```text
[SOURCE 1]
Document: DBMS Unit 3 Notes
Page: 27
Unit: 3

Content:
...

[SOURCE 2]
Document: DBMS PYQ 2025
Page: 5

Content:
...
```

---

# 11. Generation Architecture

The generator should expose an abstraction similar to:

```text
generate_answer(
    query,
    context,
    conversation_history,
    response_language
)
```

The implementation can call Gemini.

The application should avoid embedding Gemini-specific logic throughout the codebase.

This makes future model changes easier.

---

# 12. Prompt Architecture

Prompt layers:

```text
System instructions
        +
Academic grounding rules
        +
Citation rules
        +
Language/style instructions
        +
Retrieved context
        +
Conversation history
        +
Current user query
```

Core rule:

```text
Use supplied context as the primary source of truth.
Do not fabricate citations.
If the supplied context does not contain enough information,
say that the information is not available in the provided sources.
```

---

# 13. Citation Architecture

Citations should be generated from retrieval metadata, not invented by the LLM.

Recommended internal representation:

```json
{
  "citation_id": "src_1",
  "document_id": "doc_123",
  "chunk_id": "chunk_456",
  "title": "DBMS Unit 3 Notes",
  "page": 27
}
```

The frontend can render:

```text
[1] DBMS Unit 3 Notes — Page 27
```

The LLM should reference known citation IDs.

---

# 14. PostgreSQL Data Model

Core entities:

```text
User
Organization
Subscription
University
Course
Semester
Subject
Unit
Document
Conversation
Message
UsageRecord
Feedback
```

Relationships:

```text
Organization
 ├── Users
 └── Subscription

University
 └── Course
      └── Semester
           └── Subject
                └── Unit
                     └── Document

User
 └── Conversation
      └── Message

Message
 └── Citations
```

---

# 15. ChromaDB Data Model

Collection strategy should be configurable.

Possible initial approach:

```text
examrag_chunks
```

Use metadata filters:

```text
university
course
semester
subject
unit
document_id
document_type
```

Do not create an excessive number of collections unnecessarily.

---

# 16. Object Storage

Original PDFs should be stored outside PostgreSQL.

Example:

```text
bucket/
  universities/
    aktu/
      btech-cse/
        semester-6/
          dbms/
            documents/
              document-id.pdf
```

Database stores the object key and metadata.

---

# 17. Authentication Architecture

```text
Client
  ↓
Login
  ↓
Auth service
  ↓
Verify credentials/OAuth
  ↓
Session/JWT
  ↓
Protected API
```

Password storage:

```text
Plain password
     ↓
Secure password hashing
     ↓
Database
```

Never store plaintext passwords.

---

# 18. Authorization

Use role-based access control.

Example:

```text
STUDENT
 ├── Read academic content
 ├── Chat
 ├── Manage own conversations
 └── View own usage

ADMIN
 ├── All student permissions
 ├── Upload documents
 ├── Delete documents
 ├── Manage academic hierarchy
 └── View admin analytics
```

---

# 19. Multi-Tenancy

For SaaS evolution, all tenant-owned resources should have an ownership boundary.

Example:

```text
organization_id
user_id
```

Authorization checks must happen before returning private data.

The application must never rely only on frontend filtering for isolation.

---

# 20. Redis Architecture

Redis can provide:

### Rate Limiting

```text
user:{id}:requests
```

### Cache

Possible future cache:

```text
query_hash → response
```

Caching must be carefully designed so private/user-specific answers are not leaked.

### Background Queue

Redis can act as a broker for ingestion jobs if Celery/RQ is selected.

---

# 21. API Design

Initial endpoints:

## Auth

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/logout
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

## Chat

```text
POST /api/v1/chat
GET  /api/v1/conversations
GET  /api/v1/conversations/{id}
PATCH /api/v1/conversations/{id}
DELETE /api/v1/conversations/{id}
```

## Academic

```text
GET /api/v1/universities
GET /api/v1/courses
GET /api/v1/semesters
GET /api/v1/subjects
GET /api/v1/subjects/{id}/documents
```

## Admin

```text
POST /api/v1/admin/documents
GET /api/v1/admin/documents
GET /api/v1/admin/documents/{id}
DELETE /api/v1/admin/documents/{id}
POST /api/v1/admin/documents/{id}/reindex
```

## Health

```text
GET /health
GET /ready
```

API versioning should use:

```text
/api/v1/
```

---

# 22. Chat Request Flow

```text
POST /api/v1/chat
        │
        ▼
Authenticate user
        │
        ▼
Validate request
        │
        ▼
Check usage/rate limit
        │
        ▼
Resolve academic filters
        │
        ▼
Retrieve BM25 results
        │
        ▼
Retrieve vector results
        │
        ▼
Fuse results
        │
        ▼
Rerank
        │
        ▼
Build context
        │
        ▼
Call Gemini
        │
        ▼
Validate citations
        │
        ▼
Store message + usage
        │
        ▼
Return answer
```

---

# 23. Error Handling

Standard error structure:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_READY",
    "message": "The requested document is still being processed."
  }
}
```

Important error categories:

```text
AUTHENTICATION_ERROR
AUTHORIZATION_ERROR
VALIDATION_ERROR
RATE_LIMITED
DOCUMENT_NOT_FOUND
DOCUMENT_NOT_READY
INGESTION_FAILED
RETRIEVAL_FAILED
LLM_PROVIDER_ERROR
INTERNAL_ERROR
```

Do not expose stack traces to users.

---

# 24. Observability

Track:

```text
request_id
user_id
endpoint
status_code
latency
retrieval_latency
LLM_latency
model
token_usage
error_code
```

RAG-specific logs:

```text
query
filters
retrieved_chunk_ids
retrieval_scores
final_chunk_ids
model
```

Avoid logging sensitive user content unnecessarily.

---

# 25. Evaluation Architecture

Evaluation is independent of production chat.

```text
Evaluation Dataset
       │
       ▼
Retriever
       │
       ▼
Retrieved IDs
       │
       ▼
Compare with Ground Truth
       │
       ▼
Recall@K / MRR
```

Generation evaluation:

```text
Question
   ↓
RAG
   ↓
Answer + citations
   ↓
Evaluation framework
   ↓
Faithfulness
Answer relevance
Citation correctness
```

---

# 26. Evaluation Dataset Structure

```json
{
  "id": "q001",
  "question": "2NF kya hota hai?",
  "subject": "DBMS",
  "unit": 3,
  "relevant_chunk_ids": [
    "chunk_123",
    "chunk_456"
  ],
  "expected_concepts": [
    "partial dependency",
    "1NF"
  ]
}
```

---

# 27. Deployment Architecture

Initial deployment:

```text
Internet
   │
   ▼
Frontend
   │
   ▼
FastAPI
   │
   ├── PostgreSQL
   ├── Redis
   ├── ChromaDB
   ├── Object Storage
   └── Gemini API
```

Docker:

```text
docker-compose.yml

services:
  frontend
  backend
  postgres
  redis
  chromadb
```

For production, managed PostgreSQL/Redis/object storage can replace local containers.

---

# 28. CI/CD

GitHub workflow:

```text
Developer
   ↓
Git push
   ↓
GitHub Actions
   ↓
Lint
   ↓
Unit tests
   ↓
Integration tests
   ↓
Docker build
   ↓
Deploy
```

Pull requests should run tests before merging.

---

# 29. Security Checklist

- HTTPS in production.
- Secure password hashing.
- Secret management.
- JWT/session security.
- CORS configuration.
- Rate limiting.
- Input validation.
- File type validation.
- File size limits.
- Admin authorization.
- SQL injection protection through ORM/parameterized queries.
- Safe error responses.
- Dependency vulnerability scanning.
- No secrets committed to Git.
- User/tenant authorization checks.
- Secure object-storage access.

---

# 30. Scaling Strategy

## Stage 1 — Prototype

```text
One backend
One PostgreSQL
One ChromaDB
One Redis
```

## Stage 2 — Growing SaaS

```text
Multiple API instances
      +
Managed PostgreSQL
      +
Managed Redis
      +
Dedicated ingestion workers
      +
Object storage
```

## Stage 3 — Large Scale

Potentially separate:

```text
API service
Auth service
Ingestion workers
Retrieval service
AI generation service
Analytics pipeline
```

Do NOT split into microservices until operational requirements justify it.

---

# 31. Cost Control

Track:

```text
requests/user
input tokens
output tokens
embedding usage
retrieval latency
estimated model cost
```

Apply:

```text
plan limits
rate limits
context limits
maximum output tokens
caching where safe
batch embeddings
```

---

# 32. Configuration

Use environment variables.

Example:

```text
APP_ENV=
DATABASE_URL=
REDIS_URL=
CHROMA_HOST=
CHROMA_PORT=

GEMINI_API_KEY=
GEMINI_MODEL=
EMBEDDING_MODEL=

JWT_SECRET=
JWT_EXPIRY=

S3_ENDPOINT=
S3_BUCKET=
S3_ACCESS_KEY=
S3_SECRET_KEY=

GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

SENTRY_DSN=
```

Never commit `.env`.

Commit:

```text
.env.example
```

---

# 33. Testing Strategy

### Unit Tests

Test:
- Chunking.
- Metadata.
- BM25.
- Fusion.
- Citation formatting.
- Prompt construction.
- Authentication utilities.

### Integration Tests

Test:

```text
PDF → ingestion → ChromaDB
Question → retrieval → Gemini mock
API → database
```

### End-to-End

Test:

```text
Login
 ↓
Select subject
 ↓
Ask question
 ↓
Receive answer
 ↓
View citation
```

### Evaluation Tests

Run retrieval benchmark after changes to:
- Chunking.
- Embeddings.
- BM25.
- Fusion.
- Reranking.

---

# 34. Architectural Decision

For V1:

```text
Modular Monolith
```

not:

```text
Microservices
```

Reason:

- Faster development.
- Easier debugging.
- Lower deployment complexity.
- Clear module boundaries can later become services.
- Appropriate for an early SaaS product.

---

# 35. RAG Core Interface

The application should conceptually expose:

```python
class RAGPipeline:
    def answer(
        self,
        query: str,
        filters: dict,
        conversation_history: list
    ):
        ...
```

Internal components:

```text
Retriever
HybridSearch
Reranker
ContextBuilder
PromptBuilder
Generator
CitationBuilder
```

This separation makes experiments easier.

---

# 36. Definition of Done — Architecture

The architecture is ready for V1 when:

- Frontend can communicate with FastAPI.
- Authentication works.
- PostgreSQL stores application state.
- PDFs can be stored and ingested.
- ChromaDB stores searchable chunks.
- BM25 retrieval works.
- Vector retrieval works.
- Hybrid retrieval works.
- Gemini generation works.
- Citations are generated from retrieved metadata.
- Conversations are persisted.
- Evaluation can calculate Recall@K.
- Docker can run the core stack.
- Secrets are externalized.
- Tests exist for core RAG components.

---

# 37. Future Extension Points

The architecture should allow future addition of:

```text
Quiz Engine
PYQ Generator
Flashcards
Study Planner
Voice
OCR
Multimodal PDFs
Personalized Recommendations
Institutional SaaS
Billing
Advanced Analytics
Alternative LLM Providers
Alternative Vector Databases
```

These should be added as modules rather than forcing major changes to the core RAG pipeline.
