from flask import Blueprint, request, jsonify, render_template, redirect
from app.modeles.bien import Bien
from app.modeles.utilisateur import Utilisateur
from app.modeles.piece import Piece
from app import db

bien_bp = Blueprint("bien", __name__)

@bien_bp.route("/biens/form", methods=["GET"])
def form_bien():
    users = Utilisateur.query.all()
    return render_template("bien.html", utilisateurs=users)

@bien_bp.route("/biens", methods=["POST"])
def creer_bien():
    data = request.form if request.form else request.json

    bien = Bien(
        nom=data["nom"],
        description=data["description"],
        type_bien=data["type_bien"],
        ville=data["ville"],
        id_proprietaire=data["proprietaire_id"]
    )

    db.session.add(bien)
    db.session.commit()

    return """
    <h2>Bien créé</h2>
    
    <a href="/">Retour à l'accueil</a><br>
    <a href="/biens/form">Créer un autre bien</a>
    """

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

@bien_bp.route("/biens/<int:id>", methods=["GET"])
def detail_bien(id):
    bien = Bien.query.get(id)

    if not bien:
        return "Bien introuvable", 404

    return render_template("bien_detail.html", bien=bien)

@bien_bp.route("/biens/<int:id>/edit", methods=["GET"])
def form_modifier_bien(id):
    bien = Bien.query.get(id)
    return render_template("bien_edit.html", bien=bien)

@bien_bp.route("/biens/<int:id>/edit", methods=["POST"])
def modifier_bien(id):
    bien = Bien.query.get(id)

    if not bien:
        return "Bien introuvable", 404

    data = request.form

    bien.nom = data.get("nom", bien.nom)
    bien.description = data.get("description", bien.description)
    bien.type_bien = data.get("type_bien", bien.type_bien)
    bien.ville = data.get("ville", bien.ville)

    db.session.commit()

    return redirect(f"/biens/{bien.id}")

@bien_bp.route("/biens/<int:id>/pieces", methods=["POST"])
def ajouter_piece(id):
    bien = Bien.query.get(id)

    if not bien:
        return "Bien introuvable", 404

    data = request.form

    piece = Piece(
        nom=data["nom"],
        taille=data["taille"],
        bien_id=id
    )

    db.session.add(piece)
    db.session.commit()

    return redirect(f"/biens/{id}")