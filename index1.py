from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/user_flask_udemy'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    __table__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(11), nullable=False)  
    
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone
        
with app.app_context():
    db.create_all()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


user_schema = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/users', methods=['POST'])
def create_user():
  name = request.json['name']
  email = request.json['email']
  phone = request.json['phone']

  new_user= User(name, email, phone)

  db.session.add(new_user)
  db.session.commit()
  
  response = {
      'code': 1,
      'mensaje': 'Usuario creado exitosamente',
      'usuario': user_schema.dump(new_user)
  }

  return jsonify(response), 201

@app.route('/users', methods=['GET'])
def get_users():
  all_users = User.query.all()
  if not all_users:
      return jsonify({
          'code': -1,
          'mensaje': 'No hay informacion en la base de datos'
      }), 404
  response = users_schema.dump(all_users)
  return jsonify({
      'code': 0,
      'mensaje': 'Usuarios encontrados',
      'usuarios': response
  })

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
  user = User.query.get(id)
  if not user:
      return jsonify({
          'code': -2,
          'mensaje': 'El usuario no existe en la base de datos'
      }), 404
  response = user_schema.dump(user)
  return jsonify({
      'code': 0,
      'mensaje': 'Usuario encontrado',
      'usuario': response
  })

@app.route('/users/<id>', methods=['PUT'])
def update_task(id):
    user = User.query.get(id)
    if not user:
        return jsonify({
            'code': -2,
            'mensaje': 'El usuario no existe en la base de datos'
        }), 404
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    user.name = name
    user.email = email
    user.phone = phone

    db.session.commit()
    
    return jsonify({
            'code': 2,
            'mensaje': 'El usuario fue corregido exitosamente',
            'usuario_corregido': user_schema.dump(user)
        }), 201


@app.route('/users/<id>', methods=['DELETE'])
def delete_task(id):
    user = User.query.get(id)
    if not user:
        return jsonify({
            'code': -2,
            'mensaje': 'El usuario no existe en la base de datos'
        }), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({
            'code': 3,
            'mensaje': 'El usuario fue eliminado exitosamente',
            'usuario_eliminado': user_schema.dump(user)
        }), 200


@app.route('/', methods=['GET'])
def index():
    return jsonify({'code': '∞', 'mensaje': 'Bienvenido a mi API de prueba'})


if __name__ == "__main__":
    app.run(debug=True)