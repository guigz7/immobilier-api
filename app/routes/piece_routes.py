from app.modeles.piece import Piece

@bien_bp.route("/pieces", methods=["POST"])
def ajouter_piece():
    data = request.form

    piece = Piece(
        nom=data["nom"],
        taille=data["taille"],
        bien_id=data["bien_id"]
    )

    db.session.add(piece)
    db.session.commit()

    return "Pièce ajoutée"