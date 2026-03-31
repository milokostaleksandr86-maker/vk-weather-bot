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

# Флаг, чтобы бот запустился только один раз
bot_started = False
bot_lock = threading.Lock()

def start_bot():
    global bot_started
    with bot_lock:
        if bot_started:
            return
        bot_started = True
    
    logger.info("Запуск бота в отдельном потоке")
    def run():
        try:
            import vk_bot
            vk_bot.main()
        except Exception as e:
            logger.error("Ошибка в боте:", exc_info=True)
    
    thread = threading.Thread(target=run, daemon=True)
    thread.start()

@app.route('/')
def home():
    # При первом запросе запускаем бота
    start_bot()
    return "VK Bot is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
