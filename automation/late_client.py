"""late.dev API wrapper.

late.dev is the post-scheduling service that owns the actual Twitter (X) publish
step. We hand it a queue of drafts + scheduled timestamps; it handles auth, the
API rate limits, and the publish.

API docs: https://docs.late.dev/api-reference/introduction
Auth: `Authorization: Bearer <token>` in env as LW_LATE_API_KEY.

This client is intentionally minimal — `schedule_post` and `list_scheduled`. Add
delete/update as needed.
"""
from __future__ import annotations

from dataclasses import dataclass

import httpx

API_BASE = "https://api.late.dev/v1"


@dataclass
class ScheduledPost:
    id: str
    platform: str
    scheduled_at: str
    content: str
    status: str


class LateClient:
    def __init__(self, api_key: str, *, twitter_profile_id: str):
        self._api_key = api_key
        self._twitter_profile_id = twitter_profile_id

    async def schedule_post(
        self,
        *,
        content: str,
        scheduled_at_iso: str,
        media_urls: list[str] | None = None,
    ) -> ScheduledPost:
        payload = {
            "profileId": self._twitter_profile_id,
            "content": content,
            "scheduledAt": scheduled_at_iso,
        }
        if media_urls:
            payload["mediaUrls"] = media_urls
        async with httpx.AsyncClient(timeout=20) as http:
            r = await http.post(
                f"{API_BASE}/posts",
                headers={"Authorization": f"Bearer {self._api_key}"},
                json=payload,
            )
            r.raise_for_status()
            body = r.json()
        return ScheduledPost(
            id=body.get("id", ""),
            platform=body.get("platform", "twitter"),
            scheduled_at=body.get("scheduledAt", scheduled_at_iso),
            content=body.get("content", content),
            status=body.get("status", "scheduled"),
        )

    async def list_scheduled(self) -> list[ScheduledPost]:
        async with httpx.AsyncClient(timeout=20) as http:
            r = await http.get(
                f"{API_BASE}/posts",
                headers={"Authorization": f"Bearer {self._api_key}"},
                params={"profileId": self._twitter_profile_id, "status": "scheduled"},
            )
            r.raise_for_status()
            items = r.json().get("items", [])
        return [
            ScheduledPost(
                id=i.get("id", ""),
                platform=i.get("platform", "twitter"),
                scheduled_at=i.get("scheduledAt", ""),
                content=i.get("content", ""),
                status=i.get("status", ""),
            )
            for i in items
        ]
