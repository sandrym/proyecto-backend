# auth.py
from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2.extras
import db

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.post("/register")
def register():
    payload = request.get_json(force=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    with db.get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT 1 FROM users WHERE username=%s", (username,))
            if cur.fetchone():
                # 409 = Conflict
                return jsonify({"ok": False, "error": "El usuario ya existe"}), 409

            cur.execute("""
                INSERT INTO users (username, password_hash, role)
                VALUES (%s, %s, %s)
                RETURNING id, username, role
            """, (username, generate_password_hash(password), "user"))
            user = cur.fetchone()
            conn.commit()

    # Autologin tras registro
    session.update({"user_id": user["id"], "username": user["username"], "role": user["role"]})
    return jsonify({"ok": True, "user": user}), 201


@bp.post("/login")
def login():
    payload = request.get_json(force=True) or {}
    username = (payload.get("username") or "").strip()
    password = payload.get("password") or ""

    if not username or not password:
        return jsonify({"ok": False, "error": "Faltan datos"}), 400

    with db.get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, username, role, password_hash FROM users WHERE username=%s", (username,))
            row = cur.fetchone()
            if not row or not check_password_hash(row["password_hash"], password):
                # 401 = Unauthorized
                return jsonify({"ok": False, "error": "Usuario o contraseña incorrectos"}), 401

    session.update({"user_id": row["id"], "username": row["username"], "role": row["role"]})
    return jsonify({"ok": True, "user": {"id": row["id"], "username": row["username"], "role": row["role"]}})


# WHOAMI
@bp.get("/me")
def whoami():
    if "user_id" not in session:
        return jsonify({"ok": False, "user": None}), 401
    return jsonify({
        "ok": True,
        "user": {
            "id": session["user_id"],
            "username": session["username"],
            "role": session["role"]
        }
    })

# LOGOUT
@bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True})
