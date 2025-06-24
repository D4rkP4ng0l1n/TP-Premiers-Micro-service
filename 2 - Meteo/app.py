# -------------------- IMPORTS -------------------- #
from flask import Flask, request, jsonify
from flasgger import Swagger
import requests
# ------------------------------------------------- #

app = Flask(__name__)
swagger = Swagger(app)

known_cities = {
    "Rodez": (44.35, 2.57),
    "Honolulu": (21.30, -157.85),
    "Tombouctou": (16.77, -3.01)
}

# -------------------- METHODES GET -------------------- #

@app.route("/cities", methods=["GET"])
def get_cities():
    """
    Liste les villes supportées
    ---
    responses:
      200:
        description: Liste des villes disponibles
        examples:
          application/json:
            {
              "available_cities": ["Rodez", "Honolulu", "Tombouctou"]
            }
    """
    return jsonify({"available_cities": list(known_cities.keys())}), 200

@app.route("/weather", methods=["GET"])
def get_weather():
    """
    Récupère la météo d'une ville
    ---
    parameters:
      - name: city
        in: query
        type: string
        required: true
        example: Rodez
    responses:
      200:
        description: Données météo actuelles
        examples:
          application/json:
            {
              "city": "Rodez",
              "temperature": 21.3,
              "windspeed": 15.2,
              "condition": "partiellement nuageux"
            }
      400:
        description: Ville inconnue
      502:
        description: Erreur de connexion à l'API météo
    """
    city = request.args.get("city")
    if city not in known_cities:
        return jsonify({"error": "Ville inconnue"}), 400

    lat, lon = known_cities[city]
    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": lon, "current_weather": True},
            timeout=5
        )
        data = response.json()
        weather = data.get("current_weather", {})
        if not weather:
            return jsonify({"error": "Erreur lors de la récupération météo"}), 502

        return jsonify({
            "city": city,
            "temperature": weather.get("temperature"),
            "windspeed": weather.get("windspeed"),
            "condition": interpret_weather_code(weather.get("weathercode"))
        }), 200

    except requests.RequestException:
        return jsonify({"error": "Erreur de connexion à l’API météo"}), 502

# ------------------------------------------------- #

def interpret_weather_code(code):
    descriptions = {
        0: "ciel dégagé", 
        1: "principalement clair", 
        2: "partiellement nuageux",
        3: "couvert", 
        45: "brouillard", 
        51: "bruine légère",
        61: "pluie faible", 
        71: "neige faible", 
        80: "averses", 
        95: "orages"
    }
    return descriptions.get(code, "conditions inconnues")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")