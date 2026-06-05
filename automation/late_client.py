"""late.dev API wrapper.

late.dev is the post-scheduling service that owns the Twitter (X) publish
step. We hand it scheduled drafts; it handles X auth, rate limits, and
the publish.

Verified 2026-06-05 against https://docs.getlate.dev (via context7).

- Base URL: https://getlate.dev/api/v1
- Auth: `Authorization: Bearer <LW_LATE_API_KEY>` header
- Schedule: POST /posts with body
    {
      "content": str,
      "platforms": [{"platform": "twitter", "accountId": <X account id>}],
      "scheduledFor": "<ISO 8601>",
      "mediaUrls": [str, ...]      // optional
    }
  Response: { "data": { "post": { id, content, platforms, createdAt, publishStatus } } }
- List:    GET /posts?platform=twitter&status=scheduled
- Accounts: GET /accounts (one-time, to find the accountId for the connected X account)
"""
from __future__ import annotations

from dataclasses import dataclass

import httpx

API_BASE = "https://getlate.dev/api/v1"


@dataclass
class ScheduledPost:
    id: str
    platform: str
    scheduled_for: str
    content: str
    status: str


class LateClient:
    def __init__(self, api_key: str, *, twitter_account_id: str):
        self._api_key = api_key
        self._twitter_account_id = twitter_account_id

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

    async def schedule_post(
        self,
        *,
        content: str,
        scheduled_at_iso: str,
        media_urls: list[str] | None = None,
    ) -> ScheduledPost:
        payload: dict = {
            "content": content,
            "platforms": [
                {"platform": "twitter", "accountId": self._twitter_account_id}
            ],
            "scheduledFor": scheduled_at_iso,
        }
        if media_urls:
            payload["mediaUrls"] = media_urls

        async with httpx.AsyncClient(timeout=20) as http:
            r = await http.post(f"{API_BASE}/posts", headers=self._headers(), json=payload)
            r.raise_for_status()
            body = r.json()

        # Late wraps the response in {"data": {"post": {...}}}. Unwrap defensively.
        post = body.get("data", {}).get("post", body)
        return ScheduledPost(
            id=str(post.get("id", "")),
            platform="twitter",
            scheduled_for=str(post.get("scheduledFor") or scheduled_at_iso),
            content=str(post.get("content", content)),
            status=str(post.get("publishStatus", "scheduled")),
        )

    async def list_scheduled(self) -> list[ScheduledPost]:
        async with httpx.AsyncClient(timeout=20) as http:
            r = await http.get(
                f"{API_BASE}/posts",
                headers=self._headers(),
                params={"platform": "twitter", "status": "scheduled"},
            )
            r.raise_for_status()
            body = r.json()

        # Tolerate both {data: [...]} and {data: {posts: [...]}}, and bare arrays.
        data = body.get("data", body)
        items = data if isinstance(data, list) else data.get("posts") or data.get("items") or []
        return [
            ScheduledPost(
                id=str(i.get("id", "")),
                platform="twitter",
                scheduled_for=str(i.get("scheduledFor", "")),
                content=str(i.get("content", "")),
                status=str(i.get("publishStatus") or i.get("status") or "scheduled"),
            )
            for i in items
        ]

    async def list_accounts(self) -> list[dict]:
        """One-time helper: find the accountId for your connected X profile.

        Run this once after connecting Twitter in the late.dev dashboard:
            python -c "import asyncio, os; from automation.late_client import LateClient; \\
                print(asyncio.run(LateClient(os.environ['LW_LATE_API_KEY'], \\
                twitter_account_id='').list_accounts()))"
        Then put the right accountId into LW_LATE_TWITTER_ACCOUNT_ID.
        """
        async with httpx.AsyncClient(timeout=20) as http:
            r = await http.get(f"{API_BASE}/accounts", headers=self._headers())
            r.raise_for_status()
            body = r.json()
        data = body.get("data", body)
        if isinstance(data, list):
            return data
        return data.get("accounts") or data.get("items") or []
