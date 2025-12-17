import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
from flask import Flask
from threading import Thread

app_flask = Flask(__name__)

TOKEN = os.environ.get('TOKEN')
WEB_APP_URL = "https://tso-tu.github.io/competitions-miniapp/"

async def start(update: Update, context):
    bot_username = context.bot.username

    # Кнопка с deep link
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

    ✨ <b>Все функции доступны в нашем мини-приложении!</b>"""

    await update.message.reply_text(
        message_text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML"
    )

def run_bot():
    """Функция для запуска бота в отдельном потоке"""
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

@app_flask.route('/')
def home():
    return "Telegram Bot is running!"

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # Запускаем Flask-сервер
    app_flask.run(host='0.0.0.0', port=8080)



