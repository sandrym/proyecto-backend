import os
import requests

BASE_URL = f"http://localhost:{os.getenv('PORT', '5000')}/api"

def pp(title, data):
    print(f"\n=== {title} ===")
    print(data)

def main():
    # 1) Listar (vacío al inicio)
    r = requests.get(f"{BASE_URL}/games")
    pp("LIST (inicio)", r.json())

    # 2) Crear
    nuevo = {
        "nombre": "Super Mario Bros",
        "descripcion": "Clásico de plataformas",
        "anio": 1985,
        "plataforma": "NES",
        "imagen_url": "https://example.com/mario.jpg"
    }
    r = requests.post(f"{BASE_URL}/games", json=nuevo)
    creado = r.json()
    pp("CREATE", creado)
    game_id = creado["id"]

    # 3) Obtener por id
    r = requests.get(f"{BASE_URL}/games/{game_id}")
    pp("GET by id", r.json())

    # 4) Actualizar (PUT/PATCH)
    cambios = {"anio": 1986, "plataforma": "NES Classic"}
    r = requests.patch(f"{BASE_URL}/games/{game_id}", json=cambios)
    pp("UPDATE", r.json())

    # 5) Listar (debería tener 1)
    r = requests.get(f"{BASE_URL}/games")
    pp("LIST (tras crear)", r.json())

    # 6) Eliminar
    r = requests.delete(f"{BASE_URL}/games/{game_id}")
    pp("DELETE", r.json())

    # 7) Listar final (vacío de nuevo)
    r = requests.get(f"{BASE_URL}/games")
    pp("LIST (final)", r.json())

if __name__ == "__main__":
    main()
