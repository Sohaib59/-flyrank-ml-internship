# [APP NAME]

[One-sentence description: what it does, in plain language.]

**Built for:** [who this is for — e.g. "small restaurant owners who need online ordering without a $200/mo SaaS bill"]

---

## What it does

[2-4 sentences. What problem it solves, what the core flow is (user does X, app does Y),
and what makes it worth using over the obvious alternative. Be concrete — name the actual
feature, not "leverages AI to optimize the user experience."]

## Live demo

- **Try it:** [live URL, if hosted]
- **Demo video (3-5 min):** [YOUR VIDEO LINK]

## Architecture

```
[Simple sketch — even ASCII is fine. Example shape:

  Browser (React)
        |
        v
  API (Node/Express or FastAPI/etc.)
        |
        v
  Database (Postgres/SQLite/etc.)
        |
        v
  [Any external service — auth provider, AI API, payments, etc.]
]
```

[One paragraph explaining the sketch: why this shape, what each piece is responsible for,
and where the interesting engineering decision lives.]

## Tech stack

| Layer | Choice |
|---|---|
| Frontend | [e.g. React + Vite / Next.js / plain HTML-CSS-JS] |
| Backend | [e.g. Node/Express / FastAPI / Django] |
| Database | [e.g. Postgres / SQLite / MongoDB] |
| Auth | [if any] |
| Hosting | [e.g. Vercel / Railway / GitHub Pages / self-hosted] |
| Other services | [e.g. Stripe, an LLM API, email provider] |

## Setup — reproduce this locally

A stranger with no context should be able to follow this and get it running.

```bash
# 1. Clone
git clone https://github.com/[you]/[repo].git
cd [repo]

# 2. Install dependencies
[e.g. npm install]

# 3. Environment variables
cp .env.example .env
# then fill in:
#   [VAR_NAME] — [what it is, where to get it]
#   [VAR_NAME] — [what it is, where to get it]

# 4. Set up the database (if applicable)
[e.g. npm run migrate]

# 5. Run it
[e.g. npm run dev]
```

Open [http://localhost:PORT] — you should see [what they should see first].

## Usage examples

**[Example 1 — the core action]**
```
[a real command, curl call, or short walkthrough: click X, enter Y, see Z]
```

**[Example 2 — a second meaningful action]**
```
[same idea]
```

## Eval results (v2)

[This section only works with real numbers. Examples of the shape it should take —
replace with what you actually measured:]

- **[Metric name]:** [value] — measured by [how: a test suite, a set of manual test cases,
  a load test, user feedback count, etc.]
- **[Metric name]:** [value] — [method]
- **What changed from v1 → v2:** [the specific fix/change and the before/after number]

*(If you don't have formal evals yet, be honest about that here rather than inventing numbers —
e.g. "Tested manually against N scenarios listed in `/tests/manual-cases.md`; no automated eval
suite yet — see Limitations.")*

## Limitations

- **[Limitation 1 — the one you'll say on camera]:** [what breaks, when, why it wasn't fixed yet]
- **[Limitation 2]:** [same]
- **[Limitation 3]:** [same]

## Built with AI — what and how

[One honest paragraph, following the assignment's transparency framework. Example shape:
"I built this with Claude/[tool]. AI drafted the initial [component] and [component]; I wrote
the [component] myself and rewrote [X] after AI's first pass didn't handle [case]. I checked
[what you personally verified — the logic, the security, the edge cases] myself before shipping."]

## License

[MIT / etc., if you're adding one]
