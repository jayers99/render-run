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

  - Run: `poetry -C extensions/render-run run render-run --help`

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

- **Input (current):** a text file of ideas/prompts, one per line (blank lines and `#` comments ignored)
- **Command:** `render-run prepare --in <prompts.txt> --out <run_dir> [--expand/--no-expand] [--providers ...]`
- **Outputs (in `<run_dir>`):**
  - `manifest.json` (run metadata + list of items)
  - `expanded_prompts.txt` (one expanded prompt per line)

Create-domain direction (planned): use a **Markdown idea doc** owned/validated by Create, with a minimal per-idea contract (`idea_id` + `prompt`). See the Create opinion doc: `docs/opinions/create/render-run.md`.

### Default Output Location (Recommended)

If you omit `--out`, Render Run derives an output directory using your user-level generated content root:

`<generated_root>/<domain>/<project>/runs/<run_id>`

Example:

`~/icloud/praxis-generated-content/create/xmas-cards-2025/runs/20251226-235959`

Config precedence:

1. `PRAXIS_GENERATED_CONTENT_ROOT`
2. `~/.config/praxis/config.json` with `{ "generated_content_root": "..." }`
3. Default: `~/icloud/praxis-generated-content`

### Image Generation (MVP)

MVP supports a single provider implementation: a **gcloud-driven CLI wrapper**.

- Generate images: `render-run generate --manifest <run_dir>/manifest.json --provider gcloud`
- Configure the provider command via `RENDER_RUN_GCLOUD_IMAGE_COMMAND_TEMPLATE`.

This is intentionally abstract so we can add:

- OpenAI CLI (later)
- OpenAI API (later)

## License

MIT (see `LICENSE`).
