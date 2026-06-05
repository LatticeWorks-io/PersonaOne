"""Apify wrapper for the discovery loop.

We use two Apify Actors as scraping primitives:

1. **`xquik/x-follower-scraper`** (verified 2026-06-05) — pulls followers of
   seed accounts in our niche with built-in `minFollowers` / `maxFollowers`
   filters, so we don't pay for results outside the 10k–100k sweet-spot band.
   $0.15 per 1,000 filtered results. 99.2% success rate.
   https://apify.com/xquik/x-follower-scraper

2. **`api-ninja/x-twitter-advanced-search`** (verified 2026-06-05) — searches
   tweets with `engagementMinLikes` + `timeWithinTime` filters for the
   reply-guy queue. $0.35 per 1,000 results + $0.01 startup. 99.9% success.
   https://apify.com/api-ninja/x-twitter-advanced-search

Total daily cost at 200 follower results + 100 tweet results: ~$0.08/day,
~$2.50/month. Tune `max_results` in calls if you want more.

Actor IDs are pinned with override params so the wrapper survives if you
swap actors later — only the input shape mapping changes.
"""
from __future__ import annotations

from dataclasses import dataclass

from apify_client import ApifyClientAsync


@dataclass
class TwitterCandidate:
    handle: str
    followers: int
    bio: str
    last_active_at: str | None


@dataclass
class ReplyTarget:
    tweet_id: str
    author_handle: str
    text: str
    likes: int
    posted_at: str


class ApifyDiscovery:
    def __init__(
        self,
        api_token: str,
        *,
        follower_actor: str = "xquik/x-follower-scraper",
        search_actor: str = "api-ninja/x-twitter-advanced-search",
    ):
        self._client = ApifyClientAsync(token=api_token)
        self._follower_actor = follower_actor
        self._search_actor = search_actor

    async def find_shoutout_candidates(
        self,
        seed_handles: list[str],
        *,
        min_followers: int = 10_000,
        max_followers: int = 100_000,
        max_results: int = 200,
        bio_contains: str | None = None,
    ) -> list[TwitterCandidate]:
        """Pull followers of seed accounts, filtered to the sweet-spot follower band.

        The actor's `minFollowers`/`maxFollowers` do the filtering server-side,
        so we only pay for results that match (not the firehose).
        """
        run_input: dict = {
            "twitterHandles": [h.lstrip("@") for h in seed_handles],
            "relation": "followers",
            "maxItems": max_results,
            "minFollowers": min_followers,
            "maxFollowers": max_followers,
            "minAccountAgeDays": 90,  # filters obvious bot-net followers
            "outputMode": "compact",
            "includeTargetMetadata": True,
        }
        if bio_contains:
            run_input["bioContains"] = bio_contains

        run = await self._client.actor(self._follower_actor).call(run_input=run_input)
        items = await self._client.dataset(run["defaultDatasetId"]).list_items()

        out: list[TwitterCandidate] = []
        for item in items.items:
            handle = item.get("username") or item.get("screen_name") or ""
            if not handle:
                continue
            out.append(
                TwitterCandidate(
                    handle=handle,
                    followers=int(item.get("followers") or 0),
                    bio=item.get("description") or "",
                    last_active_at=item.get("createdAt"),  # account creation; actor doesn't expose last-active
                )
            )
        return out

    async def find_reply_targets(
        self,
        keywords: list[str],
        *,
        min_likes: int = 1_000,
        max_results: int = 100,
        within: str = "1d",
        language: str = "en",
    ) -> list[ReplyTarget]:
        """Pull recent viral tweets matching niche keywords for the reply-guy queue.

        `within` is the actor's `timeWithinTime` ('1d' = last 24h, '6h' etc.).
        Engagement filter is server-side via `engagementMinLikes`.
        """
        run_input: dict = {
            "query": " OR ".join(keywords) if keywords else "",
            "contentKeywords": keywords,
            "search_type": "Top",
            "numberOfTweets": max(max_results, 20),  # actor minimum is 20
            "engagementMinLikes": min_likes,
            "timeWithinTime": within,
            "contentLanguage": language,
            "tweetTypes": ["original"],  # exclude replies/quotes to avoid noise
        }
        run = await self._client.actor(self._search_actor).call(run_input=run_input)
        items = await self._client.dataset(run["defaultDatasetId"]).list_items()

        out: list[ReplyTarget] = []
        for item in items.items:
            tweet_id = str(item.get("tweet_id") or item.get("id_str") or "")
            if not tweet_id:
                continue
            out.append(
                ReplyTarget(
                    tweet_id=tweet_id,
                    author_handle=item.get("screen_name", ""),
                    text=item.get("text") or "",
                    likes=int(item.get("favorites") or 0),
                    posted_at=item.get("created_at") or "",
                )
            )
        return out
