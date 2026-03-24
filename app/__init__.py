from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)

    from app.routes.utilisateur_routes import utilisateur_bp
    from app.routes.bien_routes import bien_bp

    app.register_blueprint(utilisateur_bp)
    app.register_blueprint(bien_bp)

    return app