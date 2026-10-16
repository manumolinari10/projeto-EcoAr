# cria e configura a aplicação
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()  # carrega as variáveis do .env

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuração do banco de dados (SQLite pra começar, é um arquivo só)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:senha_aqui@localhost/clima_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)  # permite que o frontend acesse essa API

    with app.app_context():
        from app import models  # importa os models pra criar as tabelas
        db.create_all()

        from app.routes import main
        app.register_blueprint(main)

    return app