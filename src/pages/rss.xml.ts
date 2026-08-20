import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { getSortedPosts } from "@/utils/getSortedPosts";
import { getPostUrl } from "@/utils/getPostPaths";
import { getSortedCatalysts } from "@/utils/getSortedCatalysts";
import { getCatalystUrl } from "@/utils/getCatalystPaths";
import config from "@/config";

export async function GET() {
  const posts = await getCollection("posts");
  const sortedPosts = getSortedPosts(posts);

  const catalysts = await getCollection("catalysts");
  const sortedCatalysts = getSortedCatalysts(catalysts);

  const items = [
    ...sortedPosts.map(({ data, id, filePath }) => ({
      link: getPostUrl(id, filePath, config.site.lang),
      title: data.title,
      description: data.description,
      pubDate: new Date(data.modDatetime ?? data.pubDatetime),
    })),
    ...sortedCatalysts.map(({ data, id, filePath }) => ({
      link: getCatalystUrl(id, filePath, config.site.lang),
      title: data.title,
      description: data.description,
      pubDate: new Date(data.modDatetime ?? data.pubDatetime),
    })),
  ].sort((a, b) => b.pubDate.getTime() - a.pubDate.getTime());

  return rss({
    title: config.site.title,
    description: config.site.description,
    site: config.site.url,
    items,
  });
}
