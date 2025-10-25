# codespot/account_service/app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Creamos las instancias VACÍAS
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()