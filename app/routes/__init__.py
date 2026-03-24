from app.routes.utilisateur_routes import utilisateur_bp
from app.routes.bien_routes import bien_bp

app.register_blueprint(utilisateur_bp)
app.register_blueprint(bien_bp)