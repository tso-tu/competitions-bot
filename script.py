from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler

TOKEN = "8561259371:AAE_0kW6FM5hgpTByn3DwFeQ-KXwySCSrws"
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


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()