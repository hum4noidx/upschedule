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


class Passport(models.Model):
    user_id = models.IntegerField()
    uses = models.IntegerField()
    user_class = models.IntegerField()
    user_prof = models.CharField(max_length=10)
    user_math = models.CharField(max_length=10)
    vip = models.BooleanField()
    admin = models.BooleanField()


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


class Grade(models.Model):
    grade = models.IntegerField('Класс', choices=lsn_numbers)

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return f'{self.grade} класс'


class Profile(models.Model):
    profile = models.CharField('Профиль', max_length=50)
    profile_db = models.CharField('Имя для бота', max_length=30)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.profile} профиль'
