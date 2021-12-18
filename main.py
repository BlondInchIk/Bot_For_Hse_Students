import telebot
from db import user_exists, get_user_id, add_user, add_record
import time

bot=telebot.TeleBot('5097289263:AAHGLV3QXx8CgK6U5JQEIjut7N67NDKCiL4')
FIO = ''


@bot.message_handler(commands = ["start"])
def start(message):
    if(not user_exists(message.chat.id)):
        add_user(message.chat.id)
    bot.send_message(message.chat.id,'Привет, друг...')
    time.sleep(1)
    bot.send_message(message.chat.id,'Привет,...друг?')
    time.sleep(1)
    bot.send_message(message.chat.id,'Чушь какая... Возможно, стоит дать тебе имя? Но это скользкая дорожка. Ты только у меня в голове - не стоит это забывать.')
    time.sleep(3)
    bot.send_message(message.chat.id,'Чёрт! Я и правда говорю с воображаемым человеком...')
    time.sleep(1)
    bot.send_message(message.chat.id,'То, что я расскажу - совершенно секретно. Существует заговор против всех нас. Могущественная группа людей тайно управляет всей Высшей Школой Экономики.')
    time.sleep(4)

@bot.message_handler(commands = ["add"])
def start(message):
    bot.send_message(message.from_user.id, "Введите своё имя:")
    bot.register_next_step_handler(message, FIO_)
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id, cur)
    else:
        bot.send_message(message.from_user.id,"Пользователь уже есть в базе данных")
    # BotDB.add_record(message.from_user.id, operation, value)

def FIO_(message):
    global FIO
    FIO = message.text
    FIO_test(FIO)

def FIO_test(message):
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    key_no= types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    keyboard.add(key_yes, key_no)
    bot.send_message(message.chat.id,f"Твое ФИО - {FIO}?", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "add":
        pass
    elif call.data == "not":
        pass
    elif call.data == "delete":
        pass
    elif call.data == "yes":
        add_(call.message.chat.id)
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Введите свое имя ещё раз:")
        bot.register_next_step_handler(call.message, FIO_)
bot.infinity_polling()