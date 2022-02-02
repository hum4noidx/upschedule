from django.db import models

lsn_numbers = (
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
lsn_grades = (
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
)
lsn_profiles = (
    ('fm', 'Физмат'),
    ('gum', 'Гуманитарий'),
    ('se', 'Соцэконом'),
    ('bh', 'Биохим'),
    ('med', 'Медицинский'),
    ('media', 'Медиа'),
    ('akadem', 'Академический'),
    ('it', 'It/Инженеры')
)
lsn_dates = (
    (1, 'Понедельник'),
    (2, 'Вторник'),
    (3, 'Среда'),
    (4, 'Четверг'),
    (5, 'Пятница'),
)
lsn_maths = (
    ('prof', 'Профильная'),
    ('basic', 'Базовая'),
    ('None', 'Нет математики')
)


# Some stuff


class Material(models.Model):
    title = models.CharField('Заголовок', max_length=60, null=True)
    text = models.TextField('Текст', null=True, blank=True, )
    url = models.URLField('Ссылка', null=True, )
    type = models.CharField('Тип', max_length=60, null=True, blank=True, )
    tag = models.CharField('Тег', max_length=20, null=True, blank=True, )


class Discipline(models.Model):
    lsn_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'

    def __str__(self):
        return self.lsn_name


class Teacher(models.Model):
    name = models.CharField('ФИО', max_length=200)
    specialization = models.CharField('Специальность', max_length=200)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Group(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=255, null=True, blank=True, )


class Grade(models.Model):
    grade = models.IntegerField('Класс', choices=lsn_numbers)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return self.grade


class Profile(models.Model):
    profile = models.CharField('Профиль', max_length=50)
    profile_db = models.CharField('Имя для бота', max_length=30)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.profile_db


class Math(models.Model):
    math = models.CharField('Математика', max_length=50)

    class Meta:
        verbose_name = 'Математика'

    def __str__(self):
        return self.math


class Passport(models.Model):
    user_id = models.IntegerField(unique=True)
    uses = models.IntegerField('Использований', default=1)
    user_class = models.IntegerField('Класс', null=True)
    full_name = models.CharField('Имя', max_length=60, null=True)
    user_prof = models.CharField('Профиль', max_length=10, null=True)
    user_math = models.CharField('Математика', max_length=10, null=True)
    vip = models.BooleanField(default=False, null=True)
    admin = models.BooleanField(default=False, null=True)
    registered = models.BooleanField('Зарегистрирован', default=False, null=True)
    last_seen = models.DateTimeField(null=True)


class Schedule(models.Model):
    lsn_number = models.IntegerField(choices=lsn_numbers)
    lsn_text = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    lsn_class = models.CharField('Кабинет', max_length=15)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lsn_date = models.IntegerField('День недели', choices=lsn_dates)
    lsn_grade = models.IntegerField('Класс', choices=lsn_grades)
    lsn_profile = models.CharField('Профиль', choices=lsn_profiles, max_length=200)
    lsn_math = models.CharField('Математика', choices=lsn_maths, max_length=15)

    class Meta:
        verbose_name = 'График'
        verbose_name_plural = 'Графики'
