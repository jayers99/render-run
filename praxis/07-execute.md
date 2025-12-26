# Execute: Render Run

**Stage:** Execute  
**Domain:** Code

---

## Work Breakdown

| Item | Status | Notes |
| --- | --- | --- |
| Typer CLI scaffold + tests | ✅ | `hello`, `expand`, Typer wiring, pytest coverage |
| `prepare` command + manifest schema | ✅ | Writes `manifest.json`, `expanded_prompts.txt` |
| Provider abstraction + OpenAI adapter | ⏳ | Define interface, implement DALL·E calls |
| Google adapter (Gemini/Imagen) | ⏳ | Research correct endpoint + auth |
| Run folder auto-naming + review helper | ⏳ | Provide `--out` default + summary command |
| CI setup (lint + type + tests) | ⏳ | GitHub Actions / reusable workflow |

## Verification

- `poetry run pytest` (CLI + unit)
- `poetry run mypy src` (once provider interfaces exist)
- `poetry run ruff check src tests`
- Manual test: run `render-run prepare --in samples/prompts.txt --out .tmp/run-test`

## Dependencies / Blockers

- Need clarity on Google image-generation API for personal vs enterprise access.
- Need API keys before writing provider integration tests (mock until then).

## Deployment Plan

- Publish repo publicly once provider commands land.
- Tag releases (`v0.1.0-prep`, `v0.2.0-openai`, etc.)
- Document upgrade/migration steps when manifest schema changes.
