"""Check the use-case files in docs/use-cases against the format in its README.

Each case needs a title, a Status line, a Vectors line and five sections in
order. A vectorised case must list vectors, and every listed id must be a
member of the agent-audit-record corpus in the installed agent-evidence-vectors
release, which docs/use-cases/requirements.txt pins.
"""

from __future__ import annotations

import json
import re
import sys
from importlib import resources
from pathlib import Path

CASES = Path(__file__).resolve().parent.parent / "docs" / "use-cases"
SKIP = {"README.md", "TEMPLATE.md"}
SECTIONS = [
    "## Scenario",
    "## Parties and authority",
    "## What happens",
    "## What the record must show",
    "## Open questions",
]
STATUSES = {"draft", "reviewed", "vectorised"}


def corpus_ids() -> set[str]:
    """Return the member ids (draftId) of the installed agent-audit-record corpus."""
    root = resources.files("agent_evidence_vectors") / "corpora" / "vectors-agent-audit-record"
    manifest = json.loads((root / "MANIFEST.json").read_text(encoding="utf-8"))
    return {v["draftId"] for v in manifest["vectors"]}


def check(path: Path, known: set[str]) -> list[str]:
    """Return the format errors in one case file."""
    lines = path.read_text(encoding="utf-8").splitlines()
    errors: list[str] = []
    if not lines or not lines[0].startswith("# "):
        errors.append("the first line must be a '# ' title")
    status = next((ln for ln in lines if ln.startswith("Status:")), None)
    vectors = next((ln for ln in lines if ln.startswith("Vectors:")), None)
    value = status.split(":", 1)[1].strip() if status else ""
    if value not in STATUSES:
        errors.append(f"Status must be one of {sorted(STATUSES)}, found {value!r}")
    if vectors is None:
        errors.append("missing the Vectors: line")
        ids: list[str] = []
    else:
        ids = [i for i in re.split(r"[,\s]+", vectors.split(":", 1)[1].strip()) if i]
    if value == "vectorised" and not ids:
        errors.append("a vectorised case must list at least one vector")
    errors += [f"vector {i} is not in the pinned corpus" for i in ids if i not in known]
    positions = [lines.index(s) if s in lines else -1 for s in SECTIONS]
    errors += [f"missing section {s!r}" for s, p in zip(SECTIONS, positions) if p < 0]
    found = [p for p in positions if p >= 0]
    if found != sorted(found):
        errors.append("the sections are out of order")
    return errors


def main() -> int:
    """Check every case file and print one line per error."""
    known = corpus_ids()
    cases = sorted(p for p in CASES.glob("*.md") if p.name not in SKIP)
    failed = 0
    for path in cases + [CASES / "TEMPLATE.md"]:
        for err in check(path, known):
            print(f"{path.relative_to(CASES.parent.parent)}: {err}")
            failed += 1
    print(f"checked {len(cases)} case file(s) and the template against {len(known)} corpus members; {failed} error(s)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
