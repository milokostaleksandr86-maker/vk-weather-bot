import logging
import threading
import os
import sys
from flask import Flask
from dotenv import load_dotenv

# Принудительно пишем в stdout, чтобы Render точно показал логи
logging.basicConfig(level=logging.INFO, stream=sys.stdout, force=True)
logger = logging.getLogger(__name__)

logger.info("=== Файл web.py загружен ===")

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    logger.info(">>> run_bot() вызвана")
    try:
        logger.info("Попытка импорта vk_bot...")
        import vk_bot
        logger.info("Импорт успешен, запускаю vk_bot.main()")
        vk_bot.main()
    except Exception as e:
        logger.error("Ошибка в боте:", exc_info=True)

if __name__ == "__main__":
    logger.info("Запуск потока бота")
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Поток бота запущен")
    
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Запуск Flask на порту {port}")
    app.run(host='0.0.0.0', port=port)
