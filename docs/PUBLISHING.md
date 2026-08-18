# Publishing a research post

This site is a **repurposing pipeline**, not a place to write from scratch. Every
research post starts from an existing `report.md` in the research repos and becomes
one `.mdx` file here. One research artifact → the web post → (downstream) an X
thread → a LinkedIn post. Never write a post that doesn't start from a repo artifact
— that's the quality control and the time control.

The fully-worked reference is [`capacity-curves.mdx`](../src/content/posts/capacity-curves.mdx).
Copy it when in doubt.

## The mechanical chain

```
report.md (exists)
  1. create src/content/posts/<slug>.mdx, prepend the frontmatter block below
  2. paste the report body under the frontmatter
  3. copy the figures it references into src/assets/research/<slug>/ and embed them
  4. convert any inline math to $…$ / $$…$$ for KaTeX
  5. pnpm dev, eyeball it; set draft:false; commit → CI deploys
  6. (manual, later) X thread + LinkedIn post linking back to the post
```

Local dev (Node comes from nvm — `nvm use` or `export PATH="$HOME/.nvm/versions/node/<v>/bin:$PATH"`):

```bash
corepack pnpm dev       # http://localhost:4321
corepack pnpm build     # astro check + build + pagefind (what CI runs)
```

## Frontmatter block

```yaml
---
title: "Strategy Capacity Curves"          # no "Project NN —" prefix
pubDatetime: 2026-07-08T00:00:00Z          # required
featured: true                              # optional — surfaces on the home page
draft: false                                # true hides it from build
tags: [capacity, transaction-costs, momentum]
description: "One-to-two sentence hook — this is the card summary, the OG text, and search snippet."
question: "The one-line research question." # optional — from the repo README table
headline: "The headline finding."           # optional — from the repo README table
status: "finding"                           # in-sample | validated | negative-result | finding | infra
dataSources: ["yfinance — 200 S&P names, 2010–2024 daily"]
repo: "https://github.com/.../capacity_study"
notebook: "https://github.com/.../notebooks/analysis.ipynb"   # optional
dashboard: "https://.../capacity"                             # optional
---
```

`title`, `pubDatetime`, `description` are required; everything else is optional and
degrades gracefully (a plain blog post can omit all the research fields). The
research fields render as the status badge + metadata block (top of post) and the
Resources footer (bottom) — see `src/components/ResearchMeta.astro` and
`ResourcesFooter.astro`.

### Status values

| status | use for |
|---|---|
| `finding` | a robust result/analysis (capacity, attribution, shadow prices) |
| `study` | a methodology / literature walk-through rather than a result of my own |
| `negative-result` | a plausible edge that failed OOS / deflation |
| `in-sample` | a first read, holdout still sealed |
| `validated` | survived the harness (**process only — keep the spec private**) |
| `infra` | tooling / platform build-outs (risk model, validation harness) |

## Figures

Reports reference figures by filename (`net_curves.png`). To embed them:

```bash
mkdir -p src/assets/research/<slug>
cp "/path/to/<project>/results/net_curves.png" src/assets/research/<slug>/
```

Then in the `.mdx`, use the `@/assets` alias (Astro optimizes + lightboxes it):

```md
![Descriptive alt text — say what the chart shows.](@/assets/research/<slug>/net_curves.png)
```

Always write real alt text; it's read aloud and indexed.

## Math (KaTeX)

`remark-math` + `rehype-katex` are wired in `astro.config.ts`. Use `$…$` inline and
`$$…$$` display. Convert unicode-y report notation to TeX:

- `Σ = B·F·Bᵀ + Δ` → `$\Sigma = B F B^{\top} + \Delta$`
- `IC(t)=c+a·e^{−λt}` → `$IC(t) = c + a\,e^{-\lambda t}$`
- `∝ √participation` → `$\propto \sqrt{\text{participation}}$`

## Publish-order ranking (strongest hooks first)

From the research repo's social-media strategy — publish roughly in this order so
the strongest counterintuitive hooks land first:

1. **capacity** — best signal (Sharpe 0.52) has $0 capacity; worst scales to $135M. ✅ *(done — the reference post)*
2. **oos-validation + alpha-engine** — selected IS Sharpe 0.35 → negative OOS; the trials-ledger deflation table.
3. **attribution** — a "market-neutral" book that was 97% factor, reconciled to 1e-17.
4. **shadow-prices** — what each constraint costs (momentum-neutrality 121 bps/yr).
5. **regime** — an HMM finds real regimes but they're risk control, not alpha.
6. factor-risk-model, alpha-decay, signal-combination, multiperiod-value,
   universe (survivorship), book-builder, risk-report, text-alpha.

## Guardrails (what NOT to publish)

- **Process, not alpha.** Methodology, infrastructure, negative results, bias
  quantifications — freely. Any signal that ever survives the harness: its
  spec/params go private. Publishing negatives is free; publishing positives gives
  away the edge.
- **No vendor-data redistribution.** EDGAR-derived is public domain (fine).
  Licensed vendor panels/columns (e.g. Sharadar) — never post raw extracts.
- **No performance claims that read as solicitation.** Frame everything as
  research/education, never "returns you could get." Keeps clear of
  investment-advice territory and matches the brand.
```
