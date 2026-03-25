from flask import Flask, session, render_template
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    app.config['SECRET_KEY'] = 'cle_pour_session'

    db.init_app(app)

    from app.modeles.utilisateur import Utilisateur
    from app.routes.utilisateur_routes import utilisateur_bp
    from app.routes.bien_routes import bien_bp
    from app.routes.piece_routes import piece_bp

    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(bien_bp)
    app.register_blueprint(piece_bp)

    @app.route("/")
    def accueil():
        user = None
        if "user_id" in session:
            user = Utilisateur.query.get(session["user_id"])
        return render_template("index.html", user=user)

    return app