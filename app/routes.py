# define os endpoints da API
from flask import Blueprint, jsonify  # pyright: ignore[reportMissingImports]
from app import db
from app.models import Cidade, Leitura
from app.weather_service import buscar_clima_atual, buscar_qualidade_ar

main = Blueprint('main', __name__)


@main.route('/api/clima/<nome_cidade>', methods=['GET'])
def obter_clima(nome_cidade):
    """Busca o clima atual, salva no banco e retorna pro cliente."""
    clima = buscar_clima_atual(nome_cidade)

    if clima is None:
        return jsonify({'erro': 'Cidade não encontrada'}), 404

    dados_ar = buscar_qualidade_ar(clima['latitude'], clima['longitude'])
    aqi_valor = dados_ar['aqi'] if dados_ar else None

    # Verifica se a cidade já existe no banco, senão cria
    cidade = Cidade.query.filter_by(nome=nome_cidade).first()
    if cidade is None:
        cidade = Cidade(
            nome=nome_cidade,
            latitude=clima['latitude'],
            longitude=clima['longitude']
        )
        db.session.add(cidade)
        db.session.commit()

    # Salva a leitura atual
    leitura = Leitura(
        cidade_id=cidade.id,
        temperatura=clima['temperatura'],
        umidade=clima['umidade'],
        descricao=clima['descricao'],
        indice_qualidade_ar=aqi_valor
    )
    db.session.add(leitura)
    db.session.commit()

    return jsonify({
        'cidade': nome_cidade,
        'temperatura': clima['temperatura'],
        'umidade': clima['umidade'],
        'descricao': clima['descricao'],
        'indice_qualidade_ar': dados_ar
    }), 200

@main.route('/api/historico/<nome_cidade>', methods=['GET'])
def obter_historico(nome_cidade):
    """Retorna as leituras salvas de uma cidade."""
    cidade = Cidade.query.filter_by(nome=nome_cidade).first()

    if cidade is None:
        return jsonify({'erro': 'Cidade não encontrada'}), 404

    leituras = Leitura.query.filter_by(cidade_id=cidade.id).order_by(Leitura.criado_em.desc()).all()

    return jsonify([{
        'temperatura': l.temperatura,
        'umidade': l.umidade,
        'descricao': l.descricao,
        'indice_qualidade_ar': l.indice_qualidade_ar,
        'data': l.criado_em.isoformat()
    } for l in leituras]), 200