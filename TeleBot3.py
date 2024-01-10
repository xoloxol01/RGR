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

# Функция для управления брокерскими счетами
def broker_account_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Создать счет', 'Просмотреть счета', 'Изменить счет', 'Удалить счет', 'Вернуться в главное меню')
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Обработчик для управления брокерскими счетами
@bot.message_handler(func=lambda message: message.text == "Брокерские счета")
def broker_accounts(message):
    broker_account_menu(message)

@bot.message_handler(func=lambda message: message.text == "Создать счет")
def create_broker_account(message):
    msg = bot.send_message(message.chat.id, "Введите название нового брокерского счета:")
    bot.register_next_step_handler(msg, add_broker_account)

def add_broker_account(message):
    account_name = message.text
    user_accounts[message.chat.id].append(account_name)
    user_assets[message.chat.id][account_name] = []
    current_account[message.chat.id] = account_name
    bot.send_message(message.chat.id, f"Брокерский счет '{account_name}' создан.")
    broker_account_menu(message)

# ...

bot.polling(none_stop=True)