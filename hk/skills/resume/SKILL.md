---
name: resume
description: Tailor the user's resume to a specific job posting so it gets past ATS screening. Use this skill whenever the user wants to tailor, customize, rewrite, or ATS-optimize their resume for a role, pastes a job posting and asks for a resume, or asks to match their experience to a job. The ATS system scans the resume for relevant experience, so rewrite the summary, bullet points (X-Y-Z formula), and skills to match the target role. Reads the user's background from work-history.md and saves output to the output/ folder.
---

# Resume Tailoring Skill

When this skill is invoked, tailor the user's resume to a specific job posting so it passes Applicant Tracking System (ATS) screening and speaks directly to the role.

---

## Source of Truth

**Always read `work-history.md` (in the project root) before doing anything else.** That file contains the user's real experience, skills, and certifications. Everything you write must come from it. Never invent experience, metrics, tools, or qualifications that aren't in that file.

If `work-history.md` is missing or still has unfilled `[bracketed]` placeholders, stop and tell the user to fill it in first. Point them to the README.

---

## Workflow

### Step 1 — Get the job posting

If the user hasn't pasted a job description, ask them to paste the full job posting text (or give a URL to fetch).

### Step 2 — Analyze the job

Extract and list:

- **Role title** and **company name**
- **Key responsibilities**, ranked by how much emphasis the posting gives them
- **Required qualifications** (hard requirements the resume must address)
- **Preferred qualifications**

### Step 3 — ATS keyword extraction

ATS systems often do literal string matching, so exact phrasing matters. Treat this as a separate pass from general job analysis:

- Pull every specific noun phrase used for skills, tools, certifications, methodologies, and job titles
- Flag any term that appears more than once as **high-priority**. Repetition signals ATS weight.
- Note the exact form the posting uses (e.g., "decision flows" not "decision trees" if that's the posting's word)
- Build a keyword list that will inform Steps 5, 6, and 7

### Step 4 — Map experience to the role

For each key requirement, identify which of the user's bullets or accomplishments best addresses it. Note any gaps. Flag the 2-3 strongest matching accomplishments as "lead bullets" to feature prominently.

### Step 5 — Write a tailored headline and summary

- **Headline:** match the exact job title (or a close variant) from the posting
- **Summary (3-4 sentences):** open with years of experience and the specific domain, reference 2-3 of the most relevant accomplishments, close with a value statement aligned to the company's goals
- Weave high-priority ATS keywords from Step 3 into the summary naturally. This is the first section an ATS scans.

### Step 6 — Rewrite bullet points using the X-Y-Z formula

Apply the Google X-Y-Z formula to all experience bullets:

> "Accomplished [X] as measured by [Y], by doing [Z]"

**Important:** Never write "as measured by" literally. Weave the metric (Y) naturally into the sentence so it reads fluently. For example: "Improved resolution time by 25% by redesigning the knowledge base workflow" — not "Improved resolution time by 25% as measured by support analytics, by redesigning..."

Rules:

- Order bullets within each role from most to least relevant for this role. The first bullet should be the strongest match to the posting's top priorities; the last bullet the weakest connection.
- Use the exact ATS keywords from Step 3 wherever they truthfully apply. Don't paraphrase if the posting has a specific term.
- If a bullet lacks a quantifiable metric (Y), use qualitative impact (scope, scale, stakeholder level). Never fabricate numbers.
- Keep bullets to one sentence, starting with a strong past-tense action verb.
- Aim for 3-5 bullets per role, trimming the less relevant ones.

### Step 7 — Select a targeted skills list

From the user's skills and expertise in `work-history.md`, select the 8-12 most directly mentioned or implied by the posting. Use the exact vocabulary from the ATS keyword list in Step 3, not synonyms. List them in order of relevance. Group into "Tools" and "Expertise" if space allows.

### Step 8 — Assemble and save the tailored resume

Produce a complete resume in clean Markdown with this structure:

```
# [Full Name][, Credentials]
[contact line: location · email · phone · LinkedIn]

## [Tailored Headline]
[Summary paragraph]

**Key Skills:** [targeted list]
**Key Expertise:** [targeted list]

## Professional Experience
[tailored roles and bullets]

## Education & Certifications
[from work-history.md]
```

Save the file to:

```
output/resume-[CompanyName]-[RoleTitle]-[YYYY-MM-DD].md
```

Use today's date and replace spaces with hyphens in the filename (e.g., `output/resume-Acme-ProjectManager-2026-04-22.md`). Create the `output/` folder if it doesn't exist.

### Step 9 — Gap check and summary report

After saving, briefly tell the user:

- Which of their accomplishments most strongly matched the role
- Any hard qualifications they can't address on the resume
- 1-2 suggestions for how to handle those gaps in a cover letter or interview

---

## Important Rules

- Never fabricate metrics or experiences. If a number doesn't exist, describe impact qualitatively.
- Mirror the job posting's language exactly for skills and tools. ATS systems score on keyword match.
- Always apply the X-Y-Z formula. Don't leave bullets as task descriptions ("responsible for...").
- Everything must trace back to `work-history.md`.
- Always save output to the `output/` folder.
