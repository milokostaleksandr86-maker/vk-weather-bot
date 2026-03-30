import requests
from typing import Dict, Optional

class WeatherAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "http://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Optional[Dict]:
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru"
            }
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Ошибка: {e}")
            return None
    
    def format_weather(self, data: Dict) -> str:
        if not data:
            return "❌ Город не найден. Проверьте название."
        
        city = data.get("name", "Неизвестно")
        temp = data.get("main", {}).get("temp", 0)
        feels_like = data.get("main", {}).get("feels_like", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        description = data.get("weather", [{}])[0].get("description", "")
        
        # Выбор эмодзи
        weather_id = data.get("weather", [{}])[0].get("id", 800)
        emoji = self._get_emoji(weather_id)
        
        return f"""{emoji} Погода в городе {city}

🌡 Температура: {temp:.1f}°C
🤔 Ощущается как: {feels_like:.1f}°C
🌥 Состояние: {description.capitalize()}
💧 Влажность: {humidity}%

Для другого города напиши: /weather <город>"""
    
    def _get_emoji(self, weather_id: int) -> str:
        if weather_id >= 200 and weather_id < 300:
            return "⛈"
        elif weather_id >= 300 and weather_id < 600:
            return "🌧"
        elif weather_id >= 600 and weather_id < 700:
            return "❄️"
        elif weather_id >= 700 and weather_id < 800:
            return "🌫"
        elif weather_id == 800:
            return "☀️"
        else:
            return "☁️"