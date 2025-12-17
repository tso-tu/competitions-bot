import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, TypeHandler
from flask import Flask, request, jsonify

app_flask = Flask(__name__)
TOKEN = os.environ.get('TOKEN')

# Получаем URL сервиса Render
RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL')
WEBHOOK_URL = f"{RENDER_EXTERNAL_URL}/webhook"

# Инициализация бота
application = Application.builder().token(TOKEN).build()

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

# Регистрация обработчика
application.add_handler(CommandHandler("start", start))

@app_flask.route('/')
def home():
    return "Bot is running!"

@app_flask.route('/webhook', methods=['POST'])
def webhook():
    """Эндпоинт для получения обновлений от Telegram"""
    update = Update.de_json(request.get_json(), application.bot)
    application.update_queue.put_nowait(update)
    return jsonify({'status': 'ok'})

@app_flask.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка webhook (вызовите этот URL после деплоя)"""
    import asyncio
    
    async def _set():
        await application.bot.set_webhook(WEBHOOK_URL)
    
    asyncio.run(_set())
    return f"Webhook установлен на {WEBHOOK_URL}"

if __name__ == '__main__':
    app_flask.run(host='0.0.0.0', port=8080)
