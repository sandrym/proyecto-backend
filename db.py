import psycopg2
import psycopg2.extras
from typing import List, Dict, Any, Optional
import config

def get_connection():
    return psycopg2.connect(
        host=config.PG_HOST,
        port=config.PG_PORT,
        dbname=config.PG_DB,
        user=config.PG_USER,
        password=config.PG_PASSWORD,
    )

def row_to_dict(row) -> Dict[str, Any]:
    return dict(row)

COMMON_FIELDS = "id, nombre, descripcion, anio, plataforma, imagen_url, url, color, created_at, updated_at"

def list_games(limit: int = 100, offset: int = 0) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"""
                SELECT {COMMON_FIELDS}
                FROM games
                ORDER BY id ASC
                LIMIT %s OFFSET %s
            """, (limit, offset))
            items = [row_to_dict(r) for r in cur.fetchall()]

            cur.execute("SELECT COUNT(*) AS total FROM games")
            row = cur.fetchone()
            total = row['total'] if row else 0

            return {"items": items, "total": total, "limit": limit, "offset": offset}

def get_game(game_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"""
                SELECT {COMMON_FIELDS}
                FROM games WHERE id = %s
            """, (game_id,))
            row = cur.fetchone()
            return row_to_dict(row) if row else None

def create_game(data: Dict[str, Any]) -> Dict[str, Any]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO games (nombre, descripcion, anio, plataforma, imagen_url, url, color)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, nombre, descripcion, anio, plataforma, imagen_url, url, color, created_at, updated_at
            """, (
                data.get("nombre"),
                data.get("descripcion"),
                data.get("anio"),
                data.get("plataforma"),
                data.get("imagen_url"),
                data.get("url"),
                data.get("color"),
            ))
            return row_to_dict(cur.fetchone())

def update_game(game_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    fields, values = [], []
    for key in ["nombre", "descripcion", "anio", "plataforma", "imagen_url", "url", "color"]:
        if key in data:
            fields.append(f"{key} = %s")
            values.append(data[key])
    if not fields:
        return get_game(game_id)

    values.append(game_id)
    set_clause = ", ".join(fields)

    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(f"""
                UPDATE games SET {set_clause}, updated_at = NOW()
                WHERE id = %s
                RETURNING {COMMON_FIELDS}
            """, tuple(values))
            row = cur.fetchone()
            return row_to_dict(row) if row else None

def delete_game(game_id: int) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM games WHERE id = %s", (game_id,))
            return cur.rowcount > 0


def get_user_by_username(username: str):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            row = cur.fetchone()
            return row

