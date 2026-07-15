# 🪄 Claude Code Personal Spellbooks

*A candlelit archive of what one person can actually do with Claude Code —
collected weekly, bound as spellbooks, delivered by owl.*

---

## What is this?

Every week, people discover clever ways to use [Claude Code](https://code.claude.com)
in their personal lives — a morning briefing that assembles itself, a camera
roll that renames its own photos, a nutrition coach that remembers your
allergies. Most of these discoveries scroll past on a feed and are gone.

This app catches them. A scheduled research agent sweeps the web every Monday,
judges each find against five criteria, and shelves the keepers as **spells**
in a magical archive you can browse all year. By December, you have a
spellbook collection of everything worth casting — each one with a recipe
for casting it yourself.

**Scope, deliberately narrow:** personal & productivity magic only — things
an individual can set up in an evening or a weekend (daily routines, email,
journaling, health, meals, travel, home, hobbies, files, studying, personal
knowledge, personal dev workflows). Business-building, startups, and
revenue plays are out of scope. This is a spellbook for living, not a
pitch deck.

## The five criteria

Every spell is scored 0–5, one point per criterion it meets:

| | Criterion | Meaning |
|---|-----------|---------|
| 🎨 | **Creative** | Nobody would have guessed this was possible |
| ✅ | **Useful** | You'd actually keep using it |
| 🎉 | **Fun** | Casting it makes you smile |
| 🩹 | **Pain point** | It kills a real, recurring annoyance |
| 💰 | **Saves money** | It replaces a subscription, fee, or paid service |

## A tour of the archive

Open the page and you're in **the restricted section** — six candlelit
alcoves, one per school of magic:

🏠 Personal apps · 🗂️ Life admin · 💸 Money & budgeting ·
🎬 Creative & media · 🧠 Knowledge work · ⚙️ Dev workflows

- **Tomes** — each spell is a leather-bound book stacked in its alcove.
  Thicker spine = higher score. Gilt page-edges mark the money-savers.
  This week's new arrivals **glow golden** until fresher ones land.
- **Open a tome** (click it) for the full entry: what it is, a vivid
  example, its criteria badges, sources — and the **📜 recipe**: how to
  cast it yourself, what tools you need, and whether it's a
  `one-evening`, `weekend`, or `ongoing` casting.
- **The month drawers** — a cabinet below with one drawer per month.
  Pull one open to see everything discovered that month, sortable by
  score or recency. At each month's end the archive's librarian leaves a
  **🪶 note** in the drawer: the month's themes, what's rising, the best
  find.
- **Filters & search** — chips for each criterion and a search box that
  reads titles, summaries, and recipes. Both work on the shelves and the
  drawers at once.

## Using it

```sh
cd claude-code-use-cases
python3 -m http.server 8124
# open http://localhost:8124
```

That's it — no build step, no dependencies. The page is one HTML file
reading one JSON file.

### The weekly owl 🦉

A scheduled Claude Code task (`weekly-claude-code-usecases`, Mondays ~9am)
does the collecting:

1. Researches the past week's finds across several angles (blogs, Reddit,
   HN, roundups) — personal & productivity only
2. Scores candidates and **dedupes** against everything already shelved
   (same spell reworded ≠ new spell; sources merge into existing tomes)
3. Shelves 3–8 genuinely new spells, each with a replication recipe
4. Validates, commits, and sends the week's **top 5 to Telegram**
5. On the month's last run, writes the librarian's note; on the year's
   last run, binds the **2026 annual report**

> The task runs while the desktop app is open; if it's closed on Monday
> morning, it runs on next launch.

### Telegram setup (once)

1. Message **@BotFather** → `/newbot` → copy the token
2. `cp config.example.json config.json` and paste the token in
3. Send your new bot any message (it can't speak first)
4. `python3 send_telegram.py --get-chat-id` → put the id in `config.json`
5. Test: `python3 send_telegram.py` — the owl should arrive instantly

`config.json` is gitignored; the token never leaves your machine.

## Shelving a spell by hand

Add an entry to `data/usecases.json`:

```json
{
  "id": "the-example-spell",
  "category": "Life admin",
  "title": "The Example Spell",
  "summary": "What it does and why it's worth shelving, in 2-3 sentences.",
  "example": "One vivid, specific instance of it in the wild.",
  "recipe": {
    "how": "How to cast it yourself, in 2-3 sentences.",
    "tools": ["Claude Code", "whatever else"],
    "difficulty": "one-evening"
  },
  "criteria": { "creative": false, "useful": true, "fun": false,
                "painPoint": true, "money": false },
  "score": 2,
  "sources": [{ "title": "Where you found it", "url": "https://..." }],
  "week": "2026-W29",
  "added": "2026-07-15"
}
```

Then validate before committing:

```sh
python3 check_usecases.py
```

It enforces the schema: `score` must equal the count of true criteria,
`category` and `difficulty` must come from the fixed lists, ids must be
unique, every spell needs a source and a recipe.

## House rules

- **No build step.** Plain HTML/CSS/JS + JSON; scripts are stdlib-only
  Python. If it needs `npm install`, it doesn't belong here.
- **The data file is the truth.** The page renders whatever
  `data/usecases.json` says; nothing is hardcoded twice.
- **Small commits**, validated by `check_usecases.py` first.

## The files

| File | Role |
|------|------|
| `index.html` | The archive — shelves, drawers, filters, search, modal |
| `data/usecases.json` | Every spell + the librarian's notes |
| `check_usecases.py` | Schema validator (run before committing) |
| `send_telegram.py` | The owl — sends the weekly top 5 |
| `config.example.json` | Template for your Telegram credentials |

---

*Started July 2026. The goal: open twelve drawers in December and read
back a year of small, castable magic.* 🕯️
