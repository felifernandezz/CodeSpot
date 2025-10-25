# CodeSpot/accounnt_service/app/main.py

import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_HOST = "postgres_db" # <-- IMPORTANTE: Este es el nombre del *servicio* en docker-compose

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}'

@app.route('/')
def index():
    return jsonify(message="¡El servicio de Cuentas (Flask) está funcionando!")

@app.route('/test-db')
def test_db():
    try:
        if DB_HOST in app.config['SQLALCHEMY_DATABASE_URI']:
            return jsonify(message="Configuración de DB cargada correctamente.")
        else:
            return jsonify(message="Error al cargar la config de la DB.")
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)