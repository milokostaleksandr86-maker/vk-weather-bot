import logging
import threading
import os
import sys
from flask import Flask
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    logger.info(">>> run_bot() запущена")
    try:
        import vk_bot
        logger.info("Запуск vk_bot.main()")
        vk_bot.main()
    except Exception as e:
        logger.error("Ошибка в боте:", exc_info=True)

# Проверяем, что мы в воркере, а не в мастер-процессе
# gunicorn передаёт переменную окружения, которую можно проверить
if os.environ.get('GUNICORN_MODE') == 'worker' or 'gunicorn' in os.environ.get('_', ''):
    logger.info("Запуск бота в воркере")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
else:
    logger.info("Мастер-процесс gunicorn, бот не запускается")
