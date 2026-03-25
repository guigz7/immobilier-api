from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.utilisateur_routes import utilisateur_bp
    from app.routes.bien_routes import bien_bp
    from app.routes.piece_routes import piece_bp

    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(bien_bp)
    app.register_blueprint(piece_bp)

    return app