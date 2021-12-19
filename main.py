import telebot
from telebot import types
from db import user_exists, get_user_id, add_user, add_record, delete_, output, get_all
import time
from anekdots import Anecdots
from mg import get_map_cell
from request_hse import rasp, rasp_cool
from telebot import types
from database import Database

bot=telebot.TeleBot('5097289263:AAHGLV3QXx8CgK6U5JQEIjut7N67NDKCiL4')
db = Database('db.db')
FIO = ''

'''Данный модуль реализует основную функционнальность бота и пользовательского интерфейса в нём'''
@bot.message_handler(commands = ["start"])
def start(message):
    '''Используется для начала работы telegram bot'a и запуска вступительного текста'''
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("/add","/delete")
    user_markup.row("/play","/show")
    user_markup.row("/chat","/location")
    user_markup.row("/joke")
    bot.send_message(message.from_user.id,'Привет, друг...')
    time.sleep(1)
    bot.send_message(message.from_user.id,'Привет,...друг?')
    time.sleep(1)
    bot.send_message(message.from_user.id,'Чушь какая... Возможно, стоит дать тебе имя? Но это скользкая дорожка. Ты только у меня в голове - не стоит это забывать.')
    time.sleep(3)
    bot.send_message(message.from_user.id,'Чёрт! Я и правда говорю с воображаемым человеком...')
    time.sleep(1)
    bot.send_message(message.from_user.id,'То, что я расскажу - совершенно секретно. Существует заговор против всех нас. Могущественная группа людей тайно управляет всей Высшей Школой Экономики.')
    time.sleep(4)
    bot.send_message(message.from_user.id,"Я помогу тебе в это нелегкое время \n\n Команды для управления моей силой: \n\n/add - вступить в мой клан\n/delete - дезертировать как трус -_-\n"
                                          "/play - правильное времяпрепровождение на парах по АиП\n/show - рассписание твоих будущих испытаний\n/chat - сходка анонимных алкоголиков"
                                          "\n/location - координаты домов\n/joke - если тебе грустно, тебе всегда помогут наши околоинтеллектуальные шутки", reply_markup = user_markup)

@bot.message_handler(commands = ["delete"])
def delete(message):
    '''Используется для удаления информации о пользователе из бд'''
    bot.send_message(message.from_user.id, "Вы точно хотите удалить себя из базы данных?")
    bot.register_next_step_handler(message, delete2)
def delete2(message):
    '''Используется для подтверждения удаления информации о пользователе из бд'''
    if message.text == "Да" or message.text == "да":
        delete_(message.chat.id)
    if message.text == "Нет" or message.text == "нет":
        bot.send_message(message.from_user.id, "Операция отменена:(")

@bot.message_handler(commands = ["show"])
def output_(message):
    '''Реализует вывод рассписания определенного пользователя'''
    bot.send_message(message.from_user.id, rasp_cool(output(message.from_user.id)))

@bot.message_handler(commands = ["joke"])
def get_joke(message):
    '''Предлагает пользователю случайный анекдот'''
    anect = Anecdots()
    bot.send_message(message.from_user.id, anect.get_anecdot())

@bot.message_handler(commands = ["location"])
def output_(message):
    '''Отправляет гео-метку по заданному местоположению'''
    bot.send_photo(message.from_user.id, "https://cim.hse.ru/data/2017/04/07/1168289132/map-web-01.png")
    bot.send_message(message.from_user.id, "Доступные здания вышки в этом боте:\n"
                                           "Мием, Шаболовка, Покровка, Мясницкая, Басманная, Ордынка,"
                                           " Одинцово, Дубки")

@bot.message_handler(commands=['play'])
def play_message(message):
    '''Запускает игру - лабиринт'''
    bot.send_message(message.from_user.id, "Таааак... Кто-то отважился бросить вызов моему великому лабиринту☠")
    time.sleep(2)
    bot.send_message(message.from_user.id,"Если пройдешь до противоположного по диагонали угла тебя ждет награда")
    map_cell = get_map_cell(cols, rows)
    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }
    maps[message.chat.id] = user_data
    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)

@bot.message_handler(commands = ["add"])
def start(message):
    '''Запрашивает ФИО для добваления нформации в бд'''
    if (not user_exists(message.from_user.id)):
        bot.send_message(message.from_user.id, "Введите своё ФИО:")
        bot.register_next_step_handler(message, FIO_)
    else:
        bot.send_message(message.from_user.id,"Пользователь уже есть в базе данных")

def FIO_(message):
    '''Данная функция является промежуточной и необходима для леквидации бессконечного цикла'''
    global FIO
    FIO = message.text
    FIO_test(message)

def FIO_test(message):
    '''Данная функция является промежуточной и необходима для леквидации бессконечного цикла'''
    bot.send_message(message.chat.id,f"Твое ФИО - {FIO}?")
    bot.register_next_step_handler(message, FIO_test2)

def FIO_test2(message):
    '''Запрашивает подтверждение от пользователя для внесения ФИО в бд'''
    if message.text == "Да" or message.text == "да":
        bot.send_message(message.chat.id, "Отлично!")
        add_(message.chat.id)
    else:
        if message.text == "Нет" or message.text == "нет":
            bot.send_message(message.chat.id, "Введите свое ФИО ещё раз:")
            bot.register_next_step_handler(message, FIO_)
        else:
            bot.send_message(query.message.chat.id, "Чтобы согласиться с данными отправьте да, или нет если допущена ошибка в вводе")
            FIO_test2(message)

def add_(message):
    '''Вносит информацию о пользователе в бд'''
    add_user(message, FIO)
    add_record(rasp(FIO), message)

cols, rows = 8, 8
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row( telebot.types.InlineKeyboardButton('←', callback_data='left'),
              telebot.types.InlineKeyboardButton('↑', callback_data='up'),
              telebot.types.InlineKeyboardButton('↓', callback_data='down'),
              telebot.types.InlineKeyboardButton('→', callback_data='right') )
keyboard.row(telebot.types.InlineKeyboardButton("Сдаться", callback_data='exit'))
maps = {}

def get_map_str(map_cell, player):
    '''Создает поле(лабиринта'''
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

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    '''Реализует пользовательский интерфейс игры лабиринт'''
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
                               text="Сongratulations\n+15 Social credit" )
        bot.send_animation(query.message.chat.id, "https://c.tenor.com/RvBPEdvCqHkAAAAC/social-credit.gif")
        return None
    bot.edit_message_text( chat_id=query.message.chat.id,
                           message_id=query.message.id,
                           text=get_map_str(user_data['map'], (new_x, new_y)),
                           reply_markup=keyboard )

@bot.message_handler(commands = ['chat'])
def start(message):
    '''Запуск анонимного чата'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Поиск')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Нажми на поиск собеседника. '.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    '''Остановка анонимного чата'''
    chat_info = db.get_active(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('Поиск')
        markup.add(item1)

        bot.send_message(chat_info[1], 'Теперь вы наидене с вашими мыслями'.format(message.from_user), reply_markup = markup)
        bot.send_message(message.chat.id, 'Вы вышли из чата'.format(message.from_user), reply_markup = markup)
    else:
        bot.send_message(message.chat.id, 'Вы не начали чат'.format(message.from_user), reply_markup = markup)

@bot.message_handler(content_types = ['text'])
def bot_message(message):
    '''Запуск поиска собеседника для анонимного чата'''
    if message.chat.type == 'private':
        if message.text == "Поиск":
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton("Stop")
            markup.add(item1)

            chat_two = db.get_chat()

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, "Поиск", reply_markup = markup)
            else:
                mess = 'Собеседник найден! Чтобы выйти, напишите /stop'
                markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = types.KeyboardButton("Stop")
                markup.add(item1)

                bot.send_message(message.chat.id, mess, reply_markup = markup)
                bot.send_message(chat_two, mess, reply_markup = markup)

        elif message.text == "Stop":
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, "Поиск остановлен")

    if message.text=="МИЕМ" or message.text=="Мием" or message.text=="мием" or message.text=="МЕМ":
        bot.send_location(message.from_user.id, 55.803337, 37.410132)
    if message.text == "Шаболовка" or message.text == "шаболовка":
        bot.send_location(message.from_user.id, 55.720197, 37.608582)
    if message.text == "Покровка" or message.text == "покровка" or message.text == "покровская":
        bot.send_location(message.from_user.id, 55.754007, 37.648283)
    if message.text == "Мясницкая" or message.text == "мясницкая":
        bot.send_location(message.from_user.id, 55.761456, 37.633133)
    if message.text == "Басманная" or message.text == "басманная" or message.text == "Басманая" or message.text == "Басманая":
        bot.send_location(message.from_user.id, 55.766844, 37.663422)
    if message.text == "Ордынка" or message.text == "ордынка":
        bot.send_location(message.from_user.id, 55.737520, 37.626289)
    if message.text == "Одинцово" or message.text == "одинцово":
        bot.send_location(message.from_user.id, 55.669965, 37.279713)
    if message.text == "Дубки" or message.text == "дубки":
        bot.send_location(message.from_user.id, 55.660415, 37.228285)

bot.infinity_polling()