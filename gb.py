import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import time
from datetime import datetime, timedelta

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Приватные коды
codes_private = ['CODE1', 'CODE2', 'CODE3']  # Добавьте свои коды сюда
used_codes = []  # Список использованных кодов

# Идентификаторы канала и чата
CHAT_ID = '@kazinochatfree'  # Замените на ваш ID чата
CHANNEL_ID = '@GamblingSNG'  # Замените на ваш ID канала

# Функция для старта
def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Чат", url='https://t.me/joinchat/your_chat_link')],
        [InlineKeyboardButton("Канал", url='https://t.me/your_channel_link')],
        [InlineKeyboardButton("Проверить подписку", callback_data='check_subscription')]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Добро пожаловать! Для того, чтобы получить секретный код, вы должны быть подписаны на наши ресурсы.',
        reply_markup=reply_markup
    )


# Функция для проверки подписки
def check_subscription(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user_id = query.from_user.id

    if check_user_subscription(user_id):
        code = get_unique_code()
        if code:
            context.user_data['last_code_time'] = datetime.now()
            query.edit_message_text(text=f'Вы подписаны на наши ресурсы! Ваш код доступа: {code}')
        else:
            query.edit_message_text(text='Все коды были использованы.')
    else:
        query.edit_message_text(text='Вы не подписаны на наши ресурсы. Пожалуйста, подпишитесь и проверьте еще раз.')

    # Создание кнопки для получения кода
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Забрать код", callback_data='get_code')]])
    query.message.reply_text(text='Нажмите кнопку ниже, чтобы забрать приватный код, если вы уже получали его.', reply_markup=reply_markup)


# Функция для проверки подписки пользователя
def check_user_subscription(user_id):
    try:
        # Проверка подписки на канал
        channel_member = context.bot.get_chat_member(CHANNEL_ID, user_id)
        if channel_member.status not in ['member', 'administrator', 'creator']:
            return False
        
        # Проверка подписки на чат
        chat_member = context.bot.get_chat_member(CHAT_ID, user_id)
        if chat_member.status not in ['member', 'administrator', 'creator']:
            return False
        
        return True
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        return False  # Если произошло исключение, считаем, что пользователь не подписан


# Функция для получения уникального кода
def get_unique_code():
    global used_codes
    available_codes = [code for code in codes_private if code not in used_codes]
    if available_codes:
        code = available_codes[0]  # Получить код
        used_codes.append(code)  # Добавить код в использованные
        return code
    return None


# Функция для обработки нажатия на кнопку "Забрать приватный код"
def get_code(update: Update, context: CallbackContext):
    now = datetime.now()
    last_code_time = context.user_data.get('last_code_time', None)

    if last_code_time:
        if now < last_code_time + timedelta(days=7):
            update.callback_query.answer('Вы можете забирать код только раз в 7 дней.')
            return

    # Выдача нового кода
    if check_user_subscription(update.callback_query.from_user.id):
        code = get_unique_code()
        if code:
            context.user_data['last_code_time'] = now
            update.callback_query.edit_message_text(text=f'Ваш новый код доступа: {code}')
        else:
            update.callback_query.edit_message_text(text='Все коды были использованы.')
    else:
        update.callback_query.edit_message_text(text='Вы не подписаны на наши ресурсы. Пожалуйста, подпишитесь и проверьте еще раз.')


# Основная функция для запуска бота
def main():
    # Замените TOKEN на ваш токен бота
    updater = Updater("6691638999:AAHHB9EBkN_Zkbz0gpsEICPZz7er-HAAWME")

    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher

    # Обработчик команд
    dispatcher.add_handler(CommandHandler('start', start))
    
    # Обработчики нажатий кнопок
    dispatcher.add_handler(CallbackQueryHandler(check_subscription, pattern='check_subscription'))
    dispatcher.add_handler(CallbackQueryHandler(get_code, pattern='get_code'))

    # Запуск бота
    updater.start_polling()
    
    # Работаем до остановки
    updater.idle()


if __name__ == '__main__':
    main()
