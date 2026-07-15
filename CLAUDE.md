# Claude Code Personal Spellbooks — project conventions

Static, no-build site: `index.html` + `data/usecases.json`, served with
`python3 -m http.server 8124`. **Read README.md first** — it explains the
app, the schema, and the weekly pipeline.

## Hard rules

- **No build step.** Plain HTML/CSS/JS + JSON only; tooling scripts are
  stdlib-only Python. Ask before adding any dependency, CDN script,
  external API, or git hook.
- **Scope: personal & productivity spells only.** No business-building,
  startup, or revenue-play entries. The `money` criterion means
  *saves the caster money*, not makes money.
- **Validate before committing data:** run `python3 check_usecases.py`
  (schema, unique ids, score = count of true criteria, one librarian's
  note per month).
- **Small commits, clear messages.** Commit identity is repo-local:
  `May Soon <301647653+mayscraft@users.noreply.github.com>` — never use
  the work email.
- **Voice:** UI copy and titles use the spellbook theme (spells, tomes,
  drawers, the librarian, the owl). Keep new copy in that voice.

## Moving parts

- `data/usecases.json` — all spells + `librarianNotes`; the page renders
  whatever it says.
- `send_telegram.py` — sends the latest week's top 5 (reads gitignored
  `config.json`; `--dry-run` to preview).
- Weekly scheduled task (Mondays ~9am) researches, shelves, validates,
  commits, and sends. Its instructions live in
  `~/.claude/scheduled-tasks/` — keep them in sync with this file's rules.

## Verifying UI changes

Serve the folder and exercise the page in a browser: tome modal, drawer
open/close, filters, search whisper, librarian's note. Check the console
is clean.
