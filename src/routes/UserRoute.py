from flask import Blueprint, request, jsonify
from src.services.UserService import UserService
from src.models.User import user_schema, users_schema

user_bp = Blueprint('user', __name__)


@user_bp.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    new_user = UserService.create_user(name, email, phone)
    
    response = {
        'code': 1,
        'mensaje': 'Usuario creado exitosamente',
        'usuario': user_schema.dump(new_user)
    }

    return jsonify(response), 201


@user_bp.route('/users', methods=['GET'])
def get_users():
    all_users = UserService.get_all_users()
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


@user_bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = UserService.get_user_by_id(id)
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


@user_bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    name = request.json['name']
    email = request.json['email']
    phone = request.json['phone']

    user = UserService.update_user(id, name, email, phone)
    if not user:
        return jsonify({
            'code': -2,
            'mensaje': 'El usuario no existe en la base de datos'
        }), 404
    
    return jsonify({
        'code': 2,
        'mensaje': 'El usuario fue corregido exitosamente',
        'usuario_corregido': user_schema.dump(user)
    }), 201


@user_bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = UserService.delete_user(id)
    if not user:
        return jsonify({
            'code': -2,
            'mensaje': 'El usuario no existe en la base de datos'
        }), 404
    
    return jsonify({
        'code': 3,
        'mensaje': 'El usuario fue eliminado exitosamente',
        'usuario_eliminado': user_schema.dump(user)
    }), 200