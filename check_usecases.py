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
WEEK_RE = re.compile(r"^\d{4}-W\d{2}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
REQUIRED = ["id", "title", "summary", "criteria", "score", "sources", "week", "added"]


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
        crit = uc.get("criteria", {})
        if sorted(crit.keys()) != sorted(CRITERIA):
            errors.append(f"{label}: criteria keys must be exactly {CRITERIA}")
        elif not all(isinstance(v, bool) for v in crit.values()):
            errors.append(f"{label}: criteria values must be booleans")
        else:
            expected = sum(crit.values())
            if uc.get("score") != expected:
                errors.append(f"{label}: score {uc.get('score')} != computed {expected}")
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

    if errors:
        print(f"FAIL: {len(errors)} problem(s) in {DATA.name}:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"OK: {len(usecases)} use cases, {len({u['week'] for u in usecases})} week(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
