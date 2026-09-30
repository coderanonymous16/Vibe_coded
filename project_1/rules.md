# ExamRAG — AI Coding Rules

## 1. Purpose

This file defines the rules that any AI coding assistant must follow while developing ExamRAG.

The assistant must treat:

- `PRD.md` as the product requirements source.
- `architecture.md` as the technical architecture source.
- `phase.md` as the current implementation sequence.
- `rules.md` as the development behavior and engineering rules.

If these files conflict, do not silently choose one. Explain the conflict and ask for clarification unless the current phase explicitly resolves it.

---

# 2. Core Development Principles

## Rule 1 — Build Phase by Phase

Never implement the entire application in one step.

Only implement the current phase from `phase.md`.

Do not prematurely create:
- Payment systems.
- Microservices.
- Kubernetes.
- Multi-agent systems.
- Voice systems.
- Mobile apps.
- Advanced analytics.

unless the current phase explicitly requires them.

---

## Rule 2 — Do Not Invent Requirements

Do not add product functionality merely because it seems useful.

If a requirement is not present in:
- `PRD.md`
- `architecture.md`
- `phase.md`

ask before introducing major functionality.

Small implementation details may be chosen by engineering judgment.

---

## Rule 3 — Keep the Architecture Modular

Separate:

```text
API
Service
Database
RAG
Ingestion
Authentication
Workers
Evaluation
```

Do not put business logic directly inside FastAPI route handlers.

Bad:

```python
@app.post("/chat")
def chat():
    # 200 lines of RAG/business logic
```

Preferred:

```python
@app.post("/chat")
def chat(request):
    return chat_service.process(request)
```

---

# 3. RAG Rules

## Rule 4 — RAG Must Be Source-Grounded

The system must prioritize retrieved academic context.

The LLM must not be instructed to invent an answer when evidence is unavailable.

Expected behavior:

```text
Retrieved context contains answer
        ↓
Answer using context
```

If evidence is insufficient:

```text
"I couldn't find enough information in the provided sources."
```

---

## Rule 5 — Never Fabricate Citations

Citations must come from actual retrieved chunks.

Never allow the LLM to invent:

- Document names.
- Page numbers.
- Chunk IDs.
- Source URLs.

Citation metadata must originate from the retrieval layer.

---

## Rule 6 — Preserve Metadata

Every chunk must retain useful metadata such as:

```text
document_id
source
page
university
course
semester
subject
unit
document_type
```

Do not discard metadata during chunking or retrieval.

---

## Rule 7 — Retrieval and Generation Must Be Separate

Do not tightly couple:

```text
Retriever
```

with:

```text
Gemini client
```

The retrieval layer must be testable without making an LLM request.

---

## Rule 8 — Hybrid Retrieval Must Be Experiment-Friendly

Keep these components independently configurable:

```text
BM25
Vector Search
Fusion
Reranking
Top-K
```

Do not hard-code experimental weights throughout the codebase.

---

# 4. AI Provider Rules

## Rule 9 — Isolate Gemini

Gemini-specific code should live behind a service/interface.

Do not call Gemini directly from:
- API routes.
- Database models.
- Frontend components.

Preferred:

```text
chat_service
    ↓
RAG pipeline
    ↓
generator
    ↓
Gemini provider
```

---

## Rule 10 — API Keys Are Secrets

Never hard-code:

```text
GEMINI_API_KEY
JWT_SECRET
DATABASE_PASSWORD
OAuth secrets
S3 credentials
```

Use environment variables.

Never commit `.env`.

Commit only:

```text
.env.example
```

with placeholder values.

---

# 5. Database Rules

## Rule 11 — PostgreSQL Is the Source of Application State

Use PostgreSQL for:

```text
Users
Conversations
Messages
Documents
Academic hierarchy
Subscriptions
Usage
Feedback
```

Do not use ChromaDB as the primary application database.

---

## Rule 12 — ChromaDB Is for Retrieval

ChromaDB should primarily contain:

```text
chunks
embeddings
retrieval metadata
```

Do not store critical business state only inside ChromaDB.

---

## Rule 13 — Use Migrations

Database schema changes must use Alembic migrations.

Do not manually modify production database schemas.

---

# 6. API Rules

## Rule 14 — Version APIs

Use:

```text
/api/v1/
```

Example:

```text
/api/v1/chat
/api/v1/auth/login
/api/v1/admin/documents
```

---

## Rule 15 — Validate Input

Use Pydantic schemas for request/response validation.

Do not trust frontend input.

---

## Rule 16 — Consistent Errors

Return structured errors:

```json
{
  "error": {
    "code": "DOCUMENT_NOT_READY",
    "message": "The document is still being processed."
  }
}
```

Do not expose:
- Stack traces.
- Database internals.
- API keys.
- Provider secrets.

---

# 7. Authentication and Authorization

## Rule 17 — Never Store Plaintext Passwords

Passwords must be securely hashed.

---

## Rule 18 — Enforce Authorization Server-Side

Never rely on:

```text
Frontend hiding a button
```

for security.

Every protected backend operation must verify authorization.

---

## Rule 19 — Tenant Isolation

If multi-tenancy is enabled, every private resource must have an ownership boundary.

Always verify:

```text
current_user
        ↓
resource ownership
        ↓
authorization
```

before returning or modifying private data.

---

# 8. Frontend Rules

## Rule 20 — Frontend Does Not Own Business Logic

Frontend should handle:

```text
UI
state
navigation
API interaction
presentation
```

Backend owns:

```text
authorization
RAG
usage limits
billing
data validation
business rules
```

---

## Rule 21 — Do Not Expose Secrets

Never place server-side API keys in frontend environment variables.

---

## Rule 22 — Handle Loading and Error States

Every asynchronous feature should have:

```text
Loading
Success
Empty
Error
```

states.

Chat should visibly indicate when an answer is being generated.

---

# 9. PDF/Ingestion Rules

## Rule 23 — Validate Uploaded Files

Check:

```text
file type
file size
processing status
```

Do not blindly process arbitrary uploads.

---

## Rule 24 — Ingestion Must Be Idempotent

Reprocessing the same document must not create uncontrolled duplicate chunks.

Use a stable:

```text
document_id
document version
chunk identity
```

strategy.

---

## Rule 25 — Preserve Page Information

When possible, extracted chunks should retain their source page.

This is required for useful citations.

---

# 10. Testing Rules

## Rule 26 — Test Core RAG Components

At minimum test:

```text
chunking
metadata
BM25
vector retrieval
hybrid fusion
citation construction
prompt construction
```

---

## Rule 27 — Mock External Providers

Unit tests should not depend on live Gemini calls.

Use mocks/fakes for:

```text
Gemini
embedding provider
object storage
external APIs
```

Integration tests may use controlled provider environments.

---

## Rule 28 — Do Not Ignore Test Failures

Never mark tests as passing by:
- Removing the test.
- Weakening assertions without explanation.
- Catching every exception.
- Skipping failing tests permanently.

Fix the underlying issue or document why the test is intentionally changed.

---

# 11. Evaluation Rules

## Rule 29 — Retrieval Changes Require Evaluation

When changing:

```text
chunk size
chunk overlap
embedding model
BM25 configuration
fusion weights
reranker
Top-K
```

run the retrieval evaluation.

Track:

```text
Recall@1
Recall@3
Recall@5
Recall@10
MRR
```

---

## Rule 30 — Do Not Optimize Blindly

Do not claim that a retrieval method is "better" without measurable evaluation.

Record experimental results.

---

# 12. Code Quality Rules

## Rule 31 — Prefer Simple Code

Avoid unnecessary abstractions.

Do not create a class merely because a class is possible.

---

## Rule 32 — Type Hints

Use type hints in Python code.

Example:

```python
def retrieve(
    query: str,
    top_k: int
) -> list[dict]:
    ...
```

---

## Rule 33 — Small Functions

Prefer functions with one clear responsibility.

Avoid giant files and giant functions.

---

## Rule 34 — Naming

Use descriptive names.

Preferred:

```text
hybrid_search.py
context_builder.py
document_service.py
```

Avoid:

```text
stuff.py
helper2.py
final.py
new.py
```

---

# 13. Dependency Rules

## Rule 35 — Do Not Add Dependencies Without Reason

Before adding a package:

1. Check whether the existing stack can solve the problem.
2. Check whether the package is actively maintained.
3. Add only if there is a concrete requirement.

Update:

```text
requirements.txt
```

or the project's chosen dependency file.

---

# 14. Git Rules

## Rule 36 — Small Commits

Prefer commits such as:

```text
feat: add PDF text extraction
feat: add Chroma vector store
feat: add hybrid retrieval
test: add Recall@K evaluation
fix: preserve page metadata
```

Avoid:

```text
final project
all changes
everything
```

---

## Rule 37 — Never Commit Secrets

Check before committing:

```text
.env
API keys
private credentials
tokens
database passwords
```

---

# 15. Documentation Rules

Every major subsystem should have enough documentation to explain:

```text
Purpose
Input
Output
Dependencies
Failure modes
Configuration
```

Update `README.md` when setup instructions change.

---

# 16. AI Coding Assistant Behavior

When asked to implement a phase:

1. Read the relevant PRD section.
2. Read the relevant architecture section.
3. Read the current phase in `phase.md`.
4. Inspect the existing repository.
5. Reuse existing code where appropriate.
6. Implement only the required scope.
7. Run tests.
8. Fix failures.
9. Summarize changed files.
10. Explain how to run/test the feature.

Do not rewrite unrelated working code.

---

# 17. Before Editing Existing Code

The assistant must inspect the existing implementation first.

Never blindly overwrite:

```text
configuration
database models
authentication
RAG pipeline
deployment files
```

unless the phase explicitly requires migration.

---

# 18. Definition of Done

A feature is not complete merely because code was generated.

A feature is complete when:

```text
Implementation
    +
Tests
    +
Configuration
    +
Documentation
    +
Successful local execution
```

are satisfied.

---

# 19. No Fake Completion

Never claim:

```text
"Production ready"
"Fully secure"
"Scalable to millions"
"100% accurate"
```

without evidence.

Use precise language such as:

```text
Implemented and tested locally.
```

or:

```text
Implemented the initial version; production load testing remains.
```

---

# 20. Final Rule

The assistant must optimize for:

```text
Correctness
Maintainability
Testability
Security
Traceability
Measured RAG quality
```

not for generating the maximum amount of code.

When uncertain, prefer the smallest implementation that satisfies the current phase.
