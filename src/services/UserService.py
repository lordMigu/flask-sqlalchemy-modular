from src.database.MySQLDatabase import db
from src.models.User import User


class UserService:
    
    @staticmethod
    def create_user(name, email, phone):
        """Crea un nuevo usuario en la base de datos"""
        new_user = User(name, email, phone)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def get_all_users():
        """Obtiene todos los usuarios"""
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario por su ID"""
        return User.query.get(user_id)
    
    @staticmethod
    def update_user(user_id, name, email, phone):
        """Actualiza un usuario existente"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        user.name = name
        user.email = email
        user.phone = phone
        db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id):
        """Elimina un usuario de la base de datos"""
        user = User.query.get(user_id)
        if not user:
            return None
        
        db.session.delete(user)
        db.session.commit()
        return user