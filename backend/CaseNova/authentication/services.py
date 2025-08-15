import requests
import logging
from core.constants import STEAM_GET_USER_INFO_URL
from django.conf import settings


def get_steam_user_summary(steam_id):
    params = {
        'key': settings.STEAM_API_KEY,
        'steamids': steam_id,
    }
    
    try:
        response = requests.get(
            "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/",
            params=params,
            timeout=10
        )
        response.raise_for_status()  # Проверка на HTTP-ошибки (4xx, 5xx)
        
        data = response.json()
        players = data.get("response", {}).get("players", [])
        
        if not players:
            print("Steam API вернул пустой список players")
            return None
        
        return players[0]  # Возвращаем первого пользователя
        
    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса к Steam API: {e}")
        return None
    except (KeyError, IndexError, ValueError) as e:
        print(f"Ошибка парсинга ответа Steam API: {e}")
        return None