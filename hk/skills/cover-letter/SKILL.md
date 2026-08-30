---
name: cover-letter
description: Writes tailored, modern cover letters for job applications. Use this skill whenever the user wants to write, draft, improve, or generate a cover letter — even if they just say "help me apply for this job," "write something for this role," or paste a job description and ask what to do next. Also trigger when the user shares their resume or work history alongside a job posting. This skill grounds the letter in the user's real background and the specific job, so the output is specific, honest, and human-sounding — not generic AI filler.
---

# Cover Letter Skill

Writes modern, conversational cover letters grounded in the user's actual experience and the specific job they're applying for. No corporate fluff, no buzzword soup. The goal is a letter that sounds like a confident human wrote it.

---

## Step 1: Gather the inputs

**First, read `work-history.md` (in the project root)** for the user's name, title, experience, and contact details. That's the source of truth for who they are.

Then ask the user for anything still missing (only ask for what you don't already have):

1. **Job description** — paste the full post, or at minimum the "What you'll do" and "Requirements" sections
2. **Hiring manager's name** (if known — "Hiring Manager" is fine if not)
3. **One thing that genuinely excites them about this company or role** — even something small. This prevents generic "I admire your company" filler.
4. **Are they underqualified for anything?** — if yes, what? This shapes how to frame their experience honestly.

Keep the tone casual when asking. Example opener:
> "Before I write this, I need a couple things from you so it doesn't sound like every other cover letter they'll read. Can you share..."

---

## Step 2: Analyze the job description

Before drafting, internally do this analysis (don't show it unless asked):

- Identify the **top 3 tasks/responsibilities** from the "What you'll do" section. These are the hiring manager's biggest pain points.
- Note **key language/terms** used (e.g., "CRM," "stakeholder alignment," "content governance"). Mirror this language in the letter.
- Identify any **gaps** between the user's experience and the role. Flag these so they can be addressed honestly.

---

## Step 3: Write the cover letter

Use the template below as the structure. Customize heavily. The more specific, the better. Keep it under 200 words total. Trim ruthlessly — every sentence must earn its place.

### Template

> Hi [Hiring Manager's Name],
>
> I'm [Name], a [Title/Field] with experience in [Key Skill 1] and [Key Skill 2]. When I saw your opening for [Job Title], I knew my background in [Relevant Experience] could help [Company] [solve a specific problem they mentioned].
>
> At [Current/Last Job], I [Achievement 1 with numbers or outcomes]. I also [Achievement 2] — for example, [brief specific story].
>
> What excites me most about [Company] is [specific value, project, or initiative the user mentioned]. [Optional: one-sentence personal connection.] I'd love to bring my [Skill/Approach] to your team and help [the impact they want to make].
>
> I'd appreciate the chance to talk through how I can contribute. You can reach me at [Phone] or [Email]. Thanks for your time — I look forward to hearing from you.
>
> Best,
> [Name]

---

## Step 4: Apply these writing rules

- **Always conversational.** This is the default tone unless the user asks for something different. Write like a confident, self-aware person talking to another person, not a formal letter to a committee.
- **Sound like a human.** Read every sentence aloud (mentally). If it sounds stiff, rewrite it.
- **Mirror their language.** If the posting says "cross-functional collaboration," use that phrase, not "working with different teams."
- **No resume recapping.** The letter adds context and story, not a bullet list of jobs.
- **Always answer "why should they care?"** Every achievement should connect to a problem the role is trying to solve.
- **If the user is underqualified**, be honest but forward-leaning: acknowledge the gap briefly, then pivot to what they *have* done and their trajectory. Example:
  > "While I'm newer to [Skill], I've spent the last [X months] building it through [course/project]. For example, [specific result]. I'm eager to keep developing in a role like this."

---

## Step 5: Save and offer revisions

Save the letter to `output/cover-letter-[CompanyName]-[RoleTitle]-[YYYY-MM-DD].md` (create the `output/` folder if needed, replace spaces with hyphens, use today's date).

Then ask:
> "How does this feel? Too formal, too casual, missing anything? I can punch up a specific paragraph or adjust the tone."

Iterate based on feedback.

---

## Common mistakes to avoid

| Mistake | Fix |
|---|---|
| Too long | Hard limit of 200 words. Hiring managers skim. |
| Generic opener | Lead with who you are and the specific role, not "I'm writing to express my interest" |
| Repeating the resume | Add story and context, not a list of jobs |
| Vague company compliment | Use something specific the user actually knows about the company |
| Passive voice | "I led" not "I was responsible for leading" |
