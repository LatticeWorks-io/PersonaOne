from bot.storage import Storage


def test_mark_paid_then_has_active(tmp_path):
    s = Storage(tmp_path / "t.db")
    assert s.has_active_payment(42) is False
    s.mark_paid(tg_user_id=42, offer_name="hour", rail="stars", external_id="charge_abc")
    assert s.has_active_payment(42) is True


def test_duplicate_external_id_is_idempotent(tmp_path):
    s = Storage(tmp_path / "t.db")
    s.mark_paid(42, "hour", "stars", "charge_abc")
    s.mark_paid(42, "hour", "stars", "charge_abc")
    # No exception; second call is a no-op via INSERT OR IGNORE.
    assert s.has_active_payment(42) is True


def test_session_turns_ordered_oldest_first(tmp_path):
    s = Storage(tmp_path / "t.db")
    for i in range(3):
        s.append_turn(42, "user", f"u{i}")
        s.append_turn(42, "assistant", f"a{i}")
    turns = s.recent_turns(42, limit=10)
    assert [t["content"] for t in turns] == ["u0", "a0", "u1", "a1", "u2", "a2"]


def test_recent_turns_limit_respected(tmp_path):
    s = Storage(tmp_path / "t.db")
    for i in range(10):
        s.append_turn(42, "user", f"u{i}")
    turns = s.recent_turns(42, limit=3)
    # Most recent 3, oldest first → u7, u8, u9
    assert [t["content"] for t in turns] == ["u7", "u8", "u9"]


def test_paid_users_are_per_tg_user(tmp_path):
    s = Storage(tmp_path / "t.db")
    s.mark_paid(42, "hour", "stars", "c1")
    assert s.has_active_payment(42) is True
    assert s.has_active_payment(43) is False
