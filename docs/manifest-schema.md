# Render Run — Manifest Schema (Draft)

This document defines the **target** `manifest.json` schema that Create projects can depend on.

Notes:

- Current implementation writes a minimal subset (`schema_version=0.1`, `idea`, `prompt`, `providers`).
- The schema below is the **planned** contract for provider execution + reference bundles + variations.

---

## Core Concepts

- **Run**: one invocation that prepares and/or generates outputs into a single directory.
- **Item**: one logical idea (“make a card for Joe…”).
- **Variant**: one concrete prompt composition for an item (different style ref, different strictness, different camera, etc.).
- **Provider job**: one provider execution for a specific variant.

---

## Proposed JSON Shape (v0.2)

```json
{
  "schema_version": "0.2",
  "created_at": "2025-12-26T19:20:30Z",
  "domain": "create",
  "project": {
    "name": "xmas-cards-2025",
    "path": "examples/create/xmas-cards-2025"
  },
  "input": {
    "prompts_file": "praxis/docs/prompts.txt",
    "notes": "Inner circle batch",
    "reference_root": "praxis/docs/references"
  },
  "providers": [
    {
      "id": "openai",
      "label": "OpenAI",
      "kind": "api",
      "models": {
        "image": "gpt-image-1"
      }
    },
    {
      "id": "google",
      "label": "Google",
      "kind": "api",
      "models": {
        "image": "imagen-or-gemini-image"
      }
    }
  ],
  "items": [
    {
      "id": 1,
      "title": "Joe — Padres towel mountain",
      "idea": "A Padres apron + a mountain of striped dish towels behind him",
      "prompt_slots": {
        "subject": "Joe, energetic, comedic vibe",
        "action": "posing proudly in a kitchen",
        "setting": "San Diego kitchen",
        "mood": "funny, warm",
        "style": "photo-real",
        "camera": "35mm, eye-level",
        "lighting": "soft indoor daylight",
        "palette": "Padres navy and gold"
      },
      "reference_assets": {
        "likeness": ["people/joe/joe-01.jpg"],
        "style": ["styles/minimalist-01.png"],
        "objects": ["objects/padres-apron.png", "objects/striped-towels.png"]
      },
      "variants": [
        {
          "id": "1a",
          "specificity_level": "balanced",
          "prompt": "<fully rendered prompt string>",
          "negative_prompt": "text overlays, watermarks, logos",
          "params": {
            "size": "1024x1024",
            "n": 2
          },
          "provider_jobs": [
            {
              "provider_id": "openai",
              "status": "planned",
              "artifacts": []
            },
            {
              "provider_id": "google",
              "status": "planned",
              "artifacts": []
            }
          ]
        }
      ]
    }
  ]
}
```

---

## Required vs Optional (MVP)

**Required**

- `schema_version`, `created_at`
- `items[].id`, `items[].idea`
- `items[].variants[].prompt`
- `items[].variants[].provider_jobs[].provider_id`

**Strongly recommended**

- `prompt_slots` (even if partially filled)
- `specificity_level`
- `reference_assets` (paths/URLs)

**Optional**

- `negative_prompt`
- `params` (size, n, seed, quality)
- `project` metadata (useful when runs are generated from many Create projects)

---

## Specificity Levels

- `loose`: minimal constraints; encourage model creativity.
- `balanced`: specify subject + key anchors; allow composition flexibility.
- `strict`: constrain composition, objects, mood, camera, and exclusions.

---

## Artifact Layout (Target)

```
<run_dir>/
  manifest.json
  expanded_prompts.txt
  openai/
    0001_joe_1a_001.png
  google/
    0001_joe_1a_001.png
```
