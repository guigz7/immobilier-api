from flask import Blueprint, request, jsonify
from app.models.user import Utilisateur
from app import db

utilisateur_bp = Blueprint("utilisateur", __name__)

@utilisateur_bp.route("/users", methods=["POST"])
def creer_utilisateur():
    data = request.json

    user = Utilisateur(
        prenom=data["prenom"],
        nom=data["nom"],
        date_naissance=data["date_naissance"]
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Utilisateur créé"})