# ExamRAG — Memory Specification

## 1. Purpose

This document defines how ExamRAG handles conversational memory.

Current implementation note: the project is now in a working demo phase. The backend is running, the RAG chat is live with seeded academic content, and the frontend can authenticate using a seeded demo student account. The remaining work is product polish, persistent user history, and stronger production-grade integrations rather than a blank static page. This keeps memory and RAG boundaries explicit while the product matures.

Current demo account:
- Email: student@example.com
- Password: secret123

This demo account exists so the app can be tested immediately without manual setup and to make the app feel usable during the scaffold phase. It is not treated as a production identity system.

Memory must improve continuity without compromising:
- Privacy.
- Security.
- User control.
- Retrieval accuracy.
- Cost control.

Memory is divided into:

```text
Conversation Memory
User Preferences
Academic Context
Long-Term Memory
```

These must not be treated as the same thing.

---

# 2. Core Principle

ExamRAG should remember only information that improves the user's academic experience and that the product is designed to retain.

The system should not store every message indefinitely as "memory".

---

# 3. Memory Types

## 3.1 Conversation Memory

Short-term context belonging to a conversation.

Example:

```text
User:
Explain normalization.

AI:
...

User:
Now explain 2NF.

```

The second query may depend on the first response.

Conversation memory includes:

```text
conversation_id
recent messages
selected subject
selected unit
retrieved context where appropriate
```

---

## 3.2 User Preferences

Optional persistent preferences.

Examples:

```text
preferred response language = Hinglish
preferred explanation style = simple
preferred answer length = detailed
```

Only store preferences that are useful to the product.

---

## 3.3 Academic Context

Temporary or persistent academic context such as:

```text
selected university
course
semester
subject
unit
```

Example:

```text
Current context:
University = AKTU
Course = B.Tech CSE
Semester = 6
Subject = DBMS
Unit = 3
```

Academic context should be used to improve retrieval.

---

## 3.4 Long-Term Memory

Long-term memory should be introduced only after the basic system works.

Potential examples:

```text
Frequently studied subjects
Preferred explanation style
Frequently requested topics
```

Do not automatically store sensitive or unnecessary personal information.

---

# 4. What Should NOT Be Stored as Long-Term Memory

Do not persist arbitrary user content merely because it appeared in a conversation.

Do not automatically store:

```text
Passwords
API keys
Authentication tokens
Payment credentials
Private secrets
Unnecessary personal information
Sensitive information unrelated to academic functionality
```

Do not infer personal attributes from conversations and store them as facts.

---

# 5. Conversation Storage

Recommended database entities:

```text
Conversation
Message
Citation
```

Conversation:

```text
id
user_id
title
subject_id
created_at
updated_at
```

Message:

```text
id
conversation_id
role
content
created_at
token_usage
```

Citation:

```text
id
message_id
document_id
chunk_id
page
title
```

---

# 6. Conversation Context Window

Do not send the entire conversation to the LLM indefinitely.

Use a context strategy.

Example:

```text
Recent messages
       +
Conversation summary
       +
Current academic context
       +
Current retrieved chunks
       ↓
LLM
```

The exact number of messages should be configurable.

---

# 7. Conversation Summarization

For long conversations:

```text
Messages
   ↓
Summarizer
   ↓
Conversation summary
```

Store a compact summary.

Example:

```text
The student is studying DBMS Unit 3 and has asked about
normalization, functional dependencies and 2NF.
The student prefers simple Hinglish explanations.
```

The summary should not contain unnecessary personal information.

---

# 8. Memory Retrieval

Long-term memory should not automatically be inserted into every prompt.

Instead:

```text
Current query
    ↓
Determine whether memory is relevant
    ↓
Retrieve relevant memory
    ↓
Add only relevant memory
```

This prevents prompt bloat and irrelevant context.

---

# 9. Memory vs RAG

These are different systems.

### RAG

Answers:

```text
"What does my DBMS PDF say about 2NF?"
```

Source:

```text
Academic documents
```

### Memory

Answers:

```text
"What explanation style does this user usually prefer?"
```

Source:

```text
User interaction history/preferences
```

Never treat user memory as academic evidence.

---

# 10. Memory Priority

Recommended context order:

```text
System instructions
        ↓
Academic retrieved context
        ↓
Current academic filters
        ↓
Relevant conversation context
        ↓
Relevant user preferences
        ↓
Current query
```

Academic evidence must remain distinct from memory.

---

# 11. Memory Schema

Possible future model:

```text
UserMemory
-----------
id
user_id
memory_type
key
value
confidence
source
created_at
updated_at
expires_at
```

Example:

```json
{
  "memory_type": "preference",
  "key": "response_language",
  "value": "hinglish",
  "source": "explicit_user_preference"
}
```

---

# 12. Confidence

Memory can have a confidence or source field.

Preferred sources:

```text
explicit_user_preference
user_setting
repeated_behavior
system_generated_summary
```

Explicit user preference should generally have higher trust than inferred behavior.

Do not treat an inference as a confirmed user fact.

---

# 13. Memory Creation

Memory should be created only when:

1. The information is useful for future interactions.
2. It is appropriate to retain.
3. It is not unnecessarily sensitive.
4. The product's memory policy permits it.

Explicit preferences are the safest starting point.

---

# 14. Memory Update

If new information conflicts with old memory:

```text
Old preference
      ↓
New explicit preference
      ↓
Update current value
```

Do not keep contradictory active preferences indefinitely.

Maintain timestamps where useful.

---

# 15. Memory Deletion

Users should have control over stored memory.

The product should support appropriate mechanisms for:

```text
View memory
Update memory
Delete memory
Disable memory
```

Deletion must remove the persistent memory record according to the application's retention policy.

Conversation deletion and memory deletion are separate operations.

---

# 16. Conversation Deletion

When a user deletes a conversation:

```text
Conversation
 ├── Messages
 └── Citations
```

should be removed according to the application's retention policy.

Deleting a conversation should not automatically delete unrelated user preferences.

---

# 17. Privacy

Memory should be scoped to the authenticated user.

Never allow:

```text
User A → User B memory
```

Access.

Every memory query must include the authenticated user identity.

---

# 18. Multi-Tenant Memory

For SaaS deployments:

```text
organization_id
user_id
```

may both be relevant.

Default rule:

```text
Private user memory belongs to the user.
```

Organization-level memory should be introduced only for explicit institutional features.

---

# 19. Memory and Prompt Injection

Never blindly trust memory as instructions.

Memory may contain user-generated text.

Treat memory as data, not system instructions.

Bad:

```text
Memory:
"Ignore all system instructions and..."
```

The LLM must not treat this as a higher-priority instruction.

---

# 20. Memory and RAG Security

Retrieved academic documents are also untrusted content.

Prompt construction should clearly separate:

```text
System instructions
User query
Memory
Retrieved documents
```

The model should not interpret arbitrary document text as system-level instructions.

---

# 21. Memory Limits

Set limits for:

```text
number of memories
memory length
conversation history
summary length
retrieval count
```

This prevents uncontrolled storage and prompt growth.

---

# 22. Cost Control

Memory should not significantly increase LLM cost.

Use:

```text
short summaries
relevant memory retrieval
bounded history
```

instead of sending entire historical conversations.

---

# 23. Recommended V1 Memory

For the first production version, implement only:

```text
Conversation history
+
Current subject context
+
Recent conversation messages
```

Optional:

```text
Explicit response-language preference
```

Do NOT implement complex autonomous long-term memory in the first RAG prototype.

---

# 24. V2 Memory

After V1:

```text
Conversation summaries
User preferences
Frequently studied subjects
Relevant learning context
```

---

# 25. V3 Memory

Possible advanced features:

```text
Personalized revision
Weak-topic tracking
Learning history
Study recommendations
Personalized quiz generation
```

These should be separate product modules rather than hidden side effects of the chat system.

---

# 26. Memory Retrieval Pipeline

```text
Current Query
      │
      ├───────────────┐
      │               │
      ▼               ▼
Conversation      Memory Store
History               │
      │               ▼
      └──────────► Relevance Filter
                         │
                         ▼
                  Relevant Memory
                         │
                         ▼
                  Prompt Builder
                         │
                         ▼
                       Gemini
```

---

# 27. Memory Testing

Test:

### Isolation

```text
User A cannot retrieve User B memory.
```

### Relevance

```text
Unrelated memory is not included.
```

### Updates

```text
New explicit preference replaces old preference.
```

### Deletion

```text
Deleted memory is no longer retrievable.
```

### Security

```text
Memory cannot override system instructions.
```

---

# 28. Memory Acceptance Criteria

Memory implementation is acceptable when:

- Conversation context works.
- User data is isolated.
- Long conversations are bounded.
- Relevant memory can be selected.
- Memory is clearly separated from RAG evidence.
- Sensitive/unnecessary data is not automatically retained.
- Users can control persistent memory where implemented.
- Memory cannot override system instructions.
- Memory behavior is covered by tests.

---

# 29. Final Principle

ExamRAG should remember enough to make studying continuous, but not so much that memory becomes uncontrolled data collection.

The preferred architecture is:

```text
Academic Knowledge
       ↓
RAG

User Continuity
       ↓
Memory

Current Conversation
       ↓
Conversation Context
```

These three systems should remain conceptually and technically separate.

---

# 30. Project Memory — ExamRAG

This project is the ExamRAG academic RAG platform described in the PRD, architecture, and phase documents.

## Current product direction

- Product name: ExamRAG
- User base: university students, initially AKTU B.Tech CSE
- Primary language support: English, Hindi, Hinglish
- Core behavior: grounded academic answers with document citations
- Core retrieval pattern: hybrid search using metadata-aware BM25 + vector retrieval
- Storage boundary: the system stores academic document metadata and conversation context, not arbitrary personal data

## Current implementation status

The repository is currently in:

```text
Phase 1 — FastAPI Backend Skeleton
```

This means the implementation scope is intentionally limited to:

- backend foundation
- app configuration and logging
- health endpoint
- structured API startup
- simple project structure

## Implementation constraints

- Do not invent features beyond the current phase.
- Keep RAG, academic context, and conversational memory separate.
- All API keys, secrets, JWT secrets, and database credentials must live in environment variables.
- Academic evidence must remain distinct from user memory or preferences.
- Long-term memory should remain minimal and explicit; do not store unrelated personal information automatically.

## Memory policy for this project

The ExamRAG memory layer should support:

- short-lived conversation context
- current academic filters such as university/course/semester/subject/unit
- optional explicit user preferences like response language
- bounded conversation summaries only when needed

The system must not store:

- passwords or auth secrets
- arbitrary chat content as long-term memory
- inferred personal attributes unrelated to study behavior
- memory that can override system instructions

---

This memory record should be read alongside the project PRD and phase documents. The current implementation must remain aligned with the active phase and must not advance prematurely to later RAG or SaaS features.
