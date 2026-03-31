import logging
import threading
import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Принудительный вывод в stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)
logger = logging.getLogger(__name__)

logger.info("=== web.py загружается ===")

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    logger.info(">>> run_bot() запущена")
    try:
        logger.info("Импорт vk_bot...")
        import vk_bot
        logger.info("Запуск vk_bot.main()")
        vk_bot.main()
    except Exception as e:
        logger.error("Ошибка в боте:", exc_info=True)

# ЗАПУСКАЕМ БОТА СРАЗУ ПРИ ЗАГРУЗКЕ МОДУЛЯ
logger.info("Создаём поток для бота")
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
logger.info("Поток бота запущен из глобального кода")
