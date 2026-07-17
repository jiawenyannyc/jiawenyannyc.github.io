# jiawenyannyc.github.io — Quant Research

Personal research site for **Jiawen Yan**: the long-form home for systematic quant
research — full write-ups, figures, and honest findings (negative results
included). Built with [Astro](https://astro.build) on the
[AstroPaper](https://github.com/satnaing/astro-paper) theme.

## Stack

- **Astro** static site, **Tailwind 4**, MDX content.
- **KaTeX** math (`remark-math` + `rehype-katex`), Shiki code highlighting.
- **Pagefind** static search, RSS, sitemap, auto OG images, light/dark.
- Research posts reuse the `posts` content collection, extended with research
  metadata (status badge, project, question, headline, data sources, resource
  links) — see `src/content.config.ts`.

## Develop

Node is installed via nvm; make it available, then use pnpm via corepack:

```bash
export PATH="$HOME/.nvm/versions/node/v24.18.0/bin:$PATH"
corepack pnpm install
corepack pnpm dev        # http://localhost:4321
corepack pnpm build      # astro check + build + pagefind index (what CI runs)
corepack pnpm preview
```

## Add a research post

See [`docs/PUBLISHING.md`](docs/PUBLISHING.md) — the mechanical `report.md` → `.mdx`
pipeline. The fully-worked reference is `src/content/posts/capacity-curves.mdx`.

## Deploy

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds and
publishes to GitHub Pages. One-time: enable **Settings → Pages → Source: GitHub
Actions** in the repo. The site is configured for the root domain
`https://jiawenyannyc.github.io/`; for a custom domain, add `public/CNAME` and
update `site` in `astro-paper.config.ts`.
