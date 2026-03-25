from flask import Blueprint, request, jsonify, render_template, redirect, session
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

@utilisateur_bp.route("/users_form", methods=["GET", "POST"])
def form_acces_utilisateur():
    if request.method == "GET":
        return render_template("utilisateur_form.html")

    data = request.form

    try:
        date = datetime.strptime(data["date_naissance"], "%d/%m/%Y").date()
    except:
        return "Format date invalide", 400

    user = Utilisateur.query.filter_by(
        prenom=data["prenom"],
        nom=data["nom"],
        date_naissance=date
    ).first()

    if not user:
        return "Utilisateur introuvable", 404

    return redirect(f"/users/{user.id}")

@utilisateur_bp.route("/users/<int:id>", methods=["GET"])
def detail_utilisateur(id):
    utilisateur = Utilisateur.query.get(id)

    if not utilisateur:
        return "Utilisateur introuvable", 404

    return render_template("utilisateur_detail.html", utilisateur=utilisateur)

@utilisateur_bp.route("/users/<int:id>/edit", methods=["GET", "POST"])
def modifier_utilisateur(id):
    if "user_id" not in session or session["user_id"] != id:
        return "Non autorisé", 403
        
    utilisateur = Utilisateur.query.get(id)

    if not utilisateur:
        return "Utilisateur introuvable", 404

    if request.method == "GET":
        return render_template("utilisateur_edit.html", utilisateur=utilisateur)

    data = request.form

    try:
        date = datetime.strptime(data["date_naissance"], "%d/%m/%Y").date()
    except:
        return "Format date invalide", 400

    utilisateur.prenom = data["prenom"]
    utilisateur.nom = data["nom"]
    utilisateur.date_naissance = date

    db.session.commit()

    return redirect(f"/users/{utilisateur.id}")

@utilisateur_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST
    prenom = request.form.get("prenom")
    nom = request.form.get("nom")
    date_naissance_str = request.form.get("date_naissance")

    try:
        date_naissance = datetime.strptime(date_naissance_str, "%d/%m/%Y").date()
    except:
        return "Format date invalide", 400

    user = Utilisateur.query.filter_by(
        prenom=prenom,
        nom=nom,
        date_naissance=date_naissance
    ).first()

    if not user:
        return "Utilisateur introuvable", 404

    session["user_id"] = user.id

    return redirect("/")

@utilisateur_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")