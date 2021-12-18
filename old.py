import sqlite3
import requests
import telebot
import time
from datetime import datetime
from telebot import types
import json

name = "Арсений"
surname = "Павленко"

I_WANNA_KNOW_HIM_ID = 0

time_ = datetime.now()
year = time_.year
month = time_.month
day = time_.day

bot=telebot.TeleBot('5097289263:AAHGLV3QXx8CgK6U5JQEIjut7N67NDKCiL4')

def rasp():
    ID = "https://ruz.hse.ru/api/search?term="
    ID += surname + " " + name
    print(ID)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.50"}

    full_page = requests.post(ID, headers=headers)
    full_page_str = str(full_page.content, 'utf8')

    s1 = json.loads(full_page_str)
    if s1 == []:
        return "Пользователь не найден!"
    cur_id = ""
    for i in s1:
        s2 = dict(i)
        if s2.get("id") != "":
            cur_id = s2.get("id")
        break
    raspisanie = "https://ruz.hse.ru/api/schedule/student/" + str(cur_id) + "?start=" + str(year) + "." + str(month) + "." + str(day) + "&finish=" + str(year) + "." + str(month) + "." + str(day+7)
    print(raspisanie)
    full_page = requests.post(raspisanie, headers=headers)
    full_page_str = str(full_page.content, 'utf8')
    s2 = json.loads(full_page_str)
    if s2 == []:
        return "Пользователь не найден!"
    return s2

conn = sqlite3.connect('users.db', check_same_thread=False)

cur = conn.cursor()
#Создание таблицы users
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INT PRIMARY KEY,
   date_id TEXT,
   surname_id TEXT,
   name_id TEXT);
""")
conn.commit()

#Создание таблицы raspisanie
cur.execute("""CREATE TABLE IF NOT EXISTS raspisanie(
        id__ TEXT,
        date_ TEXT,
        discipline TEXT,
        lecturer TEXT,
        auditorium TEXT,
        lecturerEmail TEXT,
        beginLesson TEXT,
        url1 TEXT,
        url1_description TEXT,
        url2 TEXT,
        url2_description TEXT,
        check_ TEXT);
""")
conn.commit()

def db_add(s):
    count = 0
    print(s)
    # cur.execute("SELECT `user_id` FROM raspisanie WHERE `check_` = ?", (check__,))
    # cur.execute("INSERT INTO raspisanie VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", user)
    for i in s:
        s2 = dict(i)
        count += 1
        date__ = str(s2.get("date"))
        discipline_ = str(s2.get("discipline"))
        lecturer_ = str(s2.get("lecturer"))
        auditorium_ = str(s2.get("auditorium"))
        lecturerEmail_ = str(s2.get("lecturerEmail"))
        beginLesson_ = str(s2.get("beginLesson"))
        url1_ = str(s2.get("url1"))
        url1_description_ = str(s2.get("url1_description"))
        url2_ = str(s2.get("url2"))
        url2_description_ = str(s2.get("url2_description"))
        check__ = str(s2.get("lessonOid"))
        print(s2.get('date'))
        # cur.execute("SELECT `id__` FROM raspisanie WHERE `check_` = ?", (check__,))
        # cur1 = cur.fetchall()
        cur.execute("SELECT * FROM raspisanie WHERE `id__` = ?", (id_,))
        cur1 = cur.fetchall()
        cur.execute("SELECT `id__` FROM raspisanie WHERE `check_` = ?", (check__,))
        cur2 = cur.fetchall()
        if len(cur1) == 0:
            user = (id_, date__, discipline_, lecturer_, auditorium_, lecturerEmail_, beginLesson_, url1_, url1_description_, url2_, url2_description_, check__)
            cur.execute("INSERT INTO raspisanie VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", user)
            conn.commit()
        else:
            cur.execute("SELECT `id__` FROM raspisanie WHERE `check_` = ?", (check__,))
            cur2 = cur.fetchall()
            user = (id_, date__, discipline_, lecturer_, auditorium_, lecturerEmail_, beginLesson_, url1_, url1_description_, url2_, url2_description_, check__)
            cur.execute("INSERT INTO raspisanie VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", user)
            conn.commit()

id1 = 719411857
db_add(rasp(), id1)

def add_(id):
    cur = rasp()
    if type(cur) != str:
        db_add(cur, id)
    else:
        bot.send_message(id, "Пользователь не найден:(")
def not_():
    pass
def delete_():
    pass
#
# markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

@bot.message_handler(commands=['start'])
def start_message(message):
    global I_WANNA_KNOW_HIM_ID
    I_WANNA_KNOW_HIM_ID = message.chat.id
    # bot.send_message(message.chat.id,'Привет, друг...')
    # time.sleep(1)
    # bot.send_message(message.chat.id,'Привет,...друг?')
    # time.sleep(1)
    # bot.send_message(message.chat.id,'Чушь какая... Возможно, стоит дать тебе имя? Но это скользкая дорожка. Ты только у меня в голове - не стоит это забывать.')
    # time.sleep(3)
    # bot.send_message(message.chat.id,'Чёрт! Я и правда говорю с воображаемым человеком...')
    # time.sleep(1)
    # bot.send_message(message.chat.id,'То, что я расскажу - совершенно секретно. Существует заговор против всех нас. Могущественная группа людей тайно управляет всей Высшей Школой Экономики.')
    # time.sleep(4)
    bot.send_message(message.chat.id,"""Мои функции:
Добавить пользователя - /add
Узнать об изменении в рассписании - /up
Удалить пользователя - /delete""")
    # time.sleep(60)
    # bot.send_photo(message.chat.id, 'https://i.pinimg.com/originals/ee/91/bc/ee91bcd451ce911d6ad5b167b6b7abb1.jpg');

@bot.message_handler(content_types='text')
def commands(message):
    if message.text == "/add" or message.text == "add":
        get_name1(message)
    if message.text == "/up" or message.text == "up":
        pass
    if message.text == "/delete" or message.text == "delete":
        pass
def get_name1(message):
    bot.send_message(message.from_user.id, "Введите своё имя:")
    bot.register_next_step_handler(message, get_name)
def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Введите свою фамилию:")
    bot.register_next_step_handler(message, get_surname)
def get_surname(message):
    global surname
    surname = message.text
    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='ДА', callback_data='yes')
    key_no= types.InlineKeyboardButton(text='НЕТ', callback_data='no')
    keyboard.add(key_yes, key_no)
    bot.send_message(message.chat.id,f"Твоя фамилия - {surname} и имя - {name}?", reply_markup=keyboard)

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
        bot.register_next_step_handler(call.message, get_name)

# bot.send_photo(928814645, 'https://i.pinimg.com/originals/ee/91/bc/ee91bcd451ce911d6ad5b167b6b7abb1.jpg');
def parsing():
    pass

bot.infinity_polling()

# bot.send_message(message.chat.id,'Не бойся. Я помогу тебе выжить, играя по их правилам...')
# keyboard = types.InlineKeyboardMarkup();
# key_yes = types.InlineKeyboardButton(text='/ADD', callback_data='add');
# key_no= types.InlineKeyboardButton(text='/NOT', callback_data='not');
# keyboard.add(key_yes, key_no);
# key_fist= types.InlineKeyboardButton(text='/DELETE', callback_data='delete');
# keyboard.add(key_fist);
# bot.send_message(message.chat.id,"Как тебе помочь /start?", reply_markup=keyboard)
