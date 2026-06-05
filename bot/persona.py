"""Persona loader. A persona is a YAML file describing who the bot is acting as."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class Offer(BaseModel):
    name: str
    description: str
    stars_price: int = Field(ge=1, description="Telegram Stars price (XTR units)")
    usd_price: float = Field(gt=0, description="USD equivalent for the crypto rail")


class Persona(BaseModel):
    handle: str
    display_name: str
    angle: str
    voice_rules: list[str]
    greeting: str
    paywall_message: str
    offers: list[Offer]
    system_prompt: str


def load_persona(path: str | Path) -> Persona:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    return Persona.model_validate(raw)
