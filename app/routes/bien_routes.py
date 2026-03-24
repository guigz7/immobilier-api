from flask import Blueprint, request, jsonify
from app.models.bien import Bien
from app import db

bien_bp = Blueprint("bien", __name__)

@bien_bp.route("/biens/form", methods=["GET"])
def form_bien():
    return render_template("bien.html")

@bien_bp.route("/biens", methods=["POST"])
def creer_bien():
    data = request.form if request.form else request.json

    bien = Bien(
        nom=data["nom"],
        description=data["description"],
        type_bien=data["type_bien"],
        ville=data["ville"],
        proprietaire_id=data["proprietaire_id"]
    )

    db.session.add(bien)
    db.session.commit()

    return "Bien créé"