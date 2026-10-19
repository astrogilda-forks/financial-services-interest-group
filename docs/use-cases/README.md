# Use cases

One file per finance use case, written in prose so the group can review it before anything is built from it. Each case later gains conformance vectors, and CI checks those against a pinned release of the record corpus, so a case states a behaviour that a verifier can be tested on.

## File format

Name the file `docs/use-cases/<short-slug>.md` and copy [TEMPLATE.md](TEMPLATE.md). A case carries:

- a title line (`# ...`);
- a `Status:` line, one of `draft` (open for comment), `reviewed` (the group has checked the prose) or `vectorised` (it has conformance vectors);
- a `Vectors:` line, empty until the case is vectorised, then the member ids of the pinned corpus that test it (for example `A1, A9`);
- the sections `## Scenario`, `## Parties and authority`, `## What happens`, `## What the record must show` and `## Open questions`, in that order.

`tools/check_use_cases.py` checks this on every pull request. A `vectorised` case must list at least one vector, and every listed id must exist in the corpus release pinned in [requirements.txt](requirements.txt).

## The pinned corpus

The record corpus is [agent-evidence-vectors](https://github.com/probityai/agent-evidence-vectors) `vectors-agent-audit-record`, pinned by exact version in `requirements.txt`. CI installs that release and replays the corpus, so the vectors a case lists are the ones that release ships. Dependabot opens a pull request for each new release, and that release's notes list the members it changed.

Run the checks locally:

```sh
pip install -r docs/use-cases/requirements.txt
python tools/check_use_cases.py
agent-evidence-vectors --corpus vectors-agent-audit-record
```
