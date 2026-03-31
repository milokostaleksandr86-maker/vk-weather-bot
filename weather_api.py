import requests
import logging

logger = logging.getLogger(__name__)

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "http://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",
                "lang": "ru"
            }
            r = requests.get(self.url, params=params, timeout=10)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return None

    def format_weather(self, data):
        city = data.get("name", "Неизвестно")
        temp = data.get("main", {}).get("temp", 0)
        desc = data.get("weather", [{}])[0].get("description", "")
        return f"🌤 {city}: {temp:.1f}°C, {desc}"
