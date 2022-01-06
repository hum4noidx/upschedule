import datetime

from django.contrib import admin
from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Passport(models.Model):
    user_id = models.IntegerField()
    uses = models.IntegerField()
    user_class = models.IntegerField()
    user_prof = models.CharField(max_length=10)
    user_math = models.CharField(max_length=10)
    vip = models.BooleanField()
    admin = models.BooleanField()


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.lesson_name


class Lecturer(models.Model):
    name = models.CharField('ФИО', max_length=200)
    specialization = models.CharField('Специальность', max_length=200)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Timetable(models.Model):
    lesson_numbers = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
    )
    lesson_grades = (
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
    )
    lesson_profiles = (
        ('fm', 'Физмат'),
        ('gum', 'Гуманитарий'),
        ('se', 'Соцэконом'),
        ('bh', 'Биохим'),
        ('med', 'Медицинский'),
        ('media', 'Медиа'),
        ('akadem', 'Академический'),
        ('it', 'It/Инженеры')
    )
    lesson_dates = (
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
    )
    lesson_maths = (
        ('prof', 'Профильная'),
        ('base', 'Базовая'),
        ('None', 'Нет математики')
    )

    lesson_number = models.IntegerField(choices=lesson_numbers)
    lesson_text = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    classroom = models.CharField('Кабинет', max_length=15)
    teacher = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
    lesson_date = models.IntegerField('День недели', choices=lesson_dates)
    lesson_grade = models.IntegerField('Класс', choices=lesson_grades)
    lesson_profile = models.CharField('Профиль', choices=lesson_profiles, max_length=200)
    lesson_math = models.CharField('Математика', choices=lesson_maths, max_length=15)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return f'\nУрок - {self.lesson_text} Класс - {self.classroom}'

# class User(models.Model):
#     telegram_id = models.CharField(max_length=20)
#     twitch_id = models.CharField(max_length=20)
#     twitch_bearer = models.CharField(max_length=30)
#     twitch_refresh_token = models.CharField(max_length=50)
#     created = models.DateTimeField(auto_now_add=True)
#
#     def str(self):
#         return f'USER {self.twitch_id}'
#
#
# class Chat(models.Model):
#     broadcaster = models.ForeignKey(User, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=10)
#     chat_id = models.CharField(max_length=30)
#     shelf_life = models.DateField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     def str(self):
#         return f'CHAT {self.nickname}'
