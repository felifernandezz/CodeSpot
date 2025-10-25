# codespot/account_service/wsgi.py

from app import create_app

# Llama a la fábrica para crear la instancia de la app
app = create_app()

if __name__ == '__main__':
    app.run()