from flask import Blueprint, redirect, session
from app.modeles.piece import Piece
from app import db

piece_bp = Blueprint("pieces", __name__)

@piece_bp.route("/pieces", methods=["POST"])
def ajouter_piece():
    if "user_id" not in session or session["user_id"] != id:
         "Non autorisé", 403

    data = request.form

    piece = Piece(
        nom=data["nom"],
        taille=data["taille"],
        bien_id=data["id_bien"]
    )

    db.session.add(piece)
    db.session.commit()

    return "Pièce ajoutée"

@piece_bp.route("/pieces/<int:id>/delete", methods=["POST"])
def supprimer_piece(id):
    if "user_id" not in session or session["user_id"] != id:
        return "Non autorisé", 403

    piece = Piece.query.get(id)

    if not piece:
        return "Pièce introuvable", 404

    bien_id = piece.id_bien

    db.session.delete(piece)
    db.session.commit()

    return redirect(f"/biens/{bien_id}")