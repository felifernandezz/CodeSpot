# codespot/account_service/app/auth/routes.py

from flask import Blueprint, request, jsonify
from ..extensions import db, bcrypt  
from ..models import User, Profile   


auth_bp = Blueprint('auth', __name__)

# 2. Creamos la ruta DENTRO del blueprint
@auth_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not username or not password:
        return jsonify({"error": "Email, username y password son requeridos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El email ya está registrado"}), 400
    if Profile.query.filter_by(username=username).first():
        return jsonify({"error": "El nombre de usuario ya existe"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(email=email, password_hash=password_hash)
    new_profile = Profile(username=username, user=new_user)

    try:
        db.session.add(new_user)
        db.session.add(new_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear la cuenta: {str(e)}"}), 500

    return jsonify({
        "message": "Usuario registrado exitosamente",
        "user": {"email": new_user.email},
        "profile": {"username": new_profile.username}
    }), 201
    
@auth_bp.route('/profile/<string:username>', methods=['GET'])
def return_user_profile(username):
    profile = Profile.query.filter_by(username=username).first()
    if not profile:
        return jsonify({"error": "Perfil no encontrado"}), 404

    return jsonify({
        "username": profile.username,
        "email": profile.user.email
    }), 200