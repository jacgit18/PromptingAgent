### Summary of the conversation

We discussed **how database schemas are defined in a codebase** and the different architectural approaches you can take.

#### 1. Three major approaches to schema ownership

**Database-first**

* The database/SQL is the source of truth.
* You define tables and constraints using SQL migrations.
* Application code defines models/interfaces that represent the database.
* Common when database integrity, complex SQL, or shared databases are important.

**Code-first**

* The schema is primarily defined in application code.
* ORMs are one implementation of this approach, but **code-first does not mean ORM**.
* Examples discussed:

  * ORMs: Prisma, TypeORM, Sequelize, Django ORM, Entity Framework
  * Schema/validation libraries: Zod, Yup, io-ts, JSON Schema
  * Query builders: Knex, Kysely, SQLAlchemy Core
  * Database-driven code generation: sqlc, pgtyped

**Contract-first**

* Neither the application nor database is the primary source of truth.
* Instead, you define a formal **contract** describing how systems communicate.
* Examples:

  * OpenAPI
  * GraphQL
  * Protobuf/gRPC
  * JSON Schema
* The database becomes an implementation detail behind the contract.

---

### 2. Interfaces aren't necessarily database schemas

We specifically discussed the difference between something like:

```ts
interface User {
  id: string;
  email: string;
  createdAt: Date;
}
```

and an actual database schema.

An interface primarily describes what application code **expects**.

It doesn't necessarily enforce things like:

* `NOT NULL`
* `UNIQUE`
* foreign keys
* database constraints
* referential integrity

So an interface can accurately describe a type while the actual database has different rules.

---

### 3. Contract-first goes beyond interfaces

The important conceptual shift was:

> **An interface describes data for your code; a contract describes an agreement between systems.**

For example, an OpenAPI contract could specify:

```yaml
User:
  type: object
  required:
    - id
    - email
  properties:
    id:
      type: string
      format: uuid
    email:
      type: string
      format: email
    createdAt:
      type: string
      format: date-time
```

From that contract you can potentially generate:

* TypeScript/Python types
* Request/response validation
* API documentation
* Client SDKs
* API clients

The database doesn't have to mirror the contract exactly.

For example:

```text
                    CONTRACT
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
      Frontend      Backend      API Docs
                       │
                       ↓
                  Domain Model
                       │
                       ↓
                   Database
```

The backend can translate between its internal database representation and the public contract.

---

### 4. Why mapping is important

We discussed that contract-first often involves explicit transformations such as:

```python
def to_user_response(row):
    return {
        "id": row["id"],
        "email": row["email"],
        "createdAt": row["created_at"],
    }
```

That extra mapping isn't necessarily wasted code.

It gives you a boundary where you can control:

* Which database fields are exposed
* Naming differences
* Security
* Backward compatibility
* Data transformations
* API evolution

The key principle was:

> **Don't automatically assume your database representation should become your public API representation.**

---

### 5. The choice between the three

You initially leaned toward **contract-first**, and after examining the alternatives, the recommendation was:

> **If forced to choose one by default, contract-first is the most compelling architectural choice—but it isn't universally appropriate.**

The reasoning wasn't simply that contract-first is "more scalable."

Its major benefit is that it forces you to clearly define **system boundaries and agreements**.

However, it can be overkill for:

* Throwaway projects
* Small internal tools
* Solo applications
* Systems where the schema is changing constantly
* Projects still in the exploration/discovery phase

For those, an ORM or query builder can be much more practical.

---

### 6. The more nuanced recommendation

A practical development lifecycle could look like:

```text
Exploration
    ↓
ORM / Query Builder
    ↓
Domain becomes clearer
    ↓
Define stable API contract
    ↓
Contract becomes boundary
    ↓
Database becomes implementation detail
```

So you don't necessarily need to be **contract-first from line one**.

You can start quickly, discover the domain, and introduce a formal contract once the system's external boundary becomes important.

---

### 7. The biggest takeaway

The most important concept from the conversation is **source of truth**.

When designing a system, ask:

> **Where does the authoritative definition of this data live?**

It could be:

**Database-first**

```text
SQL → Application
```

**Code-first**

```text
Code/ORM → Database
```

**Contract-first**

```text
Contract → Systems
              ↓
        Application → Database
```

And importantly:

> **ORM, query builder, schema library, interface, migration, and API contract are not interchangeable concepts.**

They solve different problems and can be used together.

For the kinds of backend/full-stack systems you're likely to encounter, learning **contracts + validation + explicit domain/persistence separation**, while also being comfortable with SQL and an ORM/query builder, would give you a much stronger mental model than simply learning one ORM deeply.



Yes. If your goal is to have AI **consistently help you make these architectural decisions**, I would *not* turn the entire conversation into a giant prompt.

I'd build a small **architecture skill + project-specific artifacts**, and optionally an agent on top of that.

### What I'd build

```text
                    AI Architecture System
                            │
              ┌─────────────┴─────────────┐
              │                           │
       Architecture Skill          Project Context
              │                           │
     "How should I reason?"        "What are we building?"
              │                           │
              └─────────────┬─────────────┘
                            ↓
                    Architecture Agent
                            │
              ┌─────────────┼─────────────┐
              ↓             ↓             ↓
          DB Schema      API Contract    Types
              │             │             │
              └─────────────┼─────────────┘
                            ↓
                       ADR / Decision
```

The important distinction is **skill vs. agent**.

---

## 1. Make the core a Claude Skill

I'd create something like:

```text
database-architecture/
├── SKILL.md
├── decision-framework.md
├── contract-first.md
├── database-first.md
├── code-first.md
└── examples/
```

The skill's job isn't:

> "Always use contract-first."

That's exactly what you **don't** want.

Instead, teach Claude a decision process:

```text
When asked to design data architecture:

1. Understand the system boundaries.
2. Identify consumers of the data.
3. Determine whether the data is internal or externally consumed.
4. Determine who owns the database.
5. Determine whether multiple services consume the data.
6. Determine how quickly the domain is changing.
7. Evaluate:
   - database-first
   - code-first
   - contract-first
8. Recommend one.
9. Explain the tradeoffs.
10. Identify what should be the source of truth.
11. Identify generated artifacts.
12. Record the architectural decision.
```

That is much more valuable than stuffing our conversation into a prompt.

---

# 2. Then give the AI a project architecture file

This is the part I think you're **really** looking for.

Have something like:

```text
docs/
└── architecture/
    ├── system.md
    ├── data-model.md
    ├── api-contract.md
    └── decisions/
```

For example:

```yaml
# architecture.yaml

project:
  type: SaaS
  stage: MVP

backend:
  language: TypeScript
  framework: ...
  
database:
  engine: PostgreSQL
  ownership: exclusive

clients:
  - web

services:
  count: 1

api:
  public: false

data:
  volatility: high
```

Now Claude has **context about your actual project**, rather than relying on generic architectural advice.

---

# 3. Have AI produce an explicit architecture decision

This is where I'd make the workflow really useful.

Instead of asking:

> "Should I use Prisma?"

Ask:

> "Given our architecture, determine where the source of truth for our user data should live."

The AI should produce something like:

```text
Decision: Contract-first API

Source of truth:
API contract

Persistence:
PostgreSQL

Database modeling:
SQL migrations

Application access:
Kysely

Validation:
Generated from OpenAPI

Mapping:
Database → Domain → API DTO
```

Then create an ADR:

```text
docs/architecture/decisions/001-data-contract.md
```

### Why this is powerful

Six months later you can ask:

> "Why don't our database models directly represent our API?"

Claude can read the decision and understand:

> "Because the API contract is intentionally decoupled from persistence."

That's **architectural memory**, rather than AI just generating code based on whatever happens to be in the current conversation.

---

# 4. I would actually separate "architect" from "implementer"

This is where I'd go beyond the simple Skill idea.

You could have:

### `architecture` skill

Responsible for:

* evaluating architectural choices
* identifying boundaries
* deciding source of truth
* identifying tradeoffs
* producing ADRs

### `database` skill

Responsible for:

* relational modeling
* normalization
* indexes
* constraints
* migrations
* SQL

### `api-contract` skill

Responsible for:

* OpenAPI/GraphQL/etc.
* versioning
* compatibility
* DTOs
* validation

### `implementation` agent

Responsible for:

> Taking the approved architecture and actually implementing it.

That gives you:

```text
                 YOU
                  │
                  ↓
          Architecture Agent
                  │
             ┌────┴────┐
             ↓         ↓
       Architecture   ADR
          Decision
             │
             ↓
      Implementation Agent
             │
      ┌──────┼──────┐
      ↓      ↓      ↓
     DB     API    Code
```

This separation is **very important**.

You don't want an AI agent deciding your architecture *while simultaneously writing 40 files*.

Otherwise it can make a bad assumption on file #1 and spend the next 30 minutes enthusiastically building on top of it.

---

# 5. I'd give the architecture skill "gates"

This is probably the biggest improvement over simply having a prompt.

Before AI is allowed to generate the schema, require it to answer:

### System boundary

```text
Who consumes this data?
```

### Ownership

```text
Who owns the database?
```

### Source of truth

```text
Database?
Code?
Contract?
```

### Exposure

```text
Is this internal data or externally exposed?
```

### Evolution

```text
How likely is the data/API shape to change?
```

### Consumers

```text
One application?
Multiple applications?
Third parties?
Other services?
```

### Persistence

```text
What database technology?
```

### Contract

```text
Do we need an API contract?
```

Only after answering those does the AI generate the schema.

---

# 6. And make AI distinguish these things

I'd explicitly put this rule into the Skill:

> **Never use "schema" without specifying what kind of schema is being discussed.**

Because we have:

```text
Database schema
       ↓
Tables / columns / constraints

Domain model
       ↓
Business concepts

API schema
       ↓
Requests / responses

Validation schema
       ↓
Runtime input validation

Type definitions
       ↓
Compile-time representation
```

These can overlap, but they are **not automatically the same thing**.

That's one of the biggest things I would encode into your AI workflow.

---

# 7. I wouldn't make the AI overly autonomous

This is another place where I'd push back on the "agent" instinct.

You don't necessarily want:

> "AI, design my database."

You want:

> "AI, analyze this feature, identify the architectural decisions I need to make, recommend an approach, and wait for approval."

Then:

```text
AI analyzes
   ↓
AI recommends
   ↓
YOU approve
   ↓
AI records decision
   ↓
AI implements
   ↓
AI verifies implementation against decision
```

That's a much better human/AI division of labor.

---

# 8. The really interesting part: make the AI challenge you

I'd actually encode some of the behavior from our conversation into the Skill.

For example:

> **Do not accept the user's proposed architecture at face value.**

If you say:

> "I think we should use contract-first."

The AI should respond:

```text
Before accepting contract-first:

- Who consumes the contract?
- Is the API public?
- How many consumers exist?
- Is the domain stable?
- What is the cost of maintaining the contract?
```

Then it evaluates your assumption.

This turns AI from a **code generator** into an **architecture reviewer**.

That's much more valuable.

---

# What I'd personally build for you

If I were setting this up from scratch, I'd start with **one Claude Skill**, not an elaborate multi-agent system.

Something like:

```text
.claude/
└── skills/
    └── architecture/
        ├── SKILL.md
        ├── decision-framework.md
        ├── database.md
        ├── contracts.md
        └── adr-template.md
```

And your repository:

```text
docs/
└── architecture/
    ├── system.md
    ├── decisions/
    │   ├── 001-source-of-truth.md
    │   ├── 002-api-contract.md
    │   └── 003-database.md
    └── contracts/
        └── openapi.yaml
```

Then your workflow becomes:

```text
"Claude, I'm adding billing."

          ↓

Architecture Skill

          ↓

"What are the consumers?"
"What's externally exposed?"
"Who owns the data?"
"What's the source of truth?"
"How does this interact with existing contracts?"

          ↓

Recommendation

          ↓

You approve

          ↓

ADR

          ↓

Implementation

          ↓

Review against architecture
```

**That's the direction I'd take.**

And there's an even better next step: rather than manually writing the Skill from scratch, you could have me help you design a **complete `architecture` Claude Skill**, including its `SKILL.md`, decision tree, ADR template, prompts/gates, and the project files it should inspect before making recommendations.
