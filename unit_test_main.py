import unittest
import sqlite3
from db import user_exists, get_user_id, add_user, add_record, delete_, output
from request_hse import rasp

class BotTest(unittest.TestCase):
    def testIsUserExist(self):
        user_id= "719411857"
        self.assertTrue(user_exists(user_id),"Пользователь не существует")

    def testGetDbUserId1(self):
        user_id= "719411857"
        self.assertEqual(get_user_id(user_id),4, "ID пользователя не найден")

    def testGetDbUserId(self):
        user_id= "719411857"
        self.assertIsInstance(get_user_id(user_id),int, "ID пользователя не найден")

    def testGetTimeTable(self):
        user_id = "Санников Владимир Алексеевич"
        self.assertIsInstance(rasp(user_id),list, "Рассписание для пользователя не найдено")

    def testAddUser(self):
        user_id = "1234567"
        FIO = "Санников Владимир Алексеевич"
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()
        cur = cursor.execute("SELECT * FROM users")
        len_ = len(cur.fetchall())
        self.assertEqual(add_user(user_id, FIO),len_+1, "Пользователь не добавлен")
        cursor.execute("DELETE FROM users WHERE user_id = " + str((user_id)))
        conn.commit()

    def testOutput(self):
        user_id = "1234567"
        FIO = "Санников Владимир Алексеевич"
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `users` (`user_id`, `FIO`) VALUES (?, ?)", (user_id, FIO))
        conn.commit()
        self.assertEqual(output(user_id),FIO, "Пользователь не добавлен")
        cursor.execute("DELETE FROM users WHERE user_id = " + str((user_id)))
        conn.commit()

if __name__ == '__main__':
    unittest.main()