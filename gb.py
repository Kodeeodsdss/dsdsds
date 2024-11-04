import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Функция для обработки команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет! Я бот, который отвечает на команду /start.')

# Запуск бота
def main():
    application = ApplicationBuilder().token("6691638999:AAHHB9EBkN_Zkbz0gpsEICPZz7er-HAAWME").build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling()

if __name__ == '__main__':
    main()
