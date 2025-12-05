from flask import Flask, request, jsonify
from flask_cors import CORS
import config
import db
from auth import bp as auth_bp

app = Flask(__name__)

# Clave secreta generada una sola vez (NO cambies cada vez que arranques)
app.secret_key = "f95d1728171c9b06dddc0e52dfcc65fc"  # necesaria para sesiones
# Registrar el blueprint de autenticación
app.register_blueprint(auth_bp)

# CORS configurado para permitir el frontend
CORS(app, origins=config.CORS_ORIGINS.split(","), supports_credentials=True)

# Healthcheck
@app.get("/api/health")
def health():
    return jsonify({"ok": True, "message": "Backend Flask operativo"})

# Listar juegos con paginación básica
@app.get("/api/games")
def list_games():
    try:
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "Parámetros limit y offset deben ser enteros"}), 400

    data = db.list_games(limit=limit, offset=offset)
    return jsonify(data)

# Obtener un juego por id
@app.get("/api/games/<int:game_id>")
def get_game(game_id):
    game = db.get_game(game_id)
    if not game:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify(game)

# Crear juego
@app.post("/api/games")
def create_game():
    payload = request.get_json(force=True) or {}
    # Validación mínima
    nombre = payload.get("nombre")
    if not nombre:
        return jsonify({"error": "'nombre' es obligatorio"}), 400

    created = db.create_game(payload)
    return jsonify(created), 201

# Actualizar juego (PUT/PATCH)
@app.put("/api/games/<int:game_id>")
@app.patch("/api/games/<int:game_id>")
def update_game(game_id):
    payload = request.get_json(force=True) or {}
    updated = db.update_game(game_id, payload)
    if not updated:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify(updated)

# Eliminar juego
@app.delete("/api/games/<int:game_id>")
def delete_game(game_id):
    ok = db.delete_game(game_id)
    if not ok:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.PORT, debug=config.FLASK_DEBUG)
