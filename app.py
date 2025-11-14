from flask import Flask, jsonify
from src.database.MySQLDatabase import init_db
from src.routes.UserRoute import user_bp
from config import get_config


def create_app():
    app = Flask(__name__)
    
    # Cargar configuración desde variables de entorno
    config = get_config()
    app.config.from_object(config)
    
    # Inicializar base de datos
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(user_bp)
    
    # Ruta principal
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({'code': '∞', 'mensaje': 'Bienvenido a mi API de prueba'})
    
    return app


if __name__ == "__main__":
    app = create_app()
    config = get_config()
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)