import unittest
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
if __name__ == '__main__':
    unittest.main()