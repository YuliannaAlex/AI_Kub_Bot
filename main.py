import os
from dotenv import load_dotenv
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes
)

load_dotenv()  # Загружает .env файл

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
CHOOSING = 1

# Данные о языках программирования
language_data = {
    "JavaScript": {
        "Сфера применения": "Веб-разработка (фронтенд и бэкенд), мобильные приложения (React Native), десктопные приложения (Electron)",
        "Использование в нейросетях": "~15% (используется в веб-интерфейсах для нейросетей)",
        "Порог входа": "Низкий для базового уровня",
        "План самообразования": "1. Основы JS\n2. ES6+\n3. Node.js\n4. Фреймворки (React, Vue)"
    },
    "Python": {
        "Сфера применения": "Веб-разработка, Data Science, AI/ML, автоматизация",
        "Использование в нейросетях": "~60% (основной язык для машинного обучения)",
        "Порог входа": "Очень низкий",
        "План самообразования": "1. Основы Python\n2. ООП\n3. Библиотеки (NumPy, Pandas)\n4. Фреймворки (Django, Flask)"
    },
    "Java": {
        "Сфера применения": "Корпоративные приложения, Android-разработка",
        "Использование в нейросетях": "~10%",
        "Порог входа": "Средний",
        "План самообразования": "1. Основы Java\n2. ООП\n3. Spring Framework\n4. Базы данных"
    },
    "C#": {
        "Сфера применения": "Десктопные приложения, игры (Unity), веб (ASP.NET)",
        "Использование в нейросетях": "~8%",
        "Порог входа": "Средний",
        "План самообразования": "1. Основы C#\n2. .NET\n3. ООП\n4. ASP.NET"
    },
    "C++": {
        "Сфера применения": "Высокопроизводительные системы, игры, embedded-системы",
        "Использование в нейросетях": "~7%",
        "Порог входа": "Высокий",
        "План самообразования": "1. Основы C++\n2. STL\n3. ООП\n4. Многопоточность"
    }
}

# Клавиатура с языками
def get_language_keyboard():
    return ReplyKeyboardMarkup(
        [["JavaScript", "Python"], ["Java", "C#", "C++"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def start(update, context):
    """Обработчик команды /start"""
    await update.message.reply_text(
        "Привет! Я бот, который расскажет тебе о языках программирования. "
        "Выбери язык из списка ниже:",
        reply_markup=get_language_keyboard()
    )
    return CHOOSING

async def show_language_info(update, context):
    """Показывает информацию о выбранном языке и снова предлагает выбор"""
    language = update.message.text
    info = language_data.get(language)
    
    if info:
        response = f"<b>{language}</b>\n\n"
        for key, value in info.items():
            response += f"<u>{key}</u>: {value}\n\n"
        
        # Отправляем информацию и снова показываем кнопки
        await update.message.reply_text(
            response,
            parse_mode="HTML",
            reply_markup=get_language_keyboard()
        )
    else:
        await update.message.reply_text(
            "Я не знаю такого языка. Пожалуйста, выбери из предложенных.",
            reply_markup=get_language_keyboard()
        )
    
    return CHOOSING

async def cancel(update, context):
    """Завершает диалог"""
    await update.message.reply_text(
        "Если захочешь узнать о языках снова - напиши /start",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """Запуск бота"""
    application = Application.builder().token("7957702217:AAGuE9JE3CAOI22sHpWXar-7zEjoWx5SxZw").build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    filters.Regex('^(JavaScript|Python|Java|C#|C\+\+)$'),
                    show_language_info
                )
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
