"""Small SQLite store for durable conversation notes and history."""
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB_PATH = Path(__file__).resolve().parent / "agent_memory.db"

def _connect():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def initialize_memory():
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS conversation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS user_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                fact TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(session_id, fact)
            )
        """)

def save_message(session_id: str, role: str, content: str):
    with _connect() as conn:
        conn.execute(
            "INSERT INTO conversation_history(session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (session_id, role, content, datetime.now(timezone.utc).isoformat())
        )

def load_recent_messages(session_id: str, limit: int = 12):
    with _connect() as conn:
        rows = conn.execute(
            "SELECT role, content FROM conversation_history WHERE session_id=? ORDER BY id DESC LIMIT ?",
            (session_id, limit)
        ).fetchall()
    return list(reversed(rows))

def save_fact(session_id: str, fact: str):
    fact = fact.strip()
    if not fact:
        return
    with _connect() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO user_facts(session_id, fact, created_at) VALUES (?, ?, ?)",
            (session_id, fact, datetime.now(timezone.utc).isoformat())
        )

def search_facts(session_id: str, query: str = "", limit: int = 10):
    with _connect() as conn:
        if query.strip():
            rows = conn.execute(
                "SELECT fact FROM user_facts WHERE session_id=? AND fact LIKE ? ORDER BY id DESC LIMIT ?",
                (session_id, f"%{query.strip()}%", limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT fact FROM user_facts WHERE session_id=? ORDER BY id DESC LIMIT ?",
                (session_id, limit)
            ).fetchall()
    return [row[0] for row in rows]
