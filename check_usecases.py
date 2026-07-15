#!/usr/bin/env python3
"""Validate data/usecases.json before committing / sending.

Checks: required fields, criteria keys, score = number of true criteria,
unique ids, week format YYYY-Www, http(s) source URLs, ISO dates.
Exit 0 on success, 1 with messages on failure. Stdlib only.
"""
import json
import re
import sys
from pathlib import Path

DATA = Path(__file__).parent / "data" / "usecases.json"
CRITERIA = ["creative", "useful", "fun", "painPoint", "money"]
CATEGORIES = ["Personal apps", "Life admin", "Money & budgeting",
              "Creative & media", "Knowledge work", "Dev workflows"]
DIFFICULTIES = ["one-evening", "weekend", "ongoing"]
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
REQUIRED = ["id", "title", "category", "summary", "criteria", "score", "recipe", "sources", "week", "added"]


def main() -> int:
    errors = []
    try:
        doc = json.loads(DATA.read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read {DATA}: {e}")
        return 1

    if not DATE_RE.match(doc.get("updated", "")):
        errors.append("top-level 'updated' must be YYYY-MM-DD")

    usecases = doc.get("usecases", [])
    if not usecases:
        errors.append("no usecases found")

    seen_ids = set()
    for i, uc in enumerate(usecases):
        label = uc.get("id", f"#{i}")
        for field in REQUIRED:
            if field not in uc:
                errors.append(f"{label}: missing field '{field}'")
        if uc.get("category") not in CATEGORIES:
            errors.append(f"{label}: category must be one of {CATEGORIES}")
        crit = uc.get("criteria", {})
        if sorted(crit.keys()) != sorted(CRITERIA):
            errors.append(f"{label}: criteria keys must be exactly {CRITERIA}")
        elif not all(isinstance(v, bool) for v in crit.values()):
            errors.append(f"{label}: criteria values must be booleans")
        else:
            expected = sum(crit.values())
            if uc.get("score") != expected:
                errors.append(f"{label}: score {uc.get('score')} != computed {expected}")
        rec = uc.get("recipe")
        if not isinstance(rec, dict):
            errors.append(f"{label}: recipe must be an object with how/tools/difficulty")
        else:
            if not rec.get("how"):
                errors.append(f"{label}: recipe.how must be a non-empty string")
            tools = rec.get("tools")
            if not tools or not all(isinstance(t, str) and t for t in tools):
                errors.append(f"{label}: recipe.tools must be a non-empty list of strings")
            if rec.get("difficulty") not in DIFFICULTIES:
                errors.append(f"{label}: recipe.difficulty must be one of {DIFFICULTIES}")
        if uc.get("id") in seen_ids:
            errors.append(f"{label}: duplicate id")
        seen_ids.add(uc.get("id"))
        if not WEEK_RE.match(uc.get("week", "")):
            errors.append(f"{label}: week must be YYYY-Www (e.g. 2026-W29)")
        if not DATE_RE.match(uc.get("added", "")):
            errors.append(f"{label}: added must be YYYY-MM-DD")
        srcs = uc.get("sources", [])
        if not srcs:
            errors.append(f"{label}: at least one source required")
        for s in srcs:
            if not s.get("title") or not str(s.get("url", "")).startswith(("http://", "https://")):
                errors.append(f"{label}: each source needs a title and http(s) url")

    for i, note in enumerate(doc.get("librarianNotes", [])):
        if not MONTH_RE.match(note.get("month", "")):
            errors.append(f"librarianNotes[{i}]: month must be YYYY-MM")
        if not note.get("text"):
            errors.append(f"librarianNotes[{i}]: text must be non-empty")

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {DATA.name}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(usecases)} use cases, {len({u['week'] for u in usecases})} week(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
