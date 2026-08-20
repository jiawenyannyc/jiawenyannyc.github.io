import type { CollectionEntry } from "astro:content";
import config from "@/config";

/**
 * Determines whether a catalyst note is eligible to be listed/rendered.
 * Same rules as `postFilter`: excludes drafts, and in production holds back
 * scheduled entries until `pubDatetime` minus the configured margin.
 */
function catalystFilter({ data }: CollectionEntry<"catalysts">) {
  const isPublishTimePassed =
    Date.now() >
    new Date(data.pubDatetime).getTime() - config.posts.scheduledPostMargin;
  return !data.draft && (import.meta.env.DEV || isPublishTimePassed);
}

/**
 * Returns catalyst notes that are eligible to be shown, sorted by
 * "last updated" descending (uses `modDatetime` when present, otherwise
 * `pubDatetime`).
 */
export function getSortedCatalysts(catalysts: CollectionEntry<"catalysts">[]) {
  return catalysts
    .filter(catalystFilter)
    .sort(
      (a, b) =>
        Math.floor(
          new Date(b.data.modDatetime ?? b.data.pubDatetime).getTime() / 1000
        ) -
        Math.floor(
          new Date(a.data.modDatetime ?? a.data.pubDatetime).getTime() / 1000
        )
    );
}
