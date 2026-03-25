from flask import Blueprint, request, jsonify, render_template
from datetime import datetime
from app.modeles.utilisateur import Utilisateur
from app import db

utilisateur_bp = Blueprint("utilisateur", __name__)

@utilisateur_bp.route("/users/form", methods=["GET"])
def form_utilisateur():
    return render_template("utilisateur.html")

@utilisateur_bp.route("/users", methods=["POST"])
def creer_utilisateur():
    data = request.form if request.form else request.json

    try:
        data_date = datetime.strptime(data["date_naissance"], "%d/%m/%Y").date()
    except ValueError:
        return {"error": "format date invalide (jj/mm/aaaa attendu)"}, 400

    user = Utilisateur(
        prenom=data["prenom"],
        nom=data["nom"],
        date_naissance=data_date
    )

    db.session.add(user)
    db.session.commit()

    return """
    <h2>Utilisateur créé</h2>
    
    <a href="/">Retour à l'accueil</a><br>
    <a href="/users/form">Créer un autre utilisateur</a>
    """