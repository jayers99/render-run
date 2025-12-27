# Explore: Render Run

**Stage:** Explore  
**Domain:** Code

---

## Options Considered

| Option                                                 | Summary                                        | Pros                                                   | Cons                                                                   |
| ------------------------------------------------------ | ---------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------- |
| VS Code extensions (Prompt2Image, VisionText, CoCover) | Use marketplace tooling directly inside editor | Zero setup, UI-driven                                  | Single-provider, no batch/manifest, closed UX                          |
| MCP-only workflow                                      | Expose image generation as an MCP tool         | Integrates with agents, reuse tokens                   | Requires writing provider integrations anyway, stateful outputs harder |
| Dedicated Python CLI (Render Run)                      | Ship a Typer CLI + manifest contract           | Deterministic outputs, easy to test, works with agents | Must implement provider adapters, doc/maintain                         |
| ComfyUI/Automatic1111 automation                       | Lean on existing SD pipelines                  | Powerful for SD models, visual graph                   | Heavy infrastructure, not aligned with initial provider targets        |

### Provider Integration Strategy: CLI Wrappers vs Direct APIs

| Aspect                  | CLI Wrappers (`gcloud`, OpenAI CLI, etc.)                                                                                 | Direct API / SDK Calls                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Setup effort            | Install vendor CLI, auth once (often OAuth or `gcloud auth`). Less code, but tool must be present on every machine/agent. | Need API keys + HTTP client code. More coding upfront, but only dependency is Python libs + env vars. |
| Portability             | Depends on OS support + CLI availability. Harder to run inside minimal containers/CI without installing vendor tool.      | Works anywhere Python runs; easier to vendor in containers/CI.                                        |
| Feature coverage        | Usually limited to what CLI exposes (may lag behind API features). Batch/async options vary.                              | Full control over API parameters, concurrency, retries, new features first.                           |
| Rate limiting / retries | Must rely on CLI behavior; limited hooks for backoff/metrics.                                                             | We own retry strategy, telemetry, manifest updates.                                                   |
| Credential management   | CLI may integrate with system keychain/`gcloud` config automatically (nice for local dev).                                | Need to supply keys (env vars, Keychain-export). But we can still fetch from Keychain and inject.     |
| Agent friendliness      | Agents must shell out to CLI; path issues inside remote sandboxes.                                                        | Agents just call Python functions; easier to stub/mock in tests.                                      |

**Current decision (temporary / MVP):** start with a **CLI wrapper** using `gcloud` first.

- Rationale: fastest path to a working end-to-end run in a local macOS environment, and it aligns with existing `gcloud auth` flows.
- This is explicitly not a forever decision; the architecture should support adding OpenAI CLI and direct APIs later.

### Status Note (Governance)

Some provider abstraction and a `gcloud` CLI adapter exist in the codebase already.

- Treat this as **exploratory prototype code**, not a finalized contract.
- Do not assume the UX, config keys, or manifest schema are stable until we explicitly move through Shape → Formalize.

## Spikes & Findings

- Tested feasibility of `typer` + `pytest` skeleton: fast iteration, strong typing with mypy.
- Verified Python 3.12 via pyenv/Poetry works on macOS.
- Confirmed manifest/expanded-prompt generation is trivial to implement now and unblocks Create projects immediately.

## Decisions

- Proceed with the dedicated CLI path (Render Run) and keep it public.
- Land a `prepare` command ASAP to prove the contract before adding provider integrations.
- Document Praxis lifecycle inside the repo so future contributors follow the same governance.

### Decision: MVP Provider Path

- MVP provider execution: `gcloud` CLI wrapper
- Future additions (not yet committed): OpenAI CLI adapter, OpenAI API adapter

## Outstanding Research

- Best public API for “Gemini image generation” (Imagen vs Gemini vs Vertex AI).
- Evaluate whether Copilot subscription exposes useful image models without extra API calls.
- Determine concurrency + retry strategy for future provider commands.
