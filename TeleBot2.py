import telebot
from telebot import types

bot = telebot.TeleBot('6778234952:AAEA3S8J-k5XU1LIliq-fKrZajQTuSSBAeo')

# Хранилище информации о счетах и активах для каждого пользователя
user_accounts = {}
user_assets = {}
current_account = {}

# Функция для главного меню
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Записаться на консалтинговую услугу', 'Просмотреть существующие', 'Изменить запись', 'Дашборды')  # Добавлена кнопка "Аналитика по Дашбордам"
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Функция для меню управления счетом
def account_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add( 'Удалить запись', 'Вернуться в главное меню')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def welcome(message):
    user_accounts[message.chat.id] = []
    user_assets[message.chat.id] = {}
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}!\n'
                                      'Я - ваш личный бот для записи на консалтинговую услугу. '
                                      'Используйте команды или меню для навигации.')
    main_menu(message)

# ... 

bot.polling(none_stop=True)