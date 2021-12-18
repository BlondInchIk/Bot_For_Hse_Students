import json
import random
class Anecdots:
    '''Данный класс хранит в себе анекдоты'''
    texts=[]
    def __init__(self):
        '''Функция init позволяет получить тексты из json файла'''
        string = json.loads(open("anecdots.json").read())
        self.texts=string["anecdots"]
    def get_anecdot(self):
        '''Возвращает случайный анекдот из предложенных'''
        return self.texts[random.randrange(0,5)]