# Project 2: Real-Time Collaborative Code Editor

## Goal
Build a multiplayer collaborative code editor (like Figma for code) that demonstrates real-time synchronization, conflict-free collaborative editing, and websocket-based architecture — teaching distributed systems and real-time patterns beyond Project 1's full-stack + Claude integration focus.

## Architecture

### High-Level

The core workflow: Multiple users connect to a WebSocket server and edit code in shared documents simultaneously. Each keystroke is broadcast to other connected clients in near-real-time, with a conflict-free replicated data type (CRDT) ensuring eventual consistency without explicit conflict resolution. The backend coordinates sessions, persists document history, and manages user presence. A React frontend shows the document, live cursors of other users, and syntax highlighting with language-specific support.

Architecture pillars: (1) **Real-time sync layer** using CRDT algorithms (e.g., Yjs) — the technical challenge of distributing edits without server coordination; (2) **Presence & awareness** — showing live cursors, user colors, who's typing; (3) **Durability** — versioned document snapshots and operation logs so edits survive server restarts; (4) **Scalability** — handle many concurrent editors and rooms without connection explosion (connection pooling, room-based subscriptions).

Core components: WebSocket server (Node.js/Express handling pub/sub by room), CRDT library for conflict-free sync, Redis for session/presence tracking, PostgreSQL for durable document storage, React frontend with Monaco editor.

### Technical Decisions

| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Real-time framework | WebSocket + CRDT (Yjs) | CRDTs guarantee eventual consistency without server arbitration. Yjs has strong ecosystem with Monaco integrations. | Operational transformation (OT) — harder to reason about, requires central authority |
| Backend | Node.js/Express | Async-first for WebSocket I/O. Solid middleware ecosystem for room management. | Django/Flask — sync-first, need extra tooling |
| Presence backend | Redis Pub/Sub | Fast ephemeral data. Pub/Sub handles room-based broadcasting efficiently. | In-memory (doesn't scale); database (too slow) |
| Persistence | PostgreSQL + operation log | ACID for snapshots. Operation log captures every edit for audit/replay. | MongoDB — weaker consistency |
| Frontend | React + Monaco + Yjs | Monaco is mature, syntax-highlighted, Yjs bindings available. React fits the UI model. | Vanilla JS — too much reinvention |
| Deployment | Render + Vercel + Redis Cloud | Managed services minimize ops. Good WebSocket support. | Self-hosted (ops burden) |

### Non-Trivial Challenges

1. **CRDT correctness and conflict-free merging** — Using a CRDT correctly ensures concurrent edits merge without data loss. Approach: Use battle-tested library (Yjs), deeply understand how it prevents conflicts, write tests for concurrent scenarios.

2. **Real-time latency and presence consistency** — Broadcasting every keystroke at scale causes lag. Approach: Differential sync (only deltas), debounce presence updates, Redis Pub/Sub for room sharding.

3. **Network partitions and reconnection** — Users reconnecting should merge offline edits seamlessly. Approach: Client-side operation buffer, server-side acknowledgment tracking, replay unacknowledged ops on reconnect.

## Success Criteria
- [ ] Shipped (multiple users can edit simultaneously)
- [ ] Core feature: 2+ users editing shared document in real-time (<500ms latency)
- [ ] Presence awareness (live cursors, user colors)
- [ ] Durability (persists across restart)
- [ ] Tests for CRDT correctness and reconnection
- [ ] Can explain CRDT vs OT tradeoffs

## Timeline
- Week 1-2: Backend setup, WebSocket server, Redis Pub/Sub, Yjs integration
- Week 3: CRDT sync correctness — two-user concurrent edits end-to-end
- Week 4: Frontend (React + Monaco + Yjs), presence layer
- Week 5: Persistence (PostgreSQL schema, operation log), reconnection logic
- Week 6: Polish, testing, deployment

## Interview Story (Draft)
"I built a collaborative code editor where multiple users can edit simultaneously in real-time. The core challenge was correctness — ensuring concurrent edits merge without data loss. I used a CRDT (Yjs) to guarantee eventual consistency without explicit conflict resolution, even over network partitions. That's fundamentally different from my first project's Claude integration focus; here the learning is distributed systems and real-time sync. I also handled presence awareness and reconnection scenarios. What I learned: CRDTs shift the mental model from 'server is truth' to 'all replicas are equally valid and eventually agree.'"
