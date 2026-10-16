# lógica de comunicação com OpenWeatherMap
import os
import requests

API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5"

def buscar_clima_atual(nome_cidade):
    """Busca o clima atual de uma cidade pelo nome."""
    url = f"{BASE_URL}/weather"
    params = {
        'q': nome_cidade,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'pt_br'
    }

    try:
        resposta = requests.get(url, params=params, timeout=5)
        resposta.raise_for_status() 
        dados = resposta.json()
        
        return {
            'temperatura': dados['main']['temp'],
            'umidade': dados['main']['humidity'],
            'descricao': dados['weather'][0]['description'],
            'latitude': dados['coord']['lat'],
            'longitude': dados['coord']['lon']
        }
    except Exception:
        return None

def buscar_qualidade_ar(latitude, longitude):
    """Busca o AQI e os gases específicos por coordenadas."""
    url = f"{BASE_URL}/air_pollution"
    params = {
        'lat': latitude,
        'lon': longitude,
        'appid': API_KEY
    }

    try:
        resposta = requests.get(url, params=params, timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
        
        aqi = dados['list'][0]['main']['aqi']
        gases = dados['list'][0]['components']
        
        return {
            'aqi': aqi,
            'pm2_5': gases.get('pm2_5', 0),
            'pm10': gases.get('pm10', 0),
            'no2': gases.get('no2', 0),
            'o3': gases.get('o3', 0),
            'co': gases.get('co', 0)
        }
    except Exception:
        return None