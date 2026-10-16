import pytest  # type: ignore[import-not-found]
from app import create_app, db


@pytest.fixture
def client():   #prepara um "ambiente limpo" antes de cada teste, com banco de dados em memória (não mexe no seu clima.db real).
    """Cria uma aplicação de teste com banco de dados temporário em memória."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client


def test_clima_cidade_nao_encontrada(client, mocker):
    """Se a cidade não existe, deve retornar 404."""
    mocker.patch('app.routes.buscar_clima_atual', return_value=None)   #substitui temporariamente a função real por uma que retorna um valor fixo, simulando a resposta da API sem chamá-la de verdade

    resposta = client.get('/api/clima/CidadeQueNaoExiste')

    assert resposta.status_code == 404   #a verificação em si: "isso tem que ser verdade, senão o teste falha"
    assert resposta.get_json()['erro'] == 'Cidade não encontrada'


def test_clima_sucesso(client, mocker):
    """Se a cidade existe, deve retornar 200 com os dados esperados."""
    mocker.patch('app.routes.buscar_clima_atual', return_value={
        'temperatura': 25.0,
        'umidade': 60,
        'descricao': 'céu limpo',
        'latitude': -22.7,
        'longitude': -45.1
    })

    mocker.patch('app.routes.buscar_qualidade_ar', return_value= {
        'aqi': 2, 'pm2_5': 10, 'pm10': 15, 'no2': 5, 'o3': 12, 'co': 0
    })

    resposta = client.get('/api/clima/Lorena')
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert dados['temperatura'] == 25.0
    assert dados['qualidade_ar'] ['aqi'] == 2


def test_historico_cidade_nao_encontrada(client):
    """Histórico de cidade que nunca foi consultada deve retornar 404."""
    resposta = client.get('/api/historico/CidadeInexistente')

    assert resposta.status_code == 404


def test_historico_apos_consulta(client, mocker):
    """Depois de consultar o clima, o histórico deve conter a leitura."""
    mocker.patch('app.routes.buscar_clima_atual', return_value={
        'temperatura': 30.0,
        'umidade': 50,
        'descricao': 'ensolarado',
        'latitude': -23.5,
        'longitude': -46.6
    })

    mocker.patch('app.routes.buscar_qualidade_ar', return_value= {
        'aqi': 1, 'pm2_5': 5, 'pm10': 8, 'no2': 2, 'o3': 6, 'co': 0
    })

    client.get('/api/clima/SaoPaulo')  # gera a leitura
    resposta = client.get('/api/historico/SaoPaulo')
    dados = resposta.get_json()

    assert resposta.status_code == 200
    assert len(dados) == 1
    assert dados[0]['temperatura'] == 30.0