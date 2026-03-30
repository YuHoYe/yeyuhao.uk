import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const blog = defineCollection({
  loader: glob({ base: "./src/content/blog", pattern: "**/*.{md,mdx}" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    date: z.coerce.date(),
    tags: z.array(z.string()).default([]),
    lang: z.enum(["zh", "en"]).default("zh"),
    draft: z.boolean().default(false),
  }),
});

const projects = defineCollection({
  loader: glob({ base: "./src/content/projects", pattern: "**/*.yaml" }),
  schema: z.object({
    name: z.string(),
    icon: z.string(),
    description: z.string(),
    tags: z.array(z.string()).default([]),
    url: z.string().url(),
    year: z.number(),
  }),
});

const memos = defineCollection({
  loader: glob({ base: "./src/content/memos", pattern: "**/*.md" }),
  schema: z.object({
    date: z.coerce.date(),
    type: z.string().default("memo"),
    origin: z.enum(["ai", "self"]).default("self"),
    confirmed: z.boolean().default(false),
    tags: z.array(z.string()).default([]),
    cssclasses: z.array(z.string()).default([]),
    source: z.any().optional(),
  }),
});

export const collections = { blog, projects, memos };
