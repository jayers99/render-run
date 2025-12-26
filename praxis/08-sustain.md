# Sustain: Render Run

**Stage:** Sustain  
**Domain:** Code

---

## Operational Plan

- **Release cadence:** cut a tagged release whenever a provider adapter or manifest schema change ships.
- **Issue triage:** weekly review of GitHub issues; label by provider and lifecycle stage.
- **Docs:** keep README + Praxis files updated when stage or scope changes.

## Observability & Metrics

- Track number of run folders generated per week (simple counter in CLI logs once available).
- Collect provider success/failure counts in manifest for later analysis.
- Optional: add telemetry hook (opt-in) for anonymized usage counts.

## Maintenance Tasks

- Dependency bumps (Poetry) each quarter or when security advisories appear.
- Verify provider APIs still work; update adapters/tests when new models roll out.
- Refresh Praxis stage documentation when we move beyond Explore/Shape.

## Exit Criteria

- A future `09-close.md` will document sunset decisions once Render Run is superseded or merged into another utility.
