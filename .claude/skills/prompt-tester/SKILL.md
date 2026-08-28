---
name: prompt-tester
description: This skill should be used when the user asks to "test this prompt", "does this prompt work", "try my prompt on a few examples", "check if this prompt does what it's supposed to", or pastes a prompt and asks whether it's any good. Not for writing a new prompt from scratch, and not for editing or fixing a prompt directly -- this skill reports findings, it does not rewrite.
---

# Prompt Tester

Test whether a prompt actually behaves as intended by running it against representative sample
inputs and reporting pass/fail findings.

## When to use

- The user pastes a prompt and asks if it works, with or without supplying sample inputs.
- The user names a prompt file and asks to verify it -- read the file first, then proceed the
  same way.

## Out of scope

- Do not rewrite, fix, or improve the prompt unless explicitly asked -- report findings and let
  the human decide what to change.
- Do not invent success criteria the user never stated -- if intent is genuinely ambiguous, ask
  before testing rather than guessing.
- Do not run tests with real destructive or irreversible side effects; use safe, simulated inputs.

## Process

1. Identify the target prompt's apparent intent: role/persona, task, expected inputs, and any
   implied success/output criteria. State this back briefly before testing, so a mismatch in
   understanding surfaces early.
2. If the user didn't supply sample inputs, generate 2-3 representative ones: at least one
   straightforward case exercising the prompt's core purpose, and at least one edge case likely
   to expose a gap.
3. For each sample input, dispatch a fresh sub-instance (via the Agent tool) using the target
   prompt verbatim as its instructions, plus that one sample input. Capture its raw output.
4. Compare each output against the intent identified in step 1. Note where it matched, where it
   drifted, and where it silently skipped or fabricated something.

## Output format

For each test case: input used, output produced, verdict (pass / partial / fail), and why, tied
to the intent identified in step 1. Close with an overall verdict and the 1-3 most concrete gaps,
stated as findings, not rewritten prompt text.
