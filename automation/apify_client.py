"""Apify wrapper for the discovery loop.

We use Apify Actors as our scraping primitive. The two we care about for MVP:

1. **Twitter Scraper** — given a list of in-niche large accounts, pull their followers
   and engagement rings; score candidates by follower count + activity. Output feeds
   the shoutout vendor DB.

2. **Twitter Search Scraper** — given a list of niche keywords, pull viral recent
   tweets (>1k likes, last 24h). Output feeds the reply-guy queue.

Apify charges per actor run + compute. Budget envelope: ~$5/day for both loops at
this scale. See https://apify.com/pricing.

The actor IDs below are placeholders — swap for whatever you've validated. The
function signatures are stable; you can rotate actors without changing the
discovery loop.
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
        follower_actor: str = "apidojo/twitter-scraper-lite",
        search_actor: str = "apidojo/tweet-scraper",
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
    ) -> list[TwitterCandidate]:
        """Pull followers of seed accounts, filter to the sweet-spot follower band."""
        run = await self._client.actor(self._follower_actor).call(
            run_input={
                "handles": seed_handles,
                "getFollowers": True,
                "maxItems": max_results,
            }
        )
        items = await self._client.dataset(run["defaultDatasetId"]).list_items()
        out: list[TwitterCandidate] = []
        for item in items.items:
            followers = int(item.get("followersCount") or item.get("followers") or 0)
            if not (min_followers <= followers <= max_followers):
                continue
            out.append(
                TwitterCandidate(
                    handle=item.get("userName") or item.get("handle") or "",
                    followers=followers,
                    bio=item.get("description") or "",
                    last_active_at=item.get("lastActiveAt"),
                )
            )
        return out

    async def find_reply_targets(
        self,
        keywords: list[str],
        *,
        min_likes: int = 1_000,
        max_results: int = 100,
    ) -> list[ReplyTarget]:
        """Pull recent viral tweets matching niche keywords for the reply-guy queue."""
        run = await self._client.actor(self._search_actor).call(
            run_input={
                "searchTerms": keywords,
                "sort": "Top",
                "tweetLanguage": "en",
                "maxItems": max_results,
            }
        )
        items = await self._client.dataset(run["defaultDatasetId"]).list_items()
        out: list[ReplyTarget] = []
        for item in items.items:
            likes = int(item.get("likeCount") or 0)
            if likes < min_likes:
                continue
            out.append(
                ReplyTarget(
                    tweet_id=str(item.get("id") or ""),
                    author_handle=item.get("author", {}).get("userName", "") if isinstance(item.get("author"), dict) else "",
                    text=item.get("text") or "",
                    likes=likes,
                    posted_at=item.get("createdAt") or "",
                )
            )
        return out
