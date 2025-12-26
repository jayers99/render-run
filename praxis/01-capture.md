# Capture: Render Run

**Stage:** Capture  
**Domain:** Code

---

## Goals

- Provide a reusable CLI/agent utility that Create projects can call to batch-generate images.
- Standardize how prompts, providers, and artifacts are organized (manifest-first workflow).
- Ensure the project stays public, lightweight, and Python-based (Typer + Poetry + Python 3.12).

## Raw Inputs

- Brain dump describing the desire to orchestrate multi-provider image generation (Gemini + DALL·E first).
- Research notes comparing VS Code extensions (Prompt2Image, VisionText, CoCover, ComfyUI helpers) and gaps.
- Praxis AI create-domain workflows (e.g., `xmas-cards-2025`) that need automation.

## Constraints / Requirements

- Operate as a Code-domain utility that Create projects can depend on without bundling UI.
- Determine whether to call provider **CLIs** (e.g., Gemini CLI, `gpt-image`-style tools) or integrate **direct APIs**; document trade-offs (setup effort, rate limits, portability) before locking in.
- Favor built-in GitHub Copilot / MCP access where possible, otherwise hit provider APIs or blessed CLIs.
- Maintain deterministic file outputs (manifest + expanded prompts) for human review.
- Python 3.12.x runtime, Poetry-managed dependencies, MIT License.
- Credential handling preference: pull API secrets from macOS Keychain (vs `.env` files) when running locally.

## Prior Art & References

- VS Code marketplace extensions: Prompt2Image (Pollinations), VisionText (Pollinations), CoCover (OpenAI DALL·E), Cushy Studio (ComfyUI), etc.
- Existing Praxis templates (`template-python-cli`) for repo structure, testing, and governance.
- Praxis documentation on lifecycle stages and AI guardrails.

## Open Questions

- Which Google/Gemini endpoint actually supports image generation for this workflow (Imagen vs Gemini 3)?
- How should provider credentials and rate limits be modeled in the CLI UX?
- Do we need native support for parallelism, or is sequential good enough for v0?
- Should Render Run wrap official provider CLIs or call REST/SDK APIs directly? If CLIs win, which ones (Gemini CLI, OpenAI `gpt-image`, etc.) and how do we bundle/install them?
- What is the plan for provisioning API keys (after deciding CLI vs API)? e.g., store in macOS Keychain + surface via env vars at runtime.
