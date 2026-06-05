"""Shared pytest fixtures for the bot test suite."""
from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest
import yaml

from bot.persona import load_persona
from bot.storage import Storage


@pytest.fixture
def persona_yaml(tmp_path: Path) -> Path:
    p = tmp_path / "persona.yaml"
    p.write_text(
        yaml.safe_dump(
            {
                "handle": "testpersona",
                "display_name": "Test Persona",
                "angle": "test angle",
                "voice_rules": ["test rule"],
                "greeting": "hi, i'm an AI companion — pick one to come in",
                "paywall_message": "pay to keep going",
                "offers": [
                    {"name": "hour", "description": "one hour", "stars_price": 100, "usd_price": 25.0},
                    {"name": "bundle", "description": "five notes", "stars_price": 500, "usd_price": 75.0},
                ],
                "system_prompt": "you are test persona, openly an AI",
            }
        )
    )
    return p


@pytest.fixture
def persona(persona_yaml):
    return load_persona(persona_yaml)


@pytest.fixture
def storage(tmp_path: Path) -> Storage:
    return Storage(tmp_path / "t.db")


@pytest.fixture
def fake_claude():
    c = MagicMock()
    c.reply = AsyncMock(return_value="test reply")
    return c


@pytest.fixture
def context(persona, storage, fake_claude):
    """A MagicMock context with the bot_data attributes the handlers read.

    np defaults to None (crypto rail disabled). Tests that need crypto enabled
    can do `context.application.bot_data["np"] = some_mock` before calling.
    """
    ctx = MagicMock()
    ctx.application.bot_data = {
        "persona": persona,
        "storage": storage,
        "claude": fake_claude,
        "np": None,
    }
    ctx.bot = MagicMock()
    ctx.bot.send_invoice = AsyncMock()
    return ctx
