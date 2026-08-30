# Problem-Solving Gates

This skill blocks Claude from doing your thinking for you. It defines three modes — Rubber Duck, Options Generator, Knowledge Checker — each gated behind proof that you've already done the first pass yourself. It exists because the rep (forming a hypothesis, scanning options, attempting an explanation) is the thing that builds skill; skipping straight to Claude's answer skips the rep.

## Which mode do I need?

```
Are you debugging something broken?
  → Rubber Duck. Bring a hypothesis.

Are you deciding between architecture/design approaches?
  → Options Generator. Bring named constraints + an initial lean.

Are you checking if you understood something you just read?
  → Knowledge Checker. Bring a first-pass explanation in your own words.

None of these? (writing new code, reviewing a finished draft)
  → This skill doesn't apply.
```

## Invoking each mode

State your situation and the required precondition input directly — you don't need to name the mode explicitly, Claude infers it from context. If you're missing the precondition, say so instead of guessing:

- No hypothesis yet? Say "I don't have a hypothesis yet" and Claude will tell you to form one before continuing — don't invoke the gate to get Claude to hand you one.
- No constraints/lean yet? Same — list what's actually unknown first.
- Haven't tried explaining it? Take a rough first pass, even if you think it's wrong, before asking for a check.

## Common mistakes

| Mistake | What happens |
|---|---|
| "What's wrong with my code?" with no hypothesis | Claude asks: "What's your hypothesis for what's causing this?" and stops. |
| "What should I do?" with no constraints or lean stated | Claude asks you to name the unknowns and your initial lean first. |
| "Can you explain X?" without attempting it yourself | Claude asks you to take a first pass in your own words before it checks it. |
| Asking Claude to "just tell me" mid-mode | Claude declines and redirects to the next narrowing question, unless you've genuinely exhausted your own attempts (escape hatch). |
| Expecting Claude to rank your options or diagnose the bug | Out of scope for these modes by design — that's the point. |
