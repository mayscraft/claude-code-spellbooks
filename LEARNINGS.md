# Learnings — founding session, 2026-07-15

The day this archive was built, from first web search to migrated
scheduled task. Written for future May (and future librarians) so the
decisions don't have to be re-derived.

## What got built, in one day

Research on Claude Code use cases → a JSON-backed tracker → a themed
static app ("Claude Code Personal Spellbooks") → a Telegram bot → a
weekly research agent → three rounds of redesign → a full rescope. All
static/no-build: one HTML file, one JSON file, two stdlib Python scripts.

## Product decisions and why

- **Scope narrowed on purpose (the day's biggest decision).** Started as
  "all Claude Code use cases" incl. money-making; cut to personal &
  productivity only after seeing that ambitious indie-hacker material
  (e.g. "$12K in month one") isn't actionable for one person's evenings.
  Three business entries were evicted. Rule of thumb: every spell must be
  castable by one person in an evening or a weekend.
- **💰 means *saves* money, not makes money** — consistent with the
  personal scope (ditching a subscription counts; MRR does not).
- **Recipes make entries actionable.** Every spell carries how/tools/
  difficulty. A collection of 150 headlines < a spellbook of 150 things
  you could actually cast. This was ranked the single most useful
  improvement of the day.
- **Chosen direction: workshop, not commons.** The inward path (track
  what May actually tries; status ribbons want-to-try → tried → adopted)
  beat the outward path (public directory chasing search traffic).
  Ribbons are designed but NOT built yet. Ahrefs data says the outward
  path stays open: "claude code use cases" ~300 US searches/mo, KD ~9.
- **Theme is a feature.** The Harry Potter voice (tomes, drawers, the
  librarian, the owl, the scrying glass) is used consistently in UI copy,
  Telegram messages, and the weekly agent's writing voice.

## How the weekly agent is designed

- **Multi-angle research beats one query** — listicles recycle; concrete
  sourced projects live in per-angle searches (routines/health, life
  uses, home/hobby, saving money).
- **Dedupe has three layers:** (1) agent reads the whole JSON first and
  skips covered concepts even reworded; (2) related variations fold into
  one spell with multiple sources; (3) validator hard-fails duplicate ids
  at commit time.
- **Don't pad a dry week** — an empty week is recorded as empty; the bar
  doesn't drop.
- **Month-end librarian's notes** are write-or-replace (never append a
  second note for a month — the validator enforces uniqueness). The
  annual report assembles on the last run of December.
- **Simulate before trusting automation.** A hand-run of the weekly round
  and of the librarian's note caught two real bugs before Monday could:
  a duplicate-note append path and a missing category in the task's
  schema instructions.

## Process learnings (the hard-won ones)

- **The session's folder matters more than it looks.** Scheduled tasks,
  permission grants, and per-project memory bind to the folder a session
  was opened in and can't be re-pointed. The weekly task was born in the
  Trip Planner session and had to be migrated (recreated as
  `weekly-personal-spellbooks` from a session opened here, old task
  deleted). A global note now exists in `~/.claude/CLAUDE.md`: confirm
  the folder before starting project work.
- **A validator is cheap insurance for agent-written data.** Every schema
  rule added (score math, category/difficulty enums, unique ids, note
  uniqueness) turns a silent agent mistake into a loud commit failure.
- **The task's instructions and the repo's docs should point at each
  other.** The agent reads README.md; the repo's CLAUDE.md mirrors the
  same rules so human sessions and the scheduled agent can't drift apart.
- **Scheduled tasks run only while the app is open** — a sleeping Mac
  delays the owl, never loses it; the run catches up on wake/launch.
- **Absolute paths in agent prompts** are what make a task safe to run
  from any starting folder.

## Open threads (deliberately not done yet)

- Status ribbons + "want to try" flow — the workshop hinge; next big move
- Monthly "cast one spell" ritual, with the agent scaffolding a starter
- GitHub Pages publish (phone access; the outward path if ever wanted)
- Search will earn its keep around ~60 spells (est. September)
