import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio

# === 1. Настройка логирования ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# === 2. Инициализация Flask ===
app = Flask(__name__)

# === 3. Инициализация Telegram бота ===
TOKEN = os.environ.get('TOKEN')
if not TOKEN:
    logger.error("❌ КРИТИЧЕСКАЯ ОШИБКА: Переменная 'TOKEN' не найдена!")
    
bot_app = Application.builder().token(TOKEN).build()

# === 4. Ваша команда /start ===
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_username = context.bot.username
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    
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

# Регистрируем команду
bot_app.add_handler(CommandHandler("start", start_command))

# === 5. Webhook обработчик (для получения сообщений) ===
@app.route('/webhook', methods=['POST'])
def webhook():
    """Получаем обновления от Telegram"""
    try:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        asyncio.run(bot_app.process_update(update))
        return 'ok'
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return 'error', 500

# === 6. Установка webhook (ВЫПОЛНИТЕ ОДИН РАЗ ПОСЛЕ ДЕПЛОЯ) ===
@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установите webhook - откройте этот URL в браузере после деплоя"""
    try:
        # Получаем URL сервиса
        render_url = os.environ.get('RENDER_EXTERNAL_URL', 'https://competitions-bot-ezdu.onrender.com')
        webhook_url = f"{render_url}/webhook"
        
        # Устанавливаем webhook
        asyncio.run(bot_app.bot.set_webhook(webhook_url))
        
        logger.info(f"✅ Webhook установлен на {webhook_url}")
        return f"""
        <h1>✅ Webhook установлен!</h1>
        <p>Webhook URL: {webhook_url}</p>
        <p>Теперь бот будет получать сообщения.</p>
        <p>Проверьте бота командой /start в Telegram.</p>
        """
    except Exception as e:
        logger.error(f"❌ Ошибка установки webhook: {e}")
        return f"❌ Ошибка: {e}"

# === 7. Стартовая страница и health check ===
@app.route('/')
def home():
    return "✅ Telegram Bot is running!<br>После деплоя откройте: /set_webhook"

@app.route('/health')
def health():
    return 'OK', 200

# === 8. Запуск ===
if __name__ == '__main__':
    logger.info("🚀 Запускаю сервер...")
    app.run(host='0.0.0.0', port=8080, debug=False)
