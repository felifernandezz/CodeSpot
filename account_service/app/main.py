# codespot/account_service/app/main.py

import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy  # Importar SQLAlchemy
from flask_migrate import Migrate      # Importar Migrate


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


app = Flask(__name__) 


DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "postgres_db" 

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)
migrate.init_app(app, db)

from . import models



@app.route('/')
def index():
    """Ruta de prueba para ver si el servicio está vivo."""
    return jsonify(message="¡El servicio de Cuentas (Flask) está funcionando!")

@app.route('/test-db')
def test_db():
    """Prueba que podamos hacer una consulta simple a la DB."""
    try:
        user_count = db.session.query(models.User).count()
        return jsonify(
            message="Conexión a la DB exitosa.",
            user_count=user_count
        )
    except Exception as e:
        
        return jsonify(error=f"Error al conectar a la DB: {str(e)}"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)