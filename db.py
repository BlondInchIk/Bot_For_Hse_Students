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

def add_user(user_id):
    """Добавляем юзера в базу"""
    cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
    return conn.commit()

def add_record(user_id, operation, value):
    """Создаем запись о доходах/расходах"""
    cursor.execute("INSERT INTO `records` ("
                        "`users_id`, `para_date`, "
                        "`discipline`, `lecturer`, "
                        "`auditorium`, `lectureremail`, "
                        "`beginlesson`, `url1`, `url1_description`, "
                        "`para_id`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,)",
                        (get_user_id(user_id),
                        operation == "+",
                        value))
    return conn.commit()

def close():
    """Закрываем соединение с БД"""
    connection.close()