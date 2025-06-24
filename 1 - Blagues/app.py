# -------------------- IMPORTS -------------------- #
from flask import Flask, request, jsonify
import random
# ------------------------------------------------- #

app = Flask(__name__)

# Liste initiale de blagues
jokes = [
    { "joke": "Pourquoi un canard est toujours à l'heure ? Parce qu'il est dans l'étang." },
    { "joke": "Quel est le jeu de cartes préféré des canards ? La coin-che." },
    { "joke": "Qu'est-ce qui fait Nioc nioc? Un canard qui parle en verlan." },
    { "joke": "Comment appelle-t-on un canard qui fait du DevOps ? Un DuckOps." }
]

# -------------------- METHODES GET -------------------- #

@app.route("/joke", methods=["GET"])
def get_joke():
    """Renvoie une blague aléatoire"""
    joke = random.choice(jokes)
    return jsonify(joke), 200

@app.route("/joke/<int:id>", methods=["GET"])
def get_joke_by_id(id):
    if 0 <= id < len(jokes):
        return jsonify(jokes[id]), 200
    return jsonify({"error": "Blague non trouvée."}), 404

@app.route("/jokes", methods=["GET"])
def get_jokes() :
    """Renvoie toutes les blagues disponibles"""
    return jsonify(jokes), 200

# -------------------- METHODES POST -------------------- #

@app.route("/joke", methods=["POST"])
def post_joke():
    """Ajoute une nouvelle blague"""
    data = request.get_json()

    if not data or "joke" not in data:
        return jsonify({"error": "Champ 'joke' manquant."}), 400

    new_joke = data["joke"].strip()
    if len(new_joke) < 10:
        return jsonify({"error": "La blague doit faire au moins 10 caractères."}), 400

    jokes.append({ "joke": new_joke })
    return jsonify({"message": "Blague ajoutée avec succès."}), 201

# ------------------------------------------------- #

if __name__ == "__main__":
    app.run(debug=True)
