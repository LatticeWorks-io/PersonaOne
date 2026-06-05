"""Thin wrapper around the Anthropic SDK with persona system-prompt + conversation history."""
from __future__ import annotations

from anthropic import AsyncAnthropic

from bot.persona import Persona


class ClaudeClient:
    def __init__(self, api_key: str, model: str, persona: Persona):
        self._client = AsyncAnthropic(api_key=api_key)
        self._model = model
        self._persona = persona

    async def reply(self, history: list[dict], user_message: str) -> str:
        messages = [{"role": h["role"], "content": h["content"]} for h in history]
        messages.append({"role": "user", "content": user_message})
        resp = await self._client.messages.create(
            model=self._model,
            max_tokens=512,
            system=self._persona.system_prompt,
            messages=messages,
        )
        # SDK returns a list of content blocks; we only generate text.
        return "".join(block.text for block in resp.content if block.type == "text")
