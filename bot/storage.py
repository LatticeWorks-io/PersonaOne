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
    amount_xtr   INTEGER NOT NULL DEFAULT 0,
    amount_usd   REAL    NOT NULL DEFAULT 0.0,
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

CREATE INDEX IF NOT EXISTS idx_paid_paid_at
    ON paid_users (paid_at);
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

    def mark_paid(
        self,
        tg_user_id: int,
        offer_name: str,
        rail: str,
        external_id: str,
        *,
        amount_xtr: int = 0,
        amount_usd: float = 0.0,
    ) -> None:
        with self._conn() as c:
            c.execute(
                "INSERT OR IGNORE INTO paid_users "
                "(tg_user_id, offer_name, paid_at, rail, external_id, amount_xtr, amount_usd) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (tg_user_id, offer_name, int(time.time()), rail, external_id, amount_xtr, amount_usd),
            )

    def revenue_summary(self, *, days: int = 7) -> dict:
        """Aggregate stats for the /stats admin command.

        Returns:
            {
                "paid_users_total": int,         # distinct users who've ever paid
                "payments_total": int,           # total payment events
                "stars_xtr": int,                # sum of XTR (Telegram Stars) ever received
                "crypto_usd": float,             # sum of USD (NowPayments) ever received
                "new_buyers_window": int,        # distinct users whose FIRST payment was in last `days`
                "window_days": int,
            }
        """
        since = int(time.time()) - days * 86400
        with self._conn() as c:
            row = c.execute(
                "SELECT "
                "  COUNT(DISTINCT tg_user_id)               AS paid_users_total, "
                "  COUNT(*)                                  AS payments_total, "
                "  COALESCE(SUM(amount_xtr), 0)              AS stars_xtr, "
                "  COALESCE(SUM(amount_usd), 0.0)            AS crypto_usd "
                "FROM paid_users"
            ).fetchone()
            new_buyers = c.execute(
                "SELECT COUNT(*) AS n FROM ("
                "  SELECT tg_user_id, MIN(paid_at) AS first_paid "
                "  FROM paid_users GROUP BY tg_user_id"
                ") WHERE first_paid >= ?",
                (since,),
            ).fetchone()
            return {
                "paid_users_total": row["paid_users_total"],
                "payments_total": row["payments_total"],
                "stars_xtr": int(row["stars_xtr"]),
                "crypto_usd": float(row["crypto_usd"]),
                "new_buyers_window": new_buyers["n"],
                "window_days": days,
            }

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
