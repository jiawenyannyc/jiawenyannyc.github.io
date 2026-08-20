import { getRelativeLocaleUrl } from "astro:i18n";
import { CATALYST_PATH } from "@/content.config";
import { slugifyStr } from "./slugify";
import config from "@/config";

function getCatalystPathSegments(filePath: string | undefined): string[] {
  return (
    filePath
      ?.replace(CATALYST_PATH, "")
      .split("/")
      .filter(path => path !== "")
      .filter(path => !path.startsWith("_"))
      .slice(0, -1)
      .map(segment => slugifyStr(segment)) ?? []
  );
}

function getIdSlug(id: string): string {
  const catalystId = id.split("/");
  return catalystId.length > 0
    ? String(catalystId[catalystId.length - 1])
    : id;
}

function getCatalystSlugPath(id: string, filePath: string | undefined): string {
  const pathSegments = getCatalystPathSegments(filePath);
  const slug = getIdSlug(id);
  return pathSegments.length > 0
    ? [...pathSegments, slug].join("/")
    : String(slug);
}

/**
 * Returns the slug-only path for use as a route param in `getStaticPaths`.
 * e.g. `/mrna-cancer-vaccine-phase3-repricing`
 */
export function getCatalystSlug(
  id: string,
  filePath: string | undefined
): string {
  return `/${getCatalystSlugPath(id, filePath)}`;
}

/**
 * Returns a fully navigable URL for use in `<a href>` and RSS links.
 * e.g. `/catalysts/mrna-cancer-vaccine-phase3-repricing`
 */
export function getCatalystUrl(
  id: string,
  filePath: string | undefined,
  locale: string | undefined = config.site.lang
): string {
  return getRelativeLocaleUrl(
    locale,
    `catalysts/${getCatalystSlugPath(id, filePath)}`
  );
}
