from flask import Blueprint, request, jsonify, render_template
from app.modeles.bien import Bien
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

@bien_bp.route("/biens", methods=["GET"])
def lister_biens():
    ville = request.args.get("ville")

    if ville:
        biens = Bien.query.filter_by(ville=ville).all()
    else:
        biens = Bien.query.all()

    result = []
    for b in biens:
        result.append({"nom": b.nom, "ville": b.ville})

    return jsonify(result)

@bien_bp.route("/biens/vue", methods=["GET"])
def vue_biens():
    ville = request.args.get("ville")

    if ville:
        biens = Bien.query.filter_by(ville=ville).all()
    else:
        biens = Bien.query.all()

    return render_template("liste_biens.html", biens=biens)

    @bien_bp.route("/biens/<int:id>", methods=["PUT"])
    def modifier_bien(id):
        user_id = request.headers.get("X-User-Id")
        bien = Bien.query.get(id)

        if str(bien.proprietaire_id) != user_id:
            return jsonify({"error": "non autorise"}), 403

        data = request.json
        bien.nom = data.get("nom", bien.nom)

        db.session.commit()

        return jsonify({"message": "modifie"})