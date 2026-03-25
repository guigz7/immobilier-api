from app import db

class Bien(db.Model):
    __tablename__ = "bien"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    description = db.Column(db.String(255))
    type_bien = db.Column(db.String(50))
    ville = db.Column(db.String(50))
    
    id_proprietaire = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

    pieces = db.relationship("Piece", backref="bien", lazy=True)