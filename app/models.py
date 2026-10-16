# define as tabelas do banco de dados
from app import db
from datetime import datetime, timezone

class Cidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    pais = db.Column(db.String(50))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    leituras = db.relationship('Leitura', backref='cidade', lazy=True)

class Leitura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cidade_id = db.Column(db.Integer, db.ForeignKey('cidade.id'), nullable=False)
    temperatura = db.Column(db.Float)
    umidade = db.Column(db.Integer)
    descricao = db.Column(db.String(100))
    indice_qualidade_ar = db.Column(db.Integer, nullable=True)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))