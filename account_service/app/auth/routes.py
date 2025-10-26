# codespot/account_service/app/auth/routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
    
@auth_bp.route('/login', methods=['POST'])
def login_user():
    data= request.get_json()
    email=data.get('email')
    password=data.get('password')
    
    if not email or not password:
        return jsonify({"error":"Email y password son requeridos"}),400
    
    user=User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"error": "Credenciales inválidas"}), 401
    
    access_token=create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token),200

@auth_bp.route('/profile/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    user_id=get_jwt_identity()
    user=User.query.get(user_id)
    
    if not user:
        return jsonify({"error": "Usuario no encontrado"}),404
    
    return jsonify({
        "username": user.profile.username,
        "email": user.email
    }),200
    
    