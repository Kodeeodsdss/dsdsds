import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import random

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Список промокодов
codesprivate = ["CODE1", "CODE2", "CODE3", "CODE4", "CODE5"]
used_codes = {}

# Функция для проверки подписки на канал
async def check_subscription(user_id, chat_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking subscription: {e}")
        return False

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Чат", url='https://t.me/your_chat')],
        [InlineKeyboardButton("Канал", url='https://t.me/your_channel')],
        [InlineKeyboardButton("Проверить подписку", callback_data='check_subscription')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Для того, чтобы получить секретный код, вы должны быть подписаны на наши ресурсы.', reply_markup=reply_markup)

# Обработка нажатия кнопки "Проверить подписку"
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    channel_id = '@your_channel'  # Замените на ваш ID или юзернейм канала
    chat_id = '@your_chat'  # Замените на ваш ID или юзернейм чата

    if query.data == 'check_subscription':
        channel_subscribed = await check_subscription(user_id, channel_id, context)
        chat_subscribed = await check_subscription(user_id, chat_id, context)

        if channel_subscribed and chat_subscribed:
            if user_id not in used_codes:
                code = random.choice(codesprivate)
                used_codes[user_id] = code
                codesprivate.remove(code)  # Удаляем код из доступных
                await query.edit_message_text(text=f"Вы подписаны на канал и чат! Ваш код доступа: {code}")
            else:
                await query.edit_message_text(text="Вы уже получили код. Вы можете забрать новый код через 7 дней.")
        else:
            not_subscribed = []
            if not channel_subscribed:
                not_subscribed.append("канал")
            if not chat_subscribed:
                not_subscribed.append("чат")
            await query.edit_message_text(text=f"Вы не подписаны на следующие ресурсы: {', '.join(not_subscribed)}.")

# Запуск бота
def main():
    application = ApplicationBuilder().token("6691638999:AAHHB9EBkN_Zkbz0gpsEICPZz7er-HAAWME").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
