import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from flask import Flask
from threading import Thread
import time
import asyncio

# === 1. Настройка логирования (ОЧЕНЬ важно для отладки) ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === 2. Flask app для веб-сервера (чтобы Render был доволен) ===
app_flask = Flask(__name__)

@app_flask.route('/')
def home():
    return "Telegram Bot is running!"

@app_flask.route('/health')
def health():
    return "OK", 200

# === 3. Код вашего бота ===
TOKEN = os.environ.get('TOKEN')
WEB_APP_URL = "https://tso-tu.github.io/competitions-miniapp/"

async def start(update: Update, context):
    bot_username = context.bot.username
    keyboard = [[
        InlineKeyboardButton(
            "📱 ОТКРЫТЬ В ТЕЛЕГРАМ",
            url=f"https://t.me/{bot_username}?startapp=competitions-miniapp"
        )
    ]]
    message_text = """🎯 <b>Конкурсы и соревнования Академии ТОП</b>
    
    🚀 <b>В приложении вы можете:</b>

    1️⃣ <b>Посмотреть информацию о конкурсах</b>
       • Полный список мероприятий
       • Условия и требования
       • Сроки проведения

    2️⃣ <b>Принять участие в конкурсах</b>
       • Простая и быстрая регистрация
       • Загрузка работ
       • Отслеживание статуса

    3️⃣ <b>Задать интересующие вопросы</b>
       • Оставить комментарии

    4️⃣ <b>Проголосовать за понравившиеся работы</b>
       • Оценка работ
       • Рейтинги участников
       • Подведение итогов

    ✨ <b>Все функции доступны в нашем мини-приложении!</b>
    """
    await update.message.reply_text(
        message_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

def run_bot():
    """Функция для запуска бота в отдельном потоке с собственным event loop"""
    if not TOKEN:
        logger.error("КРИТИЧЕСКАЯ ОШИБКА: Переменная окружения 'TOKEN' не задана.")
        return

    try:
        logger.info("Запускаю бота в отдельном потоке...")
        
        # 1. Создаем новый event loop для этого потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # 2. Создаем и настраиваем приложение бота
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        
        logger.info("Бот успешно инициализирован. Начинаю polling...")
        
        # 3. Запускаем бота в созданном event loop
        loop.run_until_complete(app.run_polling())
        
    except Exception as e:
        logger.error(f"Бот упал с ошибкой: {e}", exc_info=True)
    finally:
        # При завершении закрываем loop
        if loop and not loop.is_closed():
            loop.close()

# === 4. Функция для self-ping (чтобы сервис не засыпал) ===
def start_ping():
    """Периодически отправляет запросы к собственному серверу"""
    import requests
    while True:
        try:
            # Пингуем только если знаем свой публичный URL (т.е. работаем на Render)
            if 'RENDER_EXTERNAL_URL' in os.environ:
                url = os.environ['RENDER_EXTERNAL_URL']
                # Пингуем эндпоинт /health, а не корневой
                requests.get(f"{url}/health", timeout=10)
                logger.debug(f"Self-ping отправлен на {url}")
        except requests.exceptions.RequestException as e:
            # Логируем ошибку, но не прерываем цикл
            logger.warning(f"Не удалось отправить ping: {e}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка в ping: {e}")
        # Ждем 4 минуты (меньше 5-минутного таймаута Render)
        time.sleep(240)

# === 5. Главная точка входа ===
if __name__ == '__main__':
    # Запускаем self-ping в отдельном потоке (как демон)
    ping_thread = Thread(target=start_ping, daemon=True)
    ping_thread.start()
    logger.info("Поток для self-ping запущен.")

    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Поток для бота запущен.")

    # Запускаем Flask-сервер (блокирующий вызов в основном потоке)
    # Для production можно использовать waitress или gunicorn, но для начала хватит и этого.
    logger.info("Запускаю Flask-сервер...")
    app_flask.run(host='0.0.0.0', port=8080)

