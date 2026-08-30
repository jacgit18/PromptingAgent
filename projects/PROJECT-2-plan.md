# Project 2: DevDocs — RAG Chat Over Your Documentation

## Goal
Build a retrieval-augmented generation (RAG) system that lets a user upload technical documents and chat with them in real time, with cited sources, so I can demonstrate a second, genuinely different Claude integration pattern (retrieval + streaming) beyond Project 1's classification/insights pattern.

## Architecture

### High-Level
The core workflow starts with document ingestion: a user uploads a document (PDF or Markdown), the backend extracts and chunks the text, generates an embedding vector per chunk, and stores both the chunk text and its embedding in Postgres (via the `pgvector` extension). When the user asks a question in the chat UI, the backend embeds the query, runs a similarity search against the stored chunk vectors to retrieve the top-k most relevant chunks, and assembles those chunks plus the question into a prompt for Claude. The response streams back to the frontend token-by-token over Server-Sent Events (SSE) so the chat feels live rather than waiting on a full response, and the UI displays which source chunks the answer was grounded in.

The core components are: a FastAPI backend exposing upload and chat endpoints; PostgreSQL + `pgvector` holding documents, chunks, and their embeddings; an ingestion service that handles chunking and embedding generation; a retrieval service that performs vector similarity search and assembles retrieval context; a streaming chat service that calls Claude with the retrieved context and streams the response back over SSE; and a React frontend (document upload UI, streaming chat interface, citation display linking answers back to source chunks).

Components talk to each other over well-defined boundaries: React calls FastAPI over REST for upload and document management, and opens an SSE connection for chat so tokens can stream as Claude generates them rather than the frontend polling for a finished response; FastAPI talks to Postgres/pgvector via SQLAlchemy (async) for both metadata and vector similarity queries; the embedding and chat services call Claude and an embedding model via their respective SDKs. This is deliberately different from Project 1's architecture — Project 1's Claude calls were fire-and-forget batch/async jobs with polling; this project's core interaction is a live, streamed, context-grounded conversation, which is a different integration shape worth having in the portfolio.

### Technical Decisions
| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Vector store | PostgreSQL + `pgvector` extension | Reuses Postgres operational knowledge from Project 1 while adding vector similarity search; avoids standing up a separate managed vector DB for a portfolio-scale project; keeps chunk metadata and vectors in one transactional store | Pinecone / Chroma — purpose-built and easier to scale, but adds another service to run/pay for when Postgres can do this at this project's scale |
| Embedding model | Voyage AI embeddings (Anthropic's recommended embedding partner) | Pairs naturally with the Claude ecosystem; strong retrieval quality benchmarks; keeps the "AI vendor surface" coherent with the rest of the stack | OpenAI `text-embedding-3` — comparable quality, but pulls in a second AI vendor for no real benefit here |
| Streaming transport | Server-Sent Events (SSE) | Chat responses are one-directional (server streams tokens to client); SSE is simpler than WebSockets for this shape, works over plain HTTP, and reconnects automatically | WebSockets — more powerful (bidirectional, lower overhead for high-frequency messages) but unnecessary complexity for a single streaming response per turn |
| Chunking strategy | Fixed-size chunks with overlap (e.g., ~500 tokens, ~50-token overlap), section-aware where possible (split on headings first) | Simple to implement and reason about; overlap reduces the risk of cutting a relevant fact across a chunk boundary; section-awareness improves retrieval relevance over naive fixed-size splitting alone | Fully semantic/LLM-based chunking — likely higher quality but adds cost and latency to ingestion that isn't justified for a portfolio-scale project |

### Non-Trivial Challenges
1. **Chunking and retrieval quality** — Poor chunking (splitting mid-sentence, losing surrounding context, or chunks too large/small) directly degrades answer quality no matter how good the model is. Approach: use section-aware chunking with overlap, tune top-k and chunk size empirically against a small set of test questions with known-good answers, and log retrieved-chunk relevance so bad retrievals are visible and debuggable rather than silently producing weak answers.
2. **Streaming architecture end-to-end** — Getting tokens from Claude's streaming API through a FastAPI SSE endpoint to a React component that renders incrementally (without flicker, and handling a dropped connection mid-stream) has several places things can silently buffer or break. Approach: use Claude's native streaming API, an async generator in FastAPI that yields SSE-formatted events as they arrive, and a frontend `EventSource`-based hook that appends tokens as they arrive with a clear error/retry state if the stream drops.
3. **Grounding and citation accuracy** — The system must avoid answering from the model's general knowledge when the document doesn't actually contain the answer, and must correctly attribute claims to the chunks they came from. Approach: an explicit system prompt instructing Claude to answer only from provided context and say so when the context is insufficient; return chunk IDs alongside the generated answer so the frontend can render citations directly tied to retrieved text (not model-hallucinated references); test cases that specifically probe out-of-context questions to confirm the model declines rather than fabricates.

## Success Criteria
- [ ] Shipped and deployed
- [ ] Core features working: document upload/ingestion, chunking + embedding pipeline, vector similarity retrieval, streamed chat with citations
- [ ] Clean code
- [ ] Tests for critical paths: retrieval relevance on known test questions, streaming endpoint behavior, out-of-context question handling
- [ ] Can explain the architecture and tradeoffs: pgvector vs. dedicated vector DB, chunking strategy, SSE vs. WebSockets, how grounding is enforced

## Timeline
- Week 1: Setup + ingestion — FastAPI scaffold, Postgres + pgvector schema (documents, chunks, embeddings), document upload endpoint, chunking logic
- Week 2: Embeddings + retrieval — Voyage AI embedding integration, vector similarity search, retrieval service with top-k tuning against test questions
- Week 3: Streaming chat — Claude streaming integration, SSE endpoint, citation attribution logic, grounding/out-of-context test cases
- Week 4: Frontend — React chat UI with incremental token rendering, document upload UI, citation display
- Week 5: Integration, testing, polish — end-to-end testing, error handling (dropped streams, failed ingestion), retrieval quality tuning
- Week 6: Deploy, document, interview story — deployment, README, final architecture write-up, interview story polish

## Interview Story (Draft)
"I built a RAG-based chat system that lets users upload technical documents and ask questions with real-time, streamed, cited answers — a deliberately different Claude integration pattern from my first project's async batch categorization work. The main technical challenge was getting retrieval quality right: naive fixed-size chunking was losing context across boundaries and hurting answer relevance, so I moved to section-aware chunking with overlap and tuned retrieval empirically against a set of test questions. I also had to make sure the system was honest about the limits of its context — it needed to decline to answer rather than fabricate when a document didn't actually contain the answer, which I enforced through prompt design and explicit citation-to-chunk attribution rather than trusting the model's own claims. What I learned: retrieval quality, not model quality, is usually the actual bottleneck in a RAG system — the LLM call is the easy part."

---

*Once shipped, add a "Final Interview Story" section here reflecting what actually happened during the build.*
