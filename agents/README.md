# agents/ — the powerup rack

one folder, one concern per file. a future session must never re-figure the
system from scratch or drift the design: load the modules the task needs,
skip the rest. each file is a complete unit — laws, steps, examples.

| file | what it powers |
|------|----------------|
| [00-laws.md](00-laws.md) | the non-negotiables. every other module assumes them. |
| [01-page-recipe.md](01-page-recipe.md) | how a page gets created: collect → verify → data → build. |
| [02-data-model.md](02-data-model.md) | the database schema, versions, series, categories, attic. |
| [03-tags-infra.md](03-tags-infra.md) | the tag system: genre / sub-genre / category / content / players / platform / era / status. |
| [04-collections.md](04-collections.md) | collections and meta-collections: design, wiring, rules. |
| [05-media.md](05-media.md) | galleries: 10 images + 3 videos, URL-only law, media-not-found. |
| [06-search-infra.md](06-search-infra.md) | search, facets, sorts, random — the store UX and its engine. |
| [07-templates.md](07-templates.md) | the template law: build.py renders everything, edit once, expand forever. |
| [08-testing.md](08-testing.md) | the QA battery: what must pass before any push. |
| [09-expansion.md](09-expansion.md) | endless growth: adding hundreds of rows without hallucination. |

reading order for a cold start: 00 → 01 → 07 → 08. the rest load on demand.
