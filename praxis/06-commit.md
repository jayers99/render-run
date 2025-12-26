# Commit: Render Run

**Stage:** Commit  
**Domain:** Code

---

## Commit Decision

Proceed with building Render Run as the official batch image runner for Praxis Create projects.

## Scope Lock (v0)

- CLI commands: `hello` (smoke), `expand`, `prepare` (done), `generate <provider>` (planned), `review` (planned).
- Manifest schema v0.1 locked; backward-compatible additions only.
- Providers: start with OpenAI DALL·E + Google Gemini/Imagen. Others follow via adapters.

## Success Criteria

- Create project can run `prepare` + at least one provider command end-to-end, producing artifacts in a timestamped folder.
- Manifest includes per-provider status entries and filenames.
- README documents how Create projects depend on Render Run including env vars.
- Tests (unit + CLI) cover core workflows; CI runs `pytest`, `ruff`, `mypy`.

## Timeline (high-level)

1. **Week 1:** Land governance + `prepare` contract (complete).
2. **Week 2:** Implement OpenAI adapter + `generate --provider openai`.
3. **Week 3:** Implement Google adapter + manifest status updates.
4. **Week 4:** Add review helpers, finalize docs, publish repo publicly.

## Risks & Mitigation

- **API changes:** track provider SDK versions, wrap responses.
- **Rate limits:** add throttling + exponential backoff utilities.
- **Secrets leakage:** use env vars + `.env.example`, avoid committing tokens.
