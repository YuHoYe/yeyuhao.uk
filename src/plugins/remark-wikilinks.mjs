// Strips Obsidian [[wikilinks]] from markdown text nodes
// [[path|display]] → display, [[path]] → last path segment
import { visit } from "unist-util-visit";

export default function remarkWikilinks() {
  return (tree) => {
    visit(tree, "text", (node) => {
      if (!node.value.includes("[[")) return;
      node.value = node.value
        .replace(/\[\[([^\]]*?)\|([^\]]+)\]\]/g, "$2")
        .replace(/\[\[([^\]]+)\]\]/g, (_match, path) => {
          const segments = path.split("/");
          return segments[segments.length - 1];
        });
    });
  };
}
