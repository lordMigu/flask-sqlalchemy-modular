from flask import Flask
from src.database.MySQLDatabase import db


def init_app(config):
    """Crear y configurar la aplicación Flask.

    - Inicializa extensiones (db.init_app)
    - Registra blueprints importando las rutas dentro de la función
    Esto evita importaciones circulares al importar rutas que referencian a la app.
    """
    app = Flask(__name__)

    # Configuration
    app.config.from_object(config)

    # Inicializar extensiones
    db.init_app(app)

    # Blueprints (importar aquí para evitar circular imports)
    from .routes import UserRoute
    app.register_blueprint(UserRoute.main, url_prefix='/users')

    return app