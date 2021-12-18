import sqlite3
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
'''Данный модуль содержит методы для работы
    с базой данных. Позволяет хранит информацию о пользователях и получать необходимое им рассписание'''

def get_all():
    '''Для получения всех ID в бд'''
    result = cursor.execute("SELECT id FROM `users`")
    return result.fetchall()

def user_exists(user_id):
    '''Для проверки наличия пользователя в бд'''
    result = cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,))
    return bool(len(result.fetchall()))

def get_user_id(user_id):
    '''Для вывода всех данных пользователя'''
    result = cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,))
    return len(result.fetchone())

def add_user(user_id, FIO):
    '''Добавление пользователя в бд'''
    cursor.execute("INSERT INTO `users` (`user_id`, `FIO`) VALUES (?, ?)", (user_id, FIO))
    conn.commit()
    cur = cursor.execute("SELECT * FROM users")
    return len(cur.fetchall())

def add_record(s, ID_):
    '''Добавление рассписание пользователя'''
    for i in s:
        s2 = dict(i)
        para_date = str(s2.get("date"))
        discipline = str(s2.get("discipline"))
        lecturer = str(s2.get("lecturer"))
        auditorium = str(s2.get("auditorium"))
        lecturerEmail = str(s2.get("lecturerEmail"))
        beginlesson = str(s2.get("beginLesson"))
        url1 = str(s2.get("url1"))
        url1_description = str(s2.get("url1_description"))
        para_id = str(s2.get("lessonOid"))
        cursor.execute("SELECT * FROM `records` WHERE `users_id` = ? AND `para_id` = ?", (ID_, para_id))
        cur1 = cursor.fetchall()
        if len(cur1) == 0:
            cursor.execute("INSERT INTO `records` ("
                            "`users_id`, `para_date`, "
                            "`discipline`, `lecturer`, "
                            "`auditorium`, `lecturerEmail`, "
                            "`beginlesson`, `url1`, `url1_description`, "
                            "`para_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (ID_, para_date, discipline, lecturer, auditorium, lecturerEmail, beginlesson, url1, url1_description, para_id))
            conn.commit()

def output(user_id):
    '''Для вывода ФИО по id telegram аккаунта'''
    cursor.execute("SELECT FIO FROM users WHERE user_id = " + str(user_id))
    cur = cursor.fetchall()[0]
    return cur[0]

def delete_(user_id):
    '''Для удаление данных определенного пользователя'''
    cursor.execute("DELETE FROM users WHERE user_id = " + str((user_id)))
    conn.commit()
    cursor.execute("DELETE FROM records WHERE users_id = " + str((user_id)))
    conn.commit()
