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


# Some stuff


class Group(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    group_name = models.CharField(max_length=255, null=True, blank=True, )


class School(models.Model):
    name = models.CharField(max_length=255, )
    city = models.CharField(max_length=255, )
    short_name = models.CharField(max_length=15, unique=True)

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'

    def __str__(self):
        return self.name


class Classroom(models.Model):
    number = models.CharField('Кабинет', max_length=10)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'

    def __str__(self):
        return self.number


class Grade(models.Model):
    grade = models.IntegerField('Класс', '')
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=15, )

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return self.short_name


class Profile(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    profile = models.CharField('Профиль', max_length=50)
    profile_db = models.CharField('Имя для бота', max_length=30)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.profile_db


class Math(models.Model):
    math = models.CharField('Математика', max_length=50)

    class Meta:
        verbose_name = 'Математика'
        verbose_name_plural = 'Математика'

    def __str__(self):
        return self.math


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
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'

    def __str__(self):
        return self.name


class Date(models.Model):
    day = models.CharField('День недели', max_length=15)

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'

    def __str__(self):
        return self.day


class Passport(models.Model):
    user_id = models.IntegerField(unique=True)
    uses = models.IntegerField('Использований', default=1)
    full_name = models.CharField('Имя', max_length=60, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    user_class = models.ForeignKey(Grade, on_delete=models.CASCADE, null=True)
    user_prof = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    user_math = models.ForeignKey(Math, on_delete=models.CASCADE, null=True)
    registered = models.BooleanField('Зарегистрирован', default=False, null=True)
    vip = models.BooleanField(default=False, null=True)
    admin = models.BooleanField(default=False, null=True)
    last_seen = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Schedule(models.Model):
    lsn_number = models.IntegerField(choices=lsn_numbers)
    lsn_text = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    lsn_class = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    lsn_date = models.ForeignKey(Date, on_delete=models.CASCADE)
    lsn_grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    lsn_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    lsn_math = models.ForeignKey(Math, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'


class Material(models.Model):
    title = models.CharField('Заголовок', max_length=60, null=True)
    text = models.TextField('Текст', null=True, blank=True, )
    url = models.URLField('Ссылка', null=True, )
    type = models.CharField('Тип', max_length=60, null=True, blank=True, )
    tag = models.CharField('Тег', max_length=20, null=True, blank=True, )
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Материал'
        verbose_name_plural = 'Материалы'
