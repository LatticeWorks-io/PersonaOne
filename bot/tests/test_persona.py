import pytest
from pydantic import ValidationError

from bot.persona import load_persona


def _write_persona(path, overrides: dict | None = None):
    base = {
        "handle": "personaone",
        "display_name": "Persona One",
        "angle": "test angle",
        "voice_rules": ["short sentences"],
        "greeting": "hi",
        "paywall_message": "pay to keep going",
        "offers": [
            {"name": "hour", "description": "one hour", "stars_price": 100, "usd_price": 25.0},
        ],
        "system_prompt": "you are persona one",
    }
    if overrides:
        base.update(overrides)
    import yaml
    path.write_text(yaml.safe_dump(base))


def test_load_minimal_persona(tmp_path):
    p = tmp_path / "p.yaml"
    _write_persona(p)
    persona = load_persona(p)
    assert persona.handle == "personaone"
    assert persona.offers[0].stars_price == 100


def test_rejects_zero_priced_stars(tmp_path):
    p = tmp_path / "p.yaml"
    _write_persona(p, {"offers": [{"name": "n", "description": "d", "stars_price": 0, "usd_price": 1.0}]})
    with pytest.raises(ValidationError):
        load_persona(p)
