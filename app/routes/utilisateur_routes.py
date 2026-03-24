from flask import Blueprint, request, jsonify, render_template
from app.modeles.utilisateur import Utilisateur
from app import db

utilisateur_bp = Blueprint("utilisateur", __name__)

@utilisateur_bp.route("/users/form", methods=["GET"])
def form_utilisateur():
    return render_template("utilisateur.html")

@utilisateur_bp.route("/users", methods=["POST"])
def creer_utilisateur():
    data = request.form if request.form else request.json

    user = Utilisateur(
        prenom=data["prenom"],
        nom=data["nom"],
        date_naissance=data["date_naissance"]
    )

    db.session.add(user)
    db.session.commit()

    return "Utilisateur créé"