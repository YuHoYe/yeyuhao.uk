import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";
import remarkWikilinks from "./src/plugins/remark-wikilinks.mjs";

export default defineConfig({
  site: "https://yeyuhao.uk",
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    remarkPlugins: [remarkWikilinks],
    shikiConfig: {
      theme: "github-dark",
    },
  },
});
