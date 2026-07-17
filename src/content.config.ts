import { defineCollection } from "astro:content";
import { z } from "astro/zod";
import { glob } from "astro/loaders";
import config from "@/config";

export const BLOG_PATH = "src/content/posts";

const posts = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: `./${BLOG_PATH}` }),
  schema: ({ image }) =>
    z.object({
      author: z.string().default(config.site.author),
      pubDatetime: z.date(),
      modDatetime: z.date().optional().nullable(),
      title: z.string(),
      featured: z.boolean().optional(),
      draft: z.boolean().optional(),
      tags: z.array(z.string()).default(["others"]),
      ogImage: image().or(z.string()).optional(),
      description: z.string(),
      canonicalURL: z.string().optional(),
      hideEditPost: z.boolean().optional(),
      timezone: z.string().optional(),
      // --- Research metadata (all optional; non-research posts omit them) ---
      project: z.string().optional(), // e.g. "P06"
      question: z.string().optional(), // one-line research question
      headline: z.string().optional(), // headline finding
      status: z
        .enum([
          "in-sample",
          "validated",
          "negative-result",
          "finding",
          "infra",
        ])
        .optional(),
      version: z.string().optional(),
      dataSources: z.array(z.string()).optional(),
      repo: z.string().optional(), // link to the project source
      notebook: z.string().optional(), // link to the analysis notebook
      dashboard: z.string().optional(), // link to the live dashboard page
    }),
});

const pages = defineCollection({
  loader: glob({ pattern: "**/[^_]*.{md,mdx}", base: "./src/content/pages" }),
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    ogImage: z.string().optional(),
    canonicalURL: z.string().optional(),
  }),
});

export const collections = { posts, pages };
