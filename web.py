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
    try:
        import vk_bot
        vk_bot.main()
    except Exception as e:
        logger.error("Ошибка в боте:", exc_info=True)

# ЗАПУСКАЕМ БОТА СРАЗУ ПРИ ЗАГРУЗКЕ МОДУЛЯ
logger.info("Запуск бота в отдельном потоке")
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
logger.info("Поток бота запущен")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
