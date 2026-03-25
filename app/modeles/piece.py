from app import db

class Piece(db.Model):
    __tablename__ = "piece"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    surface = db.Column(db.Float)
    
    id_bien = db.Column(db.Integer, db.ForeignKey('bien.id'))