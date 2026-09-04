# Author: Oleg Mrynskyi
# CMPE 272 HW2 - GitHub Issues REST API & Webhook Service
#
# sqlite storage for webhook deliveries, mostly so we can dedupe redeliveries
# and answer GET /events

import sqlite3
import aiosqlite
from typing import List, Optional
from datetime import datetime
from app.schemas import EventRecord

async def init_db(db_path: str = "events.db") -> None:
    async with aiosqlite.connect(db_path) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                delivery_id TEXT UNIQUE NOT NULL,
                event TEXT NOT NULL,
                action TEXT,
                issue_number INTEGER,
                payload TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("CREATE INDEX IF NOT EXISTS idx_delivery_id ON events(delivery_id)")
        await db.commit()


async def is_duplicate_delivery(delivery_id: str, db_path: str = "events.db") -> bool:
    if not delivery_id:
        return False
    async with aiosqlite.connect(db_path) as db:
        async with db.execute("SELECT 1 FROM events WHERE delivery_id = ?", (delivery_id,)) as cursor:
            row = await cursor.fetchone()
            return row is not None


async def record_webhook_event(
    delivery_id: str,
    event: str,
    action: Optional[str],
    issue_number: Optional[int],
    payload: str,
    db_path: str = "events.db"
) -> bool:
    # returns False if delivery_id already exists (unique constraint kicks in)
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                """
                INSERT INTO events (delivery_id, event, action, issue_number, payload)
                VALUES (?, ?, ?, ?, ?)
                """,
                (delivery_id, event, action, issue_number, payload)
            )
            await db.commit()
            return True
    except sqlite3.IntegrityError:
        # Duplicate delivery_id constraint violation
        return False


async def get_recent_events(limit: int = 50, db_path: str = "events.db") -> List[EventRecord]:
    events = []
    async with aiosqlite.connect(db_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT id, delivery_id, event, action, issue_number, timestamp FROM events ORDER BY id DESC LIMIT ?",
            (limit,)
        ) as cursor:
            rows = await cursor.fetchall()
            for row in rows:
                # sqlite gives back a string here, not a datetime
                ts = row["timestamp"]
                if isinstance(ts, str):
                    try:
                        ts_dt = datetime.fromisoformat(ts)
                    except ValueError:
                        ts_dt = datetime.utcnow()
                elif isinstance(ts, datetime):
                    ts_dt = ts
                else:
                    ts_dt = datetime.utcnow()

                events.append(
                    EventRecord(
                        id=row["id"],
                        delivery_id=row["delivery_id"],
                        event=row["event"],
                        action=row["action"],
                        issue_number=row["issue_number"],
                        timestamp=ts_dt
                    )
                )
    return events
