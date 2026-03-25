from app import db

class Utilisateur(db.Model):
    __tablename__ = "utilisateur"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    date_naissance = db.Column(db.Date)

    biens = db.relationship("Bien", backref="proprietaire", lazy=True)