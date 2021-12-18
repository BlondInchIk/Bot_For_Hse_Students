import unittest.mock
import sqlite3
from db import user_exists, get_user_id, add_user, output
from request_hse import rasp,rasp_cool
from anekdots import Anecdots

'''Данный модуль отвечает за тестирование разрабатываемого приложения'''
class BotTest(unittest.TestCase):
    '''Данный класс реализует проверку функционнальности бота и его составляющих'''
    def testIsUserExist(self):
        '''Данная функция проверяет наличие пользователя в Базе данных'''
        user_id= "719411857"
        self.assertTrue(user_exists(user_id),"Пользователь не существует")

    def testGetDbUserId1(self):
        '''Данная функция проверяет регистрационный номер пользователя в Базе данных'''
        user_id= "719411857"
        self.assertEqual(get_user_id(user_id),4, "ID пользователя не найден")

    def testGetDbUserId(self):
        '''Функция реализует отслеживание выходного типа данных при запросе получения id пользователя БОТА(проверка на None)'''
        user_id= "719411857"
        self.assertIsInstance(get_user_id(user_id),int, "ID пользователя не найден")

    def testGetTimeTable(self):
        '''Функция реализует отслеживание выходного типа данных при запросе получения расписания пользователя БОТА(проверка на None)'''
        user_id = "Санников Владимир Алексеевич"
        self.assertIsInstance(rasp(user_id),list, "Рассписание для пользователя не найдено")

    def testGetCoolTimeTable(self):
        '''Функция отслеживает последовательную обработку json строки с дальнейшей проверкой выходного типа'''
        user_id = "Санников Владимир Алексеевич"
        self.assertIsInstance(rasp_cool(user_id), str, "Рассписание для пользователя не найдено")

    def testAddUser(self):
        '''Реализует проверку операции добавления пользоввателя в Базу данных'''
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
        '''Тестирование функции putput бота'''
        user_id = "1234567"
        FIO = "Санников Владимир Алексеевич"
        conn = sqlite3.connect('users.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `users` (`user_id`, `FIO`) VALUES (?, ?)", (user_id, FIO))
        conn.commit()
        self.assertEqual(output(user_id),FIO, "Пользователь не добавлен")
        cursor.execute("DELETE FROM users WHERE user_id = " + str((user_id)))
        conn.commit()

    def testJoke(self):
        '''Функция проверяет доступность хранимой информации в файле json'''
        anect=Anecdots()
        self.assertEqual(anect.texts[0],"Если бы программисты были врачами, им бы говорили «У меня болит нога», а они отвечали «Ну не знаю, у меня такая же нога, а ничего не болит».",
                         "Неправильно подобран анекдот")


if __name__ == '__main__':
    '''Функция запуска тестирования'''
    unittest.main()