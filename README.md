# Render Run

Render Run is a small, agent-friendly **batch image generation runner**.

**Domain:** Code

Render Run is intended to be a reusable utility that **Create-domain projects call** to generate images (across providers) and save results + manifests for review.

The intended workflow:

1. Start with a list of short image ideas.
2. Expand each idea into a detailed image prompt.
3. Submit each prompt to multiple image generation providers.
4. Save all images + a manifest to an output folder for review.

This repo is scaffolded as a minimal Python CLI (Typer + Poetry).

## Use From Create Projects

Pick one:

- **As a standalone CLI (local checkout / submodule)**

  - Run: `poetry -C examples/code/render-run run render-run --help`

- **As a dependency (recommended once published as its own repo)**
  - Add via Poetry (example): `poetry add git+https://github.com/jayers99/render-run.git`
  - Then run from the Create project: `poetry run render-run --help`

## Quickstart (Render Run repo)

- Use Python 3.12.x
- Install dependencies: `poetry install`
- Run help: `poetry run render-run --help`
- Smoke test: `poetry run render-run hello`
- Prepare a run manifest: `poetry run render-run prepare --in prompts.txt --out .tmp/run-001`
- Run tests: `poetry run pytest`

## Create → Code Contract (MVP)

Render Run establishes a minimal, stable interface for Create projects:

- **Input:** a text file of ideas/prompts, one per line (blank lines and `#` comments ignored)
- **Command:** `render-run prepare --in <prompts.txt> --out <run_dir> [--expand/--no-expand] [--providers ...]`
- **Outputs (in `<run_dir>`):**
  - `manifest.json` (run metadata + list of items)
  - `expanded_prompts.txt` (one expanded prompt per line)

Provider calls and image downloads are intentionally not implemented yet.

## License

MIT (see `LICENSE`).
