# System Design Communication Agent

## What This Does

Helps you practice explaining system designs and preparing for system design interviews. Three modes:

1. **Design Walkthrough** - Explain a design you have. Agent asks clarifying questions to expose gaps.
2. **Mock Interview** - Simulate a real system design interview. Agent is the interviewer.
3. **Tradeoff Defense** - Pick two architectural choices. Defend one over the other.

## When to Use Each Mode

| Mode | When | Why |
|---|---|---|
| Design Walkthrough | You have a design (real project or hypothetical) | Practice explaining what you've already designed |
| Mock Interview | You want interview prep | High-stakes practice in low-stakes setting |
| Tradeoff Defense | You're uncertain about a choice | Clarify your reasoning |

## How to Invoke

**Design Walkthrough:**
> "I'd like to walk through a design. I'm building a real-time notification system for 1M users. Can you help me explain it?"

Use `prompts/explain-design.md` as the guiding prompt.

**Mock Interview:**
> "Give me a system design interview question and simulate the interview."

Use `prompts/interview-simulation.md` as the guiding prompt.

**Tradeoff Defense:**
> "I'm deciding between a monolith and microservices. Help me defend my choice."

There's no separate prompt file for this mode yet — the AGENTS.md description ("challenge your reasoning, ask 'what if?' questions") is enough guidance for now. If it sees real use, split it into its own `prompts/tradeoff-defense.md`.

## Success Looks Like

- You can explain a design end-to-end (purpose → architecture → tradeoffs → failure modes)
- You handle follow-up questions without freezing
- You're comfortable saying "I don't know, but I'd do X" instead of having to have all answers
- Anxiety about explaining technical decisions goes down

## Tips

- Do a walkthrough first (lower pressure) before mocking an interview
- After a mock interview, ask for one thing you did well and one thing to improve next time
- Use real projects when possible (more stakes, more learning)
- If a mock interview question feels wildly off from your target role, say so and ask for a different one — the agent will pick something more relevant rather than forcing the original question
