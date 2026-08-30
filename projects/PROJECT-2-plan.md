# Project 2: Distributed Task Queue with Web UI

## Goal
Build a distributed task queue system where users can submit long-running jobs (e.g., data processing, report generation, batch operations), monitor progress in real-time, and retrieve results — demonstrating how to scale background work across multiple workers while handling retries, failures, and priorities.

## Architecture

### High-Level

The system is split into three layers: a REST API where clients submit jobs and poll for status, a PostgreSQL database that holds the job ledger and tracks worker state, and a pool of stateless workers that consume jobs from the queue, execute them, and report results back.

A user submits a job (e.g., "process 1000 records") via the REST API, which creates a job record with status `pending`, a priority, and a max-retry count. Workers continuously poll a job table ordered by priority and timestamp, claim a job (setting status to `in_progress` with a worker ID and lease timeout), execute it, and either mark it `done` with results or `failed` with an error code. If a worker crashes or hangs (detected via a stale lease), the job is automatically re-queued for retry up to its max-retry limit. A dead-letter queue captures jobs that exhaust retries so they can be manually inspected. The frontend (a single-page app) shows an inbox of jobs grouped by status (pending, running, done, failed), charts job duration/success rates, and real-time progress (via polling, not WebSockets, to keep infrastructure simple).

The key insight: instead of scaling by adding more instances of a monolithic app (which the finance dashboard didn't need), this project demonstrates how to scale by decoupling submission (the API) from execution (the workers), with the database as the durable coordination point. This teaches job queuing, retry logic, failure detection, and priority scheduling — patterns you'll see in every production system that does async work at scale.

### Technical Decisions

| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Queue mechanism | PostgreSQL with polling (not Celery/RabbitMQ) | Keeps the project self-contained (no new infrastructure), teaches the trade-offs of a dumb queue (polling latency, retry semantics) vs. a smart queue, and is intentionally different from Project 1's API-driven approach — this forces thinking about coordination via a database, not a message bus | Celery + Redis — more production-like, but adds complexity and a new system to operate; RabbitMQ — similar trade-off; simple in-memory queue — works for the MVP but doesn't teach anything about durability or recovery |
| Backend framework | FastAPI (again) | Consistency with Project 1 for the API layer means focus is on the *new* part (job queueing) not re-learning frameworks; FastAPI's async support helps the workers efficiently multiplex over long-running tasks | Flask — simpler, but the job polling loop is easier in async; Go / Rust — would teach a new language, but outside the scope (goal is to learn job-queueing patterns, not language churn) |
| Database | PostgreSQL (same as Project 1) | Consistency with P1; ACID guarantees matter here (job transitions must be atomic, lease conflicts must be detected), so relational is the right choice; can use advisory locks for claiming a job atomically | SQLite — works for local dev, but doesn't handle concurrent worker leases correctly without heavy locking; MongoDB — weak ACID means retry logic becomes fragile |
| Job execution | Synchronous (workers run jobs inline, not spawning subprocesses) | Teaches the basic pattern (consume, execute, report) without the complexity of subprocess management; a real system would fork/spawn/containerize, but that's a follow-on | Subprocess / Celery task — adds infrastructure; concurrent.futures — complicates the already-complex retry loop |
| Progress & observability | Polling from the frontend; workers report status updates on success/failure | Keeps the frontend simple (no WebSockets), and polling is a realistic pattern for many job queues; status updates are written durably to Postgres so they survive a worker restart | WebSockets for live push — adds infrastructure but would teach real-time patterns; streaming logs — out of scope for this project |
| Deployment | Render (backend API) + Render (workers as background tasks, or a simple Linux box running job scripts) + Vercel (React frontend) | Fast iteration on infrastructure similar to Project 1 for consistency; workers can run on Render's scheduled tasks or a cheap VPS polling the queue | Kubernetes — overkill; AWS Batch — same trade-off as Kubernetes; local Docker Compose (dev-only) — fine for iteration but doesn't teach production deployment patterns |

### Non-Trivial Challenges

1. **Atomicity of job claiming without distributed locks** — A worker must claim a job such that two workers never claim the same job simultaneously (a race condition means duplicate work). Approach: use a PostgreSQL advisory lock or SELECT...FOR UPDATE on the job row to ensure atomic claim-and-mark-in-progress; make the lease time (how long a worker can hold a job before it's considered dead) configurable and test the behavior when a worker crashes mid-job; log every claim/release for debugging deadlock scenarios.

2. **Retry logic and exponential backoff without creating a thundering herd** — If 1000 jobs fail at once and are all retried immediately, the workers and database are overloaded again. Approach: track retry count per job; on retry, add an exponential-backoff delay (e.g., 2^retry seconds) before the job becomes claimable again; implement a `next_claim_after` timestamp column so jobs naturally sort into the queue after their backoff period (no need for a separate scheduler); tests that verify a failed job respects backoff and isn't claimed too early.

3. **Worker resilience and job resumability** — A worker crashes mid-job (network failure, OOM, segfault). The job is left in `in_progress` with a stale lease. Later, a new worker detects the stale lease and re-queues the job. But how many times can it retry? What if the job is not idempotent (e.g., charging a credit card)? Approach: make the job schema include a `max_retries` field; document which jobs are idempotent and which aren't (users can mark a job as `idempotent=false` and the queue won't auto-retry it past 1 attempt, instead moving it to dead-letter for manual intervention); test scenarios: job succeeds on 2nd attempt, job is not idempotent and fails permanently, job times out and is retried, worker crash during a long-running job.

## Success Criteria
- [ ] Shipped and deployed (API, workers, database, frontend all reachable and functional)
- [ ] Core features working: job submission and status tracking, worker claiming and execution, retry logic with exponential backoff, dead-letter queue for failed jobs
- [ ] Clean code (reviewable): separation of concerns between API and worker logic, configuration not hardcoded
- [ ] Tests for critical paths: atomic job claiming, retry backoff timing, stale lease detection and re-queueing, cross-worker race conditions
- [ ] Can explain the architecture and tradeoffs: why polling over message queues, why ACID/advisory locks matter, why exponential backoff is necessary, how to handle non-idempotent jobs

## Timeline
- Week 1: Setup, schema, and API scaffolding — FastAPI project, PostgreSQL schema (jobs, workers, dead-letter table), basic job submission and status endpoints
- Week 2: Worker implementation and retry logic — polling loop, job claiming with advisory locks, status updates, exponential backoff calculation, dead-letter routing
- Week 3: Resilience and observability — stale lease detection, automatic re-queueing, logging/tracing of job lifecycle, tests for race conditions
- Week 4: Frontend — React dashboard showing job inbox (pending/running/done/failed), charts for duration/success rate, job detail view with logs
- Week 5: Integration, edge cases, and Polish — end-to-end testing, error handling on worker crashes, concurrent job load testing, timeout/backoff tuning
- Week 6 (optional): Deployment and interview story — Render/Vercel deployment, README documenting the queue semantics, interview story and post-mortem of interesting bugs/tradeoffs

## Interview Story (Draft)
"I built a distributed task queue system that lets users submit long-running jobs and track progress in real-time. The core challenge was ensuring that multiple workers could safely claim and execute jobs without race conditions or duplicate work — that meant using PostgreSQL's advisory locks to atomically claim a job, so two workers never touch the same job simultaneously. I also had to handle the reality that workers crash: I implemented a lease-based timeout so jobs claimed by dead workers are automatically re-queued, but with exponential backoff to avoid overwhelming the system if many jobs fail at once. A tricky edge case was non-idempotent jobs (like charging a credit card) — retrying them is risky, so I added support for marking jobs as non-retryable and routing them to a dead-letter queue for manual review if they fail. What I learned: most of the complexity in a production system isn't in the happy path (user submits job, worker runs it, returns result), it's in the failure modes — worker crashes, network partitions, and resource contention — and designing durability and observability around those cases is what separates a toy queue from one you can actually run in production."
