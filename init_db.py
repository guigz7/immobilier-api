from datetime import datetime
from app import create_app, db
from app.modeles.utilisateur import Utilisateur
from app.modeles.bien import Bien
from app.modeles.piece import Piece

app = create_app()

with app.app_context():
    # 🔹 Reset de la base
    db.drop_all()
    db.create_all()

    # ------------------------
    # 1️⃣ Utilisateurs
    # ------------------------
    utilisateurs_data = [
        {"prenom": "Jean", "nom": "Martin", "date_naissance": "22/08/1990"},
        {"prenom": "Marie", "nom": "Dubois", "date_naissance": "15/02/1985"},
        {"prenom": "Luc", "nom": "Petit", "date_naissance": "03/11/1992"},
        {"prenom": "Sophie", "nom": "Lefevre", "date_naissance": "28/07/1988"},
        {"prenom": "Paul", "nom": "Moreau", "date_naissance": "12/12/1995"}
    ]

    users = []
    for data in utilisateurs_data:
        user = Utilisateur(
            prenom=data["prenom"],
            nom=data["nom"],
            date_naissance=datetime.strptime(data["date_naissance"], "%d/%m/%Y").date()
        )
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print("5 utilisateurs de test ajoutés !")

    # ------------------------
    # 2️⃣ Biens
    # ------------------------
    biens_data = [
        {"nom": "Appartement 14e", "description": "Bel appartement situé dans le 14e",
         "type_bien": "Appartement", "ville": "Paris", "proprietaire_idx": 0},
        {"nom": "Loft Moderne", "description": "Loft spacieux et lumineux",
         "type_bien": "Loft", "ville": "Paris", "proprietaire_idx": 1},
        {"nom": "Studio Lumineux", "description": "Petit studio très lumineux",
         "type_bien": "Studio", "ville": "Paris", "proprietaire_idx": 2},
        {"nom": "Studio Cozy", "description": "Studio parfait pour étudiant",
         "type_bien": "Studio", "ville": "Marseille", "proprietaire_idx": 0},
        {"nom": "Appartement Vue Mer", "description": "Appartement avec vue sur la mer",
         "type_bien": "Appartement", "ville": "Marseille", "proprietaire_idx": 3},
        {"nom": "Maison Jardin", "description": "Maison avec grand jardin",
         "type_bien": "Maison", "ville": "Lyon", "proprietaire_idx": 4},
        {"nom": "Appartement Centre", "description": "Bel appartement dans le centre",
         "type_bien": "Appartement", "ville": "Bordeaux", "proprietaire_idx": 1}
    ]

    biens = []
    for data in biens_data:
        proprietaire = users[data["proprietaire_idx"]]
        bien = Bien(
            nom=data["nom"],
            description=data["description"],
            type_bien=data["type_bien"],
            ville=data["ville"],
            id_proprietaire=proprietaire.id
        )
        db.session.add(bien)
        biens.append(bien)

    db.session.commit()
    print("7 biens de test ajoutés !")

    # ------------------------
    # 3️⃣ Pièces
    # ------------------------
    pieces_data = {
        "Appartement 14e": [
            {"nom": "Salon", "surface": 25},
            {"nom": "Chambre", "surface": 15}
        ],
        "Appartement Vue Mer": [
            {"nom": "Salon", "surface": 30},
            {"nom": "Chambre principale", "surface": 20}
        ]
    }

    for bien_nom, pieces_list in pieces_data.items():
        bien = next((b for b in biens if b.nom == bien_nom), None)
        if bien:
            for p in pieces_list:
                piece = Piece(nom=p["nom"], surface=p["surface"], id_bien=bien.id)
                db.session.add(piece)

    db.session.commit()
    print("4 pièces ajoutées !")

    print("Données de test ajoutées !")