from app import db

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50))
    prenom = db.Column(db.String(50))
    date_naissance = db.Column(db.String(20))