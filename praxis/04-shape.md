# Shape: Render Run

**Stage:** Shape  
**Domain:** Code

---

## Target Experience

1. Create project prepares a `prompts.txt` (ideas per line).
2. Optionally attach reference bundles (subjects, style swatches, object close-ups) that live in the Create project.
3. Run `render-run prepare --in prompts.txt --out ./runs/<timestamp>` and pass metadata (prompt slots, reference file paths/URLs, desired specificity level).
4. The command writes `manifest.json` + `expanded_prompts.txt`, recording providers + prompts + reference metadata.
5. Subsequent commands (`render-run generate --provider dalle`, `--provider gemini`, etc.) read the manifest, apply the appropriate prompt tier (loose vs strict), and populate provider-specific folders, noting which reference bundle was used.
6. Reviewers open the run folder, inspect artifacts, and feed winners + learnings back into Create workflows.

## Architecture Overview

- **CLI (Typer):** thin command definitions (`prepare`, future `generate`/`review`).
- **Application layer:** services like `prompt_expander_service`, `batch_plan_service`, future `provider_runner_service`.
- **Adapters:** provider-specific modules (OpenAI, Google, local SD) behind consistent interfaces.
- **Artifacts:** run directory with manifests, expanded prompts, provider output subfolders, logs.

## Interfaces / Contracts

- `prompts.txt`: UTF-8, `#` ignored, blank lines skipped.
- `manifest.json`: contains schema version, metadata, `items[]` with:
  - `id`, `idea`, `prompt`
  - `prompt_slots` (subject, action, mood, tone, camera, palette, etc.)
  - `reference_assets` (people likenesses, style samples, object shots)
  - `specificity_level` (e.g., `loose`, `balanced`, `strict`) to signal how constrained the prompt is
  - `providers`
- `expanded_prompts.txt`: human-readable list used for manual review or copy-paste into UI.
- Future `results/<provider>/<id>_<slug>.png`: canonical naming for generated images.
- Variation strategy: manifest tracks variation indices so Create can compare e.g. `subject=A + style=B + mood=loose` vs `subject=A + style=C + mood=strict`.

## Data & Config

- Environment variables for API keys (e.g., `OPENAI_API_KEY`, `GOOGLE_API_KEY`).
- Optional `render-run.toml` for defaults (providers, concurrency, storage paths) — deferred until needed.

## Risks / Mitigations

- **Provider churn:** isolate adapters; keep manifest schema stable.
- **Credential sprawl:** document env var usage + secrets handling.
- **Large runs:** design for incremental writes and resumable manifests.
