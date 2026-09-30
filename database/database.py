"""SQLite persistence for products, generated content, quality, and reviews."""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "products.db"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db() -> None:
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT NOT NULL,
                image_path TEXT NOT NULL, additional_info TEXT, target_keywords TEXT,
                brand_info TEXT, product_analysis TEXT, status TEXT NOT NULL DEFAULT 'Pending Review',
                quality_score REAL DEFAULT 0, created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS descriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                description_text TEXT NOT NULL, description_type TEXT NOT NULL,
                seo_score REAL DEFAULT 0, attribute_coverage REAL DEFAULT 0, created_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS quality_analysis (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                description_id INTEGER, seo_score REAL, attribute_coverage REAL,
                similarity_scores TEXT, overall_score REAL, details TEXT, created_at TEXT NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE,
                FOREIGN KEY(description_id) REFERENCES descriptions(id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER NOT NULL,
                selected_description INTEGER, edited_text TEXT, review_status TEXT NOT NULL,
                approval_timestamp TEXT, FOREIGN KEY(product_id) REFERENCES products(id) ON DELETE CASCADE
            );
            """
        )


def create_product(data: dict[str, Any]) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            """INSERT INTO products (name, category, image_path, additional_info, target_keywords,
            brand_info, product_analysis, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (data["name"], data["category"], data["image_path"], data.get("additional_info", ""),
             data.get("target_keywords", ""), data.get("brand_info", ""),
             json.dumps(data.get("product_analysis", {})), "Pending Review", now_iso()),
        )
        return int(cursor.lastrowid)


def add_description(product_id: int, description_type: str, text: str, seo: float, coverage: float) -> int:
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO descriptions (product_id, description_text, description_type, seo_score, attribute_coverage, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (product_id, text, description_type, seo, coverage, now_iso()),
        )
        return int(cursor.lastrowid)


def save_quality(product_id: int, result: dict[str, Any], description_ids: list[int]) -> None:
    with get_connection() as connection:
        for description_id, item in zip(description_ids, result["per_description"]):
            connection.execute(
                "INSERT INTO quality_analysis (product_id, description_id, seo_score, attribute_coverage, similarity_scores, overall_score, details, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (product_id, description_id, item["seo"]["score"], item["attributes"]["percentage"],
                 json.dumps(result["similarity"]), item["overall"], json.dumps(item), now_iso()),
            )
        connection.execute("UPDATE products SET quality_score = ? WHERE id = ?", (result["overall"], product_id))


def save_review(product_id: int, selected_id: int, edited_text: str, status: str) -> None:
    timestamp = now_iso() if status == "Approved" else None
    with get_connection() as connection:
        connection.execute("DELETE FROM reviews WHERE product_id = ?", (product_id,))
        connection.execute(
            "INSERT INTO reviews (product_id, selected_description, edited_text, review_status, approval_timestamp) VALUES (?, ?, ?, ?, ?)",
            (product_id, selected_id, edited_text, status, timestamp),
        )
        connection.execute("UPDATE products SET status = ? WHERE id = ?", (status, product_id))


def list_products(status: str | None = None, category: str | None = None) -> list[dict[str, Any]]:
    query = "SELECT * FROM products WHERE 1=1"
    params: list[Any] = []
    if status and status != "All":
        query += " AND status = ?"; params.append(status)
    if category and category != "All":
        query += " AND category = ?"; params.append(category)
    query += " ORDER BY created_at DESC"
    with get_connection() as connection:
        return [dict(row) for row in connection.execute(query, params).fetchall()]


def get_product(product_id: int) -> dict[str, Any] | None:
    with get_connection() as connection:
        product = connection.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if not product:
            return None
        result = dict(product)
        result["product_analysis"] = json.loads(result["product_analysis"] or "{}")
        result["descriptions"] = [dict(row) for row in connection.execute("SELECT * FROM descriptions WHERE product_id = ? ORDER BY id", (product_id,))]
        quality = connection.execute("SELECT * FROM quality_analysis WHERE product_id = ? ORDER BY id", (product_id,)).fetchall()
        result["quality"] = [dict(row) for row in quality]
        result["review"] = next((dict(row) for row in connection.execute("SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC", (product_id,)).fetchall()), None)
        return result


def dashboard_stats() -> dict[str, float]:
    with get_connection() as connection:
        row = connection.execute("SELECT COUNT(*) products, COALESCE(SUM((SELECT COUNT(*) FROM descriptions d WHERE d.product_id = p.id)), 0) descriptions, COALESCE(SUM(status = 'Pending Review'), 0) pending, COALESCE(SUM(status = 'Approved'), 0) approved, COALESCE(AVG(quality_score), 0) average FROM products p").fetchone()
        return dict(row)
