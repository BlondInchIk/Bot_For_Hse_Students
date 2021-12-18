import sqlite3

conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()

def user_exists(user_id):
    """Проверяем, есть ли юзер в базе"""
    result = cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
    return bool(len(result.fetchall()))

def get_user_id(user_id):
    """Достаем id юзера в базе по его user_id"""
    result = cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
    return result.fetchone()[0]

def add_user(user_id, FIO):
    """Добавляем юзера в базу"""
    cursor.execute("INSERT INTO `users` (`user_id`, `FIO`) VALUES (?, ?)", (user_id, FIO))
    return conn.commit()

def add_record(s, ID_):
    """Создаем запись о доходах/расходах"""
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
        cursor.execute("INSERT INTO `records` ("
                        "`users_id`, `para_date`, "
                        "`discipline`, `lecturer`, "
                        "`auditorium`, `lecturerEmail`, "
                        "`beginlesson`, `url1`, `url1_description`, "
                        "`para_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (ID_, para_date, discipline, lecturer, auditorium, lecturerEmail, beginlesson, url1, url1_description, para_id))
        conn.commit()

def close():
    """Закрываем соединение с БД"""
    connection.close()