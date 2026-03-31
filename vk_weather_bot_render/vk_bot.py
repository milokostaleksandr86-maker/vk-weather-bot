import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv
import os
from weather_api import WeatherAPI

logger = logging.getLogger(__name__)

load_dotenv()

VK_TOKEN = os.getenv("VK_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GROUP_ID = 237196714  # твой ID группы

vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)
weather = WeatherAPI(WEATHER_API_KEY)

def send_message(user_id, text):
    try:
        vk.messages.send(user_id=user_id, message=text, random_id=0)
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")

def handle_message(text, user_id):
    text = text.lower().strip()
    if text == "/start" or text == "начать":
        send_message(user_id, "👋 Привет! Я погодный бот.\n/weather <город>")
    elif text.startswith("/weather"):
        parts = text.split(maxsplit=1)
        if len(parts) < 2:
            send_message(user_id, "❌ Укажи город. Пример: /weather Москва")
            return
        city = parts[1]
        data = weather.get_weather(city)
        if data:
            send_message(user_id, weather.format_weather(data))
        else:
            send_message(user_id, "❌ Город не найден")
    else:
        send_message(user_id, "Неизвестная команда. Используй /weather <город>")

def main():
    logger.info("🤖 VK Бот запущен...")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message
            user_id = msg['from_id']
            text = msg.get('text', '')
            logger.info(f"📩 {user_id}: {text}")
            handle_message(text, user_id)
