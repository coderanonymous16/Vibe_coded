# ExamRAG — Product Requirements Document (PRD)

## 1. Product Overview

**Product Name:** ExamRAG  
**Type:** SaaS AI Study Assistant  
**Primary Audience:** University students, initially focused on AKTU B.Tech CSE students  
**Primary Experience:** Ask academic questions in Hinglish/Hindi/English and receive grounded answers with source citations.

ExamRAG uses Retrieval-Augmented Generation (RAG) to answer questions from trusted academic material such as:
- University syllabus
- Subject notes
- Previous Year Questions (PYQs)
- Study PDFs
- Other administrator-approved academic documents

The product must prioritize source-grounded answers instead of relying only on the LLM's internal knowledge.

---

## 2. Problem Statement

Students often have academic content spread across PDFs, notes, PYQs and syllabus documents. Finding the exact information is slow, especially when:
- The user asks questions in Hinglish.
- The same concept appears under different wording.
- Relevant information is distributed across multiple PDFs.
- Students need exam-oriented explanations.
- Students need to know where an answer came from.

ExamRAG provides a unified conversational interface over academic documents.

---

## 3. Goals

### Primary Goals

1. Provide accurate, source-grounded academic answers.
2. Support Hinglish, Hindi and English queries.
3. Provide citations for retrieved information.
4. Support hybrid retrieval using BM25 + semantic embeddings.
5. Evaluate retrieval quality using Recall@K and related metrics.
6. Support multiple users.
7. Provide an admin workflow for academic document ingestion.
8. Build the system so it can evolve into a production SaaS.

### Secondary Goals

1. Conversation history.
2. Subject/semester filtering.
3. Usage limits.
4. Analytics.
5. Subscription support.
6. Scalable document ingestion.

---

## 4. Non-Goals for V1

The first version will NOT require:

- Fine-tuning an LLM.
- Voice assistant.
- Native mobile applications.
- Multi-agent architecture.
- Kubernetes.
- Microservices.
- Autonomous web research.
- Millions of documents.
- Complex recommendation engines.

These can be considered after the core RAG system is stable.

---

## 5. Target Users

### Student

A student who wants to:
- Understand concepts.
- Search notes conversationally.
- Prepare for university exams.
- Find PYQ-related information.
- Ask questions in Hinglish.

### Administrator

An administrator who:
- Uploads academic documents.
- Organizes documents by university/course/semester/subject/unit.
- Removes outdated documents.
- Monitors ingestion status.
- Reviews system usage.

---

## 6. Core User Stories

### Authentication

- As a student, I can create an account.
- As a student, I can log in.
- As a student, I can log out.
- As a student, I can authenticate using Google OAuth.
- As a student, I can reset my password.

### Academic Discovery

- As a student, I can select university.
- As a student, I can select course.
- As a student, I can select semester.
- As a student, I can select subject.
- As a student, I can filter content by unit.

### AI Chat

- As a student, I can ask questions in English.
- As a student, I can ask questions in Hindi.
- As a student, I can ask questions in Hinglish.
- As a student, I can ask follow-up questions.
- As a student, I can start a new conversation.
- As a student, I can view previous conversations.

### Citations

- As a student, I can see which document supports an answer.
- As a student, I can see the source page number when available.
- As a student, I can distinguish between different sources.

### Admin

- As an admin, I can upload a PDF.
- As an admin, I can assign metadata.
- As an admin, I can see processing status.
- As an admin, I can delete a document.
- As an admin, I can re-index a document.

---

## 7. Functional Requirements

### FR-01 Authentication

The system must support secure user authentication.

Required capabilities:
- Registration
- Login
- Logout
- Password hashing
- JWT/session handling
- Refresh token/session renewal
- Google OAuth
- Role-based access

Roles:
- STUDENT
- ADMIN

---

### FR-02 Academic Hierarchy

The system must support:

```text
University
  └── Course
       └── Semester
            └── Subject
                 └── Unit
                      └── Documents
```

Example:

```text
AKTU
 └── B.Tech CSE
      └── Semester 6
           └── DBMS
                ├── Unit 1
                ├── Unit 2
                ├── Unit 3
                ├── Unit 4
                └── Unit 5
```

---

### FR-03 Document Management

Supported initial format:
- PDF

Document metadata should include:

```json
{
  "title": "DBMS Unit 3 Notes",
  "university": "AKTU",
  "course": "B.Tech CSE",
  "semester": 6,
  "subject": "DBMS",
  "unit": 3,
  "document_type": "notes",
  "source": "admin_upload"
}
```

Document lifecycle:

```text
UPLOADED
    ↓
PROCESSING
    ↓
CHUNKED
    ↓
EMBEDDED
    ↓
INDEXED
    ↓
READY
```

Failure state:

```text
PROCESSING_FAILED
```

---

### FR-04 PDF Ingestion

The ingestion pipeline must:

1. Receive PDF.
2. Validate file.
3. Extract text.
4. Preserve page information when possible.
5. Clean extracted text.
6. Split text into chunks.
7. Attach metadata.
8. Generate embeddings.
9. Store chunks in the vector database.
10. Update document status.

---

### FR-05 Chunking

The chunking system should support configurable:

- Chunk size.
- Chunk overlap.
- Page-aware boundaries.
- Heading-aware boundaries where possible.

Initial parameters should be configurable rather than hard-coded.

---

### FR-06 Embeddings

Each searchable chunk must have an embedding.

The embedding system should support:
- Batch embedding.
- Retry handling.
- Embedding model configuration.
- Re-indexing when the embedding model changes.

---

### FR-07 Retrieval

The system must support:

1. Semantic vector retrieval.
2. BM25 lexical retrieval.
3. Hybrid retrieval.
4. Metadata filtering.
5. Optional reranking.

Target pipeline:

```text
Query
 ↓
Query preprocessing
 ↓
BM25 retrieval
 +
Vector retrieval
 ↓
Result fusion
 ↓
Optional reranking
 ↓
Top-K context
```

---

### FR-08 Query Processing

The system should handle:

```text
English
Hindi
Hinglish
```

Examples:

```text
"What is normalization?"

"Normalization kya hota hai?"

"Normalization ko simple Hinglish me samjha."
```

The system should preserve the user's requested response style.

---

### FR-09 Answer Generation

The LLM must receive:
- User query.
- Retrieved context.
- Relevant metadata.
- Conversation context where appropriate.
- System instructions.

The model must be instructed to:
- Prefer retrieved evidence.
- Avoid unsupported claims.
- Clearly state when the answer is not available in the supplied sources.
- Provide citations.
- Match the requested language/style.

---

### FR-10 Citations

Each answer should expose supporting sources.

Example:

```text
Answer...

Sources:
[1] DBMS Notes — Unit 3 — Page 27
[2] DBMS PYQ 2025 — Page 5
```

Citation data should reference internal document/chunk identifiers.

---

### FR-11 Conversation History

The system should store:
- Conversation ID.
- User ID.
- Messages.
- Timestamps.
- Selected subject/context.

Users should be able to:
- Create conversation.
- Continue conversation.
- Rename conversation.
- Delete conversation.

---

### FR-12 Usage Tracking

The system should track:
- Number of requests.
- Token usage when available.
- Model used.
- Request latency.
- Estimated AI cost.

This enables future subscription limits.

---

### FR-13 Rate Limiting

The API must support rate limiting to prevent abuse.

Limits should be configurable by:
- IP.
- User.
- Subscription plan.

Redis should be used when the system moves beyond a single-instance deployment.

---

### FR-14 Admin Dashboard

Admin capabilities:

- Upload documents.
- View documents.
- Filter documents.
- Delete documents.
- Re-index documents.
- View ingestion failures.
- View basic usage metrics.
- Manage subjects and academic hierarchy.

---

## 8. Non-Functional Requirements

### Performance

Target:
- API response should begin quickly.
- Retrieval should generally complete within a few seconds.
- LLM latency should be measured separately from retrieval latency.

### Reliability

- Failed ingestion must not corrupt existing indexes.
- Failed LLM calls should have controlled retries.
- API errors must return predictable responses.

### Security

- Passwords must never be stored in plaintext.
- Secrets must be stored in environment variables/secrets management.
- Users must only access their own private data.
- Admin endpoints must require admin authorization.
- Uploaded files must be validated.
- API endpoints must be rate-limited.

### Scalability

The architecture should allow:
- Multiple backend instances.
- Separate ingestion workers.
- External object storage.
- Redis caching/queues.
- Database scaling.
- Vector-store migration if required.

---

## 9. Evaluation Requirements

A dedicated evaluation dataset must be maintained.

Each test item should contain:

```json
{
  "question": "2NF kya hota hai?",
  "relevant_chunk_ids": ["chunk_123", "chunk_145"]
}
```

Required retrieval metrics:

- Recall@1
- Recall@3
- Recall@5
- Recall@10
- MRR

Recommended generation metrics:

- Faithfulness
- Answer relevance
- Citation correctness

Evaluation must be repeatable after retrieval changes.

---

## 10. SaaS Requirements

Future SaaS functionality:

### Plans

Example only:

```text
FREE
PRO
PREMIUM
```

Plan limits should be configurable.

### Billing

Potential providers:
- Razorpay
- Stripe

Billing should not be tightly coupled to the RAG engine.

### Multi-Tenancy

User data must be logically isolated.

Future hierarchy:

```text
Organization
 ├── Members
 ├── Subscription
 └── Academic Data
```

---

## 11. Analytics

Track:

- Daily active users.
- Questions/day.
- Questions/user.
- Most-used subjects.
- Retrieval latency.
- LLM latency.
- Error rate.
- Token usage.
- Estimated AI cost.
- Citation click/open rate.
- User feedback.

---

## 12. MVP Acceptance Criteria

V1 is considered functional when:

1. A user can log in.
2. Admin can upload an academic PDF.
3. The PDF is successfully indexed.
4. User can select a subject.
5. User can ask a question.
6. System retrieves relevant chunks.
7. Gemini generates an answer.
8. Answer includes citations.
9. Hinglish queries work.
10. Conversation history is stored.
11. Retrieval evaluation can be executed.
12. API and frontend can be deployed.

---

## 13. Future Features

Possible post-V1 features:

- AI-generated quizzes.
- PYQ practice mode.
- Exam preparation mode.
- Unit-wise revision.
- Flashcards.
- Personalized study plans.
- Weak-topic detection.
- Automatic question generation.
- PDF highlighting.
- Citation preview.
- Voice input/output.
- Mobile app.
- Institution-specific deployments.

---

## 14. Success Metrics

Technical:

- Retrieval Recall@5.
- Citation correctness.
- Answer faithfulness.
- API error rate.
- Retrieval latency.
- LLM latency.

Product:

- Questions per active user.
- Returning users.
- Conversation completion.
- Subject usage.
- Free-to-paid conversion after billing exists.

---

## 15. Product Principle

The core principle of ExamRAG is:

> **Answer from trusted academic context first, and make the evidence visible to the student.**

The system should optimize for usefulness, traceability and reliability rather than merely producing fluent answers.
