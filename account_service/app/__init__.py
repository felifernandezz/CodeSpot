# codespot/account_service/app/__init__.py

import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from .extensions import db, migrate, bcrypt, jwt
from . import models

# Cargamos variables de entorno
load_dotenv()

def create_app():
    app = Flask(__name__) # Nace la app

    # --- Configuración ---
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")
    DB_NAME = os.environ.get("POSTGRES_DB")
    DB_HOST = "postgres_db"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")
    
    # --- Conectar Extensiones ---
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # --- Registrar Blueprints ---
    # Importamos nuestro blueprint
    from .auth.routes import auth_bp
    # Registramos el blueprint en la app
    app.register_blueprint(auth_bp)


    # --- Rutas de Prueba (podemos moverlas a su propio blueprint luego) ---
    @app.route('/')
    def index():
        return jsonify(message="¡El servicio de Cuentas (Flask) está funcionando!")

    @app.route('/test-db')
    def test_db():
        try:
            user_count = db.session.query(models.User).count()
            return jsonify(
                message="Conexión a la DB exitosa.",
                user_count=user_count
            )
        except Exception as e:
            return jsonify(error=f"Error al conectar a la DB: {str(e)}"), 500

    return app # Devolvemos la app creada