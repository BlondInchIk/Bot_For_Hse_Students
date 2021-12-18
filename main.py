import telebot
from db import user_exists, get_user_id, add_user, add_record
import time
from mg import get_map_cell

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

# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#     if call.data == "add":
#         pass
#     elif call.data == "not":
#         pass
#     elif call.data == "delete":
#         pass
#     elif call.data == "yes":
#         add_(call.message.chat.id)
#     elif call.data == "no":
#         bot.send_message(call.message.chat.id, "Введите свое имя ещё раз:")
#         bot.register_next_step_handler(call.message, FIO_)

cols, rows = 8, 8

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
              telebot.types.InlineKeyboardButton('↑', callback_data='up'),
              telebot.types.InlineKeyboardButton('↓', callback_data='down'),
              telebot.types.InlineKeyboardButton('→', callback_data='right') )

maps = {}

def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🔴"
            else:
                map_str += "⬜"
        map_str += "\n"

    return map_str

@bot.message_handler(commands=['play'])
def play_message(message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    maps[message.chat.id] = user_data

    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    user_data = maps[query.message.chat.id]
    new_x, new_y = user_data['x'], user_data['y']

    if query.data == 'left':
        new_x -= 1
    if query.data == 'right':
        new_x += 1
    if query.data == 'up':
        new_y -= 1
    if query.data == 'down':
        new_y += 1

    if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
        return None
    if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
        return None

    user_data['x'], user_data['y'] = new_x, new_y

    if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
        bot.edit_message_text( chat_id=query.message.chat.id,
                               message_id=query.message.id,
                               text="Вы выиграли" )
        return None

    bot.edit_message_text( chat_id=query.message.chat.id,
                           message_id=query.message.id,
                           text=get_map_str(user_data['map'], (new_x, new_y)),
                           reply_markup=keyboard )
bot.infinity_polling()