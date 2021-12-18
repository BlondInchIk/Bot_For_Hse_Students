import json

class Shedule:
    '''Данный класс используется для извлечения json-массива состоящего из описаний предметов
    (лекций, семинаров, прак. работ и т.д.)
    '''
    lstr_array = []

    def __init__ (self, string: str):
        '''Конструктор - инициализатор класса выполняющий создание полей и назначающий начальные значения полям класса Shedule'''
        self.lstr_array = json.loads(string)

    def get_lessons(self):
        '''Парсинг строки и получение из него обьектов класса Lesson и дальнейшим выводом их в виде рассписания'''
        result = ""
        lessons_array = [self.lesson_decoder(less) for less in self.lstr_array]
        for lesson in lessons_array:
            result += lesson.to_str()
        return result

    class Lesson(object):
        '''Данный класс используется для хранения и вывода информации об одном предмете'''
        def __init__ (self, kindOfWork, date, discipline, lecturer,auditorium,
            lecturerEmail,
            beginLesson ,
            url1):
            self.kindOfWork = kindOfWork
            self.date = date
            self.discipline = discipline
            self.lecturer = lecturer
            self.auditorium = auditorium
            self.lecturerEmail = lecturerEmail
            self.beginLesson = beginLesson
            self.url1 = url1

        def to_str(self):
            return str(self.date)+" 	     "+str(self.kindOfWork)+"\n"+str(self.discipline)+" - "+str(self.beginLesson)+"\n"+"\n"+"\n"+"Ауд. "+str(self.auditorium)+"\n"+"Преподаватель: "+str(self.lecturer)+"\n"+"\n"+"Сcылка: "+str(self.url1)+"\n\n" +"☝️🧐☝️🧐☝️🧐☝️🧐☝️🧐☝️🧐☝️🧐"+"\n\n"

    def lesson_decoder(self, obj):
        return self.Lesson(obj["kindOfWork"], obj["date"], obj["discipline"], obj["lecturer"],
                        obj["auditorium"], obj["lecturerEmail"],obj["beginLesson"],
                        obj["url1"])

