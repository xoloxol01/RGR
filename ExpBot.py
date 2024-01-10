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

@bot.message_handler(func=lambda message: message.text == "Записаться на консалтинговую услугу")
def request_account_name(message):
    msg = bot.send_message(message.chat.id, "Введите тему и контактные данные:")
    bot.register_next_step_handler(msg, create_account)

def create_account(message):
    account_name = message.text
    user_accounts[message.chat.id].append(account_name)
    user_assets[message.chat.id][account_name] = []
    current_account[message.chat.id] = account_name
    bot.send_message(message.chat.id, f"Запись: '{account_name}' создана.")
    account_menu(message)

@bot.message_handler(func=lambda message: message.text == "Удалить запись")
def delete_account_step(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Да', 'Нет')
    msg = bot.send_message(message.chat.id, "Вы уверены, что хотите удалить запись? (Да/Нет)", reply_markup=markup)
    bot.register_next_step_handler(msg, confirm_delete_account)

def confirm_delete_account(message):
    if message.text.lower() == 'да':
        account_name = current_account[message.chat.id]
        user_accounts[message.chat.id].remove(account_name)
        del user_assets[message.chat.id][account_name]
        bot.send_message(message.chat.id, f"Запись '{account_name}' удалена.")
        main_menu(message)
    elif message.text.lower() == 'нет':
        edit_account(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите 'Да' или 'Нет'.")
        delete_account_step(message)


@bot.message_handler(func=lambda message: message.text == "Просмотреть существующие")
def view_accounts(message):
    if user_accounts[message.chat.id]:
        response = "Ваши записи:\n"
        for account in user_accounts[message.chat.id]:
            response += f"\n{account}:\n"
            for asset in user_assets[message.chat.id][account]:
                response += f"  - {asset['type']}: {asset['name']} (Количество: {asset['quantity']})\n"
        bot.send_message(message.chat.id, response)
    else:
        bot.send_message(message.chat.id, "У вас пока нет записи на консалтинговую услугу (.")
    main_menu(message)

@bot.message_handler(func=lambda message: message.text == "Изменить запись")
def change_account_step(message):
    if user_accounts[message.chat.id]:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for account in user_accounts[message.chat.id]:
            markup.add(account)
        msg = bot.send_message(message.chat.id, "Выберите запись для изменения:", reply_markup=markup)
        bot.register_next_step_handler(msg, edit_account)
    else:
        bot.send_message(message.chat.id, "У вас пока нет записи на консалтинговую услугу. :( ")
        main_menu(message)

def edit_account(message):
    account_name = message.text
    if account_name in user_accounts[message.chat.id]:
        current_account[message.chat.id] = account_name
        bot.send_message(message.chat.id, f"Вы выбрали запись: '{account_name}'. Что вы хотите изменить?", reply_markup=edit_account_markup())
    else:
        bot.send_message(message.chat.id, "Такой записи не существует.")
        main_menu(message)

def edit_account_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Изменить название и контактные данные записи', 'Вернуться в главное меню')
    return markup

@bot.message_handler(func=lambda message: message.text == "Изменить название и контактные данные записи")
def change_account_name_step(message):
    msg = bot.send_message(message.chat.id, "Введите новое название для вашей записи и контактные данные на консалтинговую услугу:")
    bot.register_next_step_handler(msg, change_account_name)

def change_account_name(message):
    new_account_name = message.text
    user_accounts[message.chat.id].remove(current_account[message.chat.id])
    user_accounts[message.chat.id].append(new_account_name)
    user_assets[message.chat.id][new_account_name] = user_assets[message.chat.id].pop(current_account[message.chat.id])
    current_account[message.chat.id] = new_account_name
    bot.send_message(message.chat.id, f"Название записи и контактные данные изменены на '{new_account_name}'.")
    edit_account(message)

# Обработчик для аналитики по дашбордам
@bot.message_handler(func=lambda message: message.text == "Дашборды")
def analytics_dashboard_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add('Линейный график', 'Гистограмма', 'Круговая диаграмма', 'Box-plot', 'Точечный график',
               'Вернуться в главное меню')
    bot.send_message(message.chat.id, "Выберите тип графика для аналитики:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Линейный график")
def line_chart(message):
    with open('C:\\Users\\xolox\\РГРСПС\\Линейный.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == "Гистограмма")
def histogram_chart(message):
    with open("C:\\Users\\xolox\\РГРСПС\\Гистограмма.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == "Круговая диаграмма")
def pie_chart(message):
    with open("C:\\Users\\xolox\\РГРСПС\\Круговая.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == "Box-plot")
def box_plot(message):
    with open("C:\\Users\\xolox\\РГРСПС\\box-plot.png", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == "Точечный график")
def scatter_plot(message):
    with open('C:\\Users\\xolox\\РГРСПС\\Точечный.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

@bot.message_handler(func=lambda message: message.text == "Вернуться в главное меню")
def return_to_main_menu(message):
    main_menu(message)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '<b>мне</b> <u>бы</u> кто помог!', parse_mode='html')

bot.polling(none_stop=True)