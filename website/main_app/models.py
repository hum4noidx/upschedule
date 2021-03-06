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
    name = models.CharField('Имя', max_length=255, )
    city = models.CharField('Город', max_length=255, )
    short_name = models.CharField('Короткое имя', max_length=15, unique=True)

    class Meta:
        verbose_name = 'Школа'
        verbose_name_plural = 'Школы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Classroom(models.Model):
    number = models.CharField('Кабинет', max_length=10)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кабинет'
        verbose_name_plural = 'Кабинеты'
        ordering = ['number']

    def __str__(self):
        return self.number


class Grade(models.Model):
    grade = models.IntegerField('Класс', )
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    grade_short = models.CharField(max_length=15, default='None')

    class Meta:
        verbose_name = 'Класс'
        verbose_name_plural = 'Классы'

    def __str__(self):
        return self.grade_short


class Math(models.Model):
    math = models.CharField('Математика', max_length=50)
    math_short = models.CharField(max_length=15, default='None')

    class Meta:
        verbose_name = 'Математика'
        verbose_name_plural = 'Математика'

    def __str__(self):
        return self.math


class Profile(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    profile = models.CharField('Профиль', max_length=50)
    math = models.ForeignKey(Math, on_delete=models.CASCADE, null=True, default=3)
    profile_db = models.CharField('Имя для бота', max_length=30)
    profile_short = models.CharField(max_length=15, default='None')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['grade', 'profile']

    def __str__(self):
        return self.id


class Discipline(models.Model):
    lsn_name = models.CharField('Предмет', max_length=50)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['lsn_name', ]

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
    date_short = models.CharField(max_length=15, default='None')

    class Meta:
        verbose_name = 'День недели'
        verbose_name_plural = 'Дни недели'
        ordering = ['id']

    def __str__(self):
        return self.day


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


class Horoscope(models.Model):
    sign_name = models.CharField(max_length=20)
    sign_ru = models.CharField(max_length=20)
    sign_text = models.TextField(max_length=1000)

    class Meta:
        verbose_name = 'Гороскоп'
        verbose_name_plural = 'Гороскопы'

    def __str__(self):
        return self.sign_ru


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
        ordering = ['id']


class Subscription(models.Model):
    user_id = models.IntegerField(unique=True)
    title = models.CharField('Название подписки', max_length=120, null=True)
    status = models.BooleanField('Статус подписки', default=False, null=True)
    args = models.CharField('Дополнительно', max_length=120, null=True)
    title_ru = models.CharField('Название(ру)', max_length=50, null=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.title
