# Formalize: Render Run

**Stage:** Formalize  
**Domain:** Code

---

## Solution Overview

Render Run is a Typer-based CLI + lightweight library that prepares and (eventually) executes batch image generation runs. It exposes manifest-driven workflows compatible with Create-domain projects and agent automation.

## Objectives

1. Provide a deterministic contract between Create projects and provider adapters.
2. Support multiple providers per run without duplicating prompt expansion work.
3. Keep the tool simple enough to run locally or inside CI/agents.

## Scope

- **In scope:**
  - `prepare` command (landed) producing manifests + expanded prompts.
  - Provider abstraction layer + first-party adapters (OpenAI Images, Google Gemini/Imagen).
  - `generate` command that consumes manifests, calls providers, writes artifacts.
  - `review`/`status` helpers for summarizing output folders.
- **Out of scope (v0):**
  - UI front-ends
  - Long-running job orchestration
  - Integrated asset hosting

## Architecture Summary

- CLI entrypoints call application services.
- Manifest schema (v0.1) stored as JSON for easy diffing.
- Provider adapters share a `ProviderRunner` protocol (TBD) with `prepare_request`, `execute`, `record` steps.
- Tests rely on `pytest` + fixture-generated temp dirs.

## Dependencies

- Python 3.12.x
- Typer, Rich (via Typer), future HTTP clients (httpx/requests) per provider.
- Mypy + Ruff for static analysis.

## Non-Functional Requirements

- All commands must run offline up through `prepare` (no provider calls required).
- Provider commands must support dry-run mode and structured logging.
- Default run directories live under `.tmp/runs/<timestamp>` when not specified.

## Testing Strategy

- Unit tests for services (prompt expansion, manifest writer).
- CLI integration tests for key commands using Typer's `CliRunner`.
- Contract tests for provider adapters using VCR-like fixtures or mocked HTTP clients.
