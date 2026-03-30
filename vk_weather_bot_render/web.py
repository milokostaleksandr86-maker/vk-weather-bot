import logging
import threading
import os
import sys
from flask import Flask
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    logger.info("Функция run_bot() вызвана")
    try:
        logger.info("Попытка импортировать vk_bot...")
        import vk_bot
        logger.info("Модуль vk_bot импортирован. Вызов vk_bot.main()...")
        vk_bot.main()
    except Exception as e:
        logger.error("❌ Ошибка при запуске бота:", exc_info=True)

if __name__ == "__main__":
    logger.info("Запуск потока бота")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Поток бота запущен")
    
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Запуск веб-сервера на порту {port}")
    app.run(host='0.0.0.0', port=port)
