# -*- coding: utf-8 -*-
"""
VK Погодный бот
Использует VK Long Poll API и OpenWeatherMap
"""

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv
import os
from weather_api import WeatherAPI

# Загружаем переменные окружения из файла .env
load_dotenv()

# Получаем токены из переменных окружения
VK_TOKEN = os.getenv("VK_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# ID группы (можно также взять из переменной окружения, если нужно)
GROUP_ID = 237196714

# Инициализация VK сессии
vk_session = vk_api.VkApi(token=VK_TOKEN)
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, GROUP_ID)

# Инициализация модуля погоды
weather = WeatherAPI(WEATHER_API_KEY)


def send_message(user_id: int, text: str) -> None:
    """
    Отправляет сообщение пользователю VK.
    
    Args:
        user_id: ID пользователя
        text: Текст сообщения
    """
    try:
        vk.messages.send(
            user_id=user_id,
            message=text,
            random_id=0
        )
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")


def handle_message(text: str, user_id: int) -> None:
    """
    Обрабатывает текстовое сообщение от пользователя.
    
    Args:
        text: Текст сообщения
        user_id: ID пользователя
    """
    # Приводим текст к нижнему регистру и убираем лишние пробелы
    text = text.lower().strip()
    
    # Команда /start или начать
    if text == "/start" or text == "начать":
        send_message(user_id, 
                     "👋 Привет! Я погодный бот.\n\n"
                     "📌 Команды:\n"
                     "/weather <город> — погода\n"
                     "/help — помощь")
    
    # Команда /help или помощь
    elif text == "/help" or text == "помощь":
        send_message(user_id,
                     "📖 Справка:\n"
                     "/weather Москва — погода в Москве\n"
                     "/weather London — погода в Лондоне\n"
                     "/start — приветствие")
    
    # Команда /weather <город>
    elif text.startswith("/weather"):
        # Разделяем команду и город
        parts = text.split(maxsplit=1)
        
        if len(parts) < 2:
            send_message(user_id, "❌ Укажи город. Пример: /weather Москва")
            return
        
        city = parts[1].strip()
        
        # Отправляем уведомление о начале поиска
        send_message(user_id, f"🔍 Ищу погоду в {city}...")
        
        # Получаем данные о погоде
        data = weather.get_weather(city)
        
        # Форматируем ответ
        if data:
            message = weather.format_weather(data)
        else:
            message = "❌ Город не найден. Проверьте название и попробуйте снова.\n\nПримеры: Москва, London, Санкт-Петербург"
        
        send_message(user_id, message)
    
    # Если команда не распознана
    else:
        send_message(user_id,
                     "❌ Неизвестная команда.\n"
                     "Используй /weather <город> или /help")


def main() -> None:
    """
    Основная функция запуска бота.
    Запускает прослушивание Long Poll и обрабатывает сообщения.
    """
    print("🤖 VK Бот запущен...")
    print(f"📦 ID группы: {GROUP_ID}")
    print("📨 Ожидание сообщений...")
    
    # Бесконечный цикл прослушивания событий
    for event in longpoll.listen():
        # Обрабатываем только новые сообщения
        if event.type == VkBotEventType.MESSAGE_NEW:
            message = event.obj.message
            user_id = message['from_id']
            text = message.get('text', '')
            
            # Выводим информацию в консоль (полезно для отладки)
            print(f"📩 Сообщение от {user_id}: {text}")
            
            # Обрабатываем сообщение
            handle_message(text, user_id)


# Точка входа при запуске скрипта напрямую
if __name__ == "__main__":
    main()