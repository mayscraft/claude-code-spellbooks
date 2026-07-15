# Claude Code Personal Spellbooks

A use-case tracker with a Harry Potter spellbook theme: collects notable
**personal & productivity** Claude Code use cases ("spells") scored
against five criteria — **creative, useful, fun, solves a pain point,
💰 saves money (bonus)** — shelves them in a candlelit archive on a
static page, and sends the weekly top 5 to Telegram.

Scope: things an individual can cast for themselves in an evening or a
weekend (daily routines, health, home, hobbies, knowledge, personal dev
workflows). Business-building, startup, and revenue plays are out of
scope — deliberately.

Static, no-build: plain HTML/CSS/JS + JSON, stdlib-only Python scripts.

## View the page

```sh
python3 -m http.server 8124
# open http://localhost:8124
```

## How it works

- `data/usecases.json` — the data store. Each entry has a `category` (one of:
  Personal apps, Life admin, Money & budgeting, Creative & media,
  Knowledge work, Dev workflows), criteria booleans (`money` = saves the
  caster money), a computed `score`
  (number of true criteria, money included as bonus), a `recipe`
  (`how` to replicate it, `tools` list, `difficulty`: one-evening /
  weekend / ongoing), sources, and an ISO week stamp (`2026-W29`).
  A top-level `librarianNotes` array holds month-end reflections
  (`{month: "YYYY-MM", text}`), written by the weekly task on the last
  run of each month.
- `index.html` — a candlelit archive: one alcove per category with use
  cases as stacked tomes (click one for details + its replication recipe;
  the newest week's tomes glow), a cabinet of monthly drawers (Jan–Dec)
  that open to show that month's collection and librarian's note, plus
  criteria filters and a search box that apply to both.
- `check_usecases.py` — validates the data (schema, unique ids, score
  matches criteria). Run after any edit to the JSON.
- `send_telegram.py` — formats the latest week's top 5 and posts it via
  the Telegram Bot API. `--dry-run` prints instead of sending.
- A **weekly scheduled Claude Code task** does live web research for new
  use cases, appends them (deduped) to the JSON, validates, and runs the
  Telegram send.

## Telegram setup (once)

1. In Telegram, message **@BotFather** → `/newbot` → follow prompts → copy the token.
2. `cp config.example.json config.json` and paste the token into `bot_token`.
3. Send your new bot any message (it can't message you first).
4. `python3 send_telegram.py --get-chat-id` → put the printed id into `chat_id`.
5. Test: `python3 send_telegram.py` — you should get the top 5 in Telegram.

`config.json` is gitignored — the token stays local.
