from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def init_db(app):
    """Inicializa la base de datos con la aplicación Flask"""
    db.init_app(app)
    ma.init_app(app)
    
    with app.app_context():
        db.create_all()