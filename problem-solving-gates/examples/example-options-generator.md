# Example: Options Generator Mode

**Context:** I'm adding search to a small app and need to decide how to implement it before I write any code.

**Precondition check:** Do I have named constraints and an initial lean? Yes — dataset is ~50k rows, self-hosted (no budget for a managed search service), and results need to support typo tolerance. My lean: Postgres full-text search (`tsvector`) since I already run Postgres and don't want another service to operate.

**Me:** "I'm deciding how to implement search. Constraints: ~50k rows, self-hosted with no budget for a managed service, need typo tolerance, already running Postgres. My initial lean is Postgres full-text search with a `tsvector` column. What am I missing?"

**Claude:** "One thing worth naming explicitly: does Postgres full-text search actually give you typo tolerance out of the box, or were you planning to add something for that? Separately — have you considered `pg_trgm` (trigram similarity, also built into Postgres) either instead of or alongside `tsvector`, since that's the piece that usually handles fuzzy/typo matching? And is SQLite's FTS5 in scope, or is Postgres a hard constraint already, not just a lean?"

**Me:** "Postgres is a hard constraint, I'm already committed there for the main data. And no, I hadn't separated typo tolerance from full-text search — I was conflating the two. `pg_trgm` for fuzzy matching plus `tsvector` for the actual search ranking is probably the real answer."

**Claude:** "That tracks with your constraints as stated. Anything else in the constraint list that a self-hosted managed alternative (Meilisearch, Typesense running as a container) would satisfy that this combination doesn't — or is 'no budget for a managed service' specifically about hosted/paid, not self-run open-source search engines?"

**Me:** "Good catch — I meant no budget for a *hosted* service, not that self-run alternatives are off the table. But adding another container to operate is exactly what I was trying to avoid by leaning on Postgres in the first place, so I'm sticking with `tsvector` + `pg_trgm`."

**Outcome:** Decision made — Postgres `tsvector` for ranking, `pg_trgm` for typo tolerance, no extra service. Claude surfaced a gap (typo tolerance wasn't actually covered by my original plan) and a genuine alternative (self-hosted search engines) without ranking anything or telling me what to pick.
