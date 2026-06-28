"""
SOP Service Module
"""
import sqlite3
from typing import Optional
from database.db import get_connection

def _row_to_dict(row: sqlite3.Row) -> dict:
    return dict(row)

def get_all_sops() -> list[dict]:
    conn = get_connection()
    try:
        cursor = conn.execute("SELECT * FROM sops ORDER BY created_at DESC")
        return [_row_to_dict(r) for r in cursor.fetchall()]
    finally:
        conn.close()

def get_sop_by_name(process_name: str) -> Optional[dict]:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM sops WHERE process_name = ? COLLATE NOCASE",
            (process_name.strip(),),
        )
        row = cursor.fetchone()
        return _row_to_dict(row) if row else None
    finally:
        conn.close()

def create_sop(data: dict) -> dict:
    conn = get_connection()
    try:
        conn.execute(
            """
            INSERT INTO sops (
                department, process_name, objective, scope,
                roles, prerequisites, steps, kpis,
                risk_factors, tools_required, review_frequency
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("department"),
                data["process_name"],
                data.get("objective"),
                data.get("scope"),
                data.get("roles"),
                data.get("prerequisites"),
                data.get("steps"),
                data.get("kpis"),
                data.get("risk_factors"),
                data.get("tools_required"),
                data.get("review_frequency"),
            ),
        )
        conn.commit()
        return get_sop_by_name(data["process_name"])
    except sqlite3.IntegrityError:
        raise ValueError(f"SOP '{data['process_name']}' already exists.")
    finally:
        conn.close()

def update_sop(process_name: str, data: dict) -> Optional[dict]:
    existing = get_sop_by_name(process_name)
    if not existing:
        return None

    allowed_fields = [
        "department", "process_name", "objective", "scope",
        "roles", "prerequisites", "steps", "kpis",
        "risk_factors", "tools_required", "review_frequency",
    ]

    updates = {k: v for k, v in data.items() if k in allowed_fields and v is not None}
    if not updates:
        return existing

    set_clause = ", ".join(f"{k} = ?" for k in updates)
    values = list(updates.values()) + [process_name]

    conn = get_connection()
    try:
        conn.execute(
            f"UPDATE sops SET {set_clause} WHERE process_name = ? COLLATE NOCASE",
            values,
        )
        conn.commit()
        return get_sop_by_name(updates.get("process_name", process_name))
    finally:
        conn.close()

def delete_sop(process_name: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.execute(
            "DELETE FROM sops WHERE process_name = ? COLLATE NOCASE",
            (process_name.strip(),),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
