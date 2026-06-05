"""SQLite storage for sessions and paid users.

Two tables:
- paid_users: tg_user_id, offer_name, paid_at, rail, external_id (Stars charge_id or NowPayments invoice_id)
- session_turns: tg_user_id, role, content, created_at

Sessions are append-only. The bot reads the last N turns when calling Claude.
"""
from __future__ import annotations

import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS paid_users (
    tg_user_id   INTEGER NOT NULL,
    offer_name   TEXT    NOT NULL,
    paid_at      INTEGER NOT NULL,
    rail         TEXT    NOT NULL CHECK (rail IN ('stars', 'crypto')),
    external_id  TEXT    NOT NULL,
    PRIMARY KEY (tg_user_id, external_id)
);

CREATE TABLE IF NOT EXISTS session_turns (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_user_id   INTEGER NOT NULL,
    role         TEXT    NOT NULL CHECK (role IN ('user', 'assistant')),
    content      TEXT    NOT NULL,
    created_at   INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_session_user_time
    ON session_turns (tg_user_id, created_at);
"""


class Storage:
    def __init__(self, db_path: str | Path):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._conn() as c:
            c.executescript(SCHEMA)

    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def mark_paid(self, tg_user_id: int, offer_name: str, rail: str, external_id: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO paid_users (tg_user_id, offer_name, paid_at, rail, external_id) "
                "VALUES (?, ?, ?, ?, ?)",
                (tg_user_id, offer_name, int(time.time()), rail, external_id),
            )

    def has_active_payment(self, tg_user_id: int) -> bool:
        with self._conn() as c:
            row = c.execute(
                "SELECT 1 FROM paid_users WHERE tg_user_id = ? LIMIT 1",
                (tg_user_id,),
            ).fetchone()
            return row is not None

    def append_turn(self, tg_user_id: int, role: str, content: str) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT INTO session_turns (tg_user_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (tg_user_id, role, content, int(time.time())),
            )

    def recent_turns(self, tg_user_id: int, limit: int = 20) -> list[dict]:
        with self._conn() as c:
            rows = c.execute(
                "SELECT role, content FROM session_turns WHERE tg_user_id = ? "
                "ORDER BY created_at DESC LIMIT ?",
                (tg_user_id, limit),
            ).fetchall()
            return [dict(r) for r in reversed(rows)]
