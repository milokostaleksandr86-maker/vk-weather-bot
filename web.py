import sys
import logging
import threading
import os
from flask import Flask
from dotenv import load_dotenv

# Настройка логирования, чтобы всё писалось в консоль Render
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    """Запускает VK бота в отдельном потоке с обработкой ошибок"""
    try:
        logger.info("Пытаюсь импортировать vk_bot...")
        import vk_bot
        logger.info("vk_bot импортирован успешно. Запускаю main()...")
        vk_bot.main()
    except Exception as e:
        logger.error(f"Ошибка в боте: {e}", exc_info=True)

if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Поток бота запущен")
    
    # Запускаем веб-сервер
    port = int(os.environ.get("PORT", 10000))
    logger.info(f"Запуск веб-сервера на порту {port}")
    app.run(host='0.0.0.0', port=port)
