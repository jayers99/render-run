# Sense: Render Run

**Stage:** Sense  
**Domain:** Code

---

## Patterns Observed

- Create projects repeatedly hand-roll scripts to fan prompts across providers, then manually rename/download artifacts.
- Existing VS Code extensions focus on single-image UX; they rarely expose batch tooling or manifest outputs.
- Copilot / agent workflows need deterministic file contracts to stay auditable.

## Problem Statement

Creative projects need a dependable way to turn curated prompts into multi-provider runs without leaving the Praxis workflow. Today that step is ad-hoc, error-prone, and slow to review.

## User Types

- **Create domain leads:** define prompts/memories, expect a folder of results with traceability.
- **Code domain maintainers:** own the Render Run utility, ensure CLI/API stays stable.
- **Agent operators:** run Render Run via Copilot/MCP tasks, want clear commands + artifacts.

## Ownership Boundaries (Create vs Render Run)

- **Lives in Create:**
  - Curating reference bundles (likeness photos, style palettes, object details).
  - Designing prompt building blocks (subject, action, mood, tone, camera, palette) and mixing/matching them per recipient.
  - Exploring prompt spectra (loose/serendipitous vs. tightly specified) and deciding which variations to pursue.
- **Lives in Render Run (Code):**
  - Accepting structured prompt payloads from Create projects (including reference asset paths/URLs).
  - Fan-out execution (CLI/API calls) and tracking which variation came from which template/slot.
  - Capturing outputs/metadata so Create can judge which combos worked.

## Emerging Principles

1. **Manifest-first:** every run should leave behind machine-readable context (prompts, providers, timestamps).
2. **Provider-agnostic:** pluggable backends so we can add Gemini, DALL·E, Stable Diffusion, etc.
3. **CLI-native:** prefer Typer commands that agents & humans can call; avoid bespoke UI.
4. **Praxis-aligned:** document lifecycle decisions inside `/praxis` so Create teams can audit.

## Opportunities

- Build a “prepare” phase that Create projects can call before any API keys are configured (dogfooding manifest contract now).
- Later add `generate` commands per provider that reuse the same manifest.
- Offer recipe snippets (e.g., `render-run prepare && render-run generate --provider dalle`).
