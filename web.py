import threading
import os
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "VK Bot is running!"

def run_bot():
    import vk_bot
    vk_bot.main()

# Запускаем бота в фоне при старте
bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
