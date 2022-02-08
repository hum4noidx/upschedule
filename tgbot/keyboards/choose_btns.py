from aiogram.dispatcher.handler import ctx_data
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

classes = CallbackData('class', 'classes')
profile = CallbackData('profile', 'profile')
profile_other = CallbackData('profile', 'profile', 'math', 'day')
profile_other_day = CallbackData('day', 'day')
math = CallbackData('math', 'math')
week = CallbackData('day', 'day')
# \____________________ CANCEL BUTTONS ____________________/
user_registration_cancel = InlineKeyboardButton(text='Назад', callback_data='user_registration_cancel')
cancel_butt = InlineKeyboardButton(text='В главное меню', callback_data='go_main')
# \____________________ CHOOSING CLASS, PROFILE, MATH ____________________/
# choosing class
class_5 = InlineKeyboardButton(text='5 класс', callback_data=classes.new(classes=5))
class_6 = InlineKeyboardButton(text='6 класс', callback_data=classes.new(classes=6))
class_7 = InlineKeyboardButton(text='7 класс', callback_data=classes.new(classes=7))
class_8 = InlineKeyboardButton(text='8 класс', callback_data=classes.new(classes=8))
class_9 = InlineKeyboardButton(text='9 класс', callback_data=classes.new(classes=9))
class_10 = InlineKeyboardButton(text="10 класс", callback_data=classes.new(classes=10))
class_11 = InlineKeyboardButton(text="11 класс", callback_data=classes.new(classes=11))
class_all = InlineKeyboardButton(text='Все классы', callback_data=classes.new(classes='classes_all'))
broadcast_groups = InlineKeyboardButton(text="Рассылка в беседы", callback_data='group_broadcast')
user_choose_class = InlineKeyboardMarkup(row_width=2).row(class_5, class_6).row(class_7, class_8).row(class_9,
                                                                                                      class_10).row(
    class_11).row(cancel_butt)
broadcast_choose_class = InlineKeyboardMarkup(row_width=2).row(class_5, class_6).row(class_7, class_8).row(class_9,
                                                                                                           class_10).row(
    class_11, class_all).row(cancel_butt)

# choosing profile for 11 class
profile_fm = InlineKeyboardButton(text="Физмат", callback_data=profile.new(profile="fm"))
profile_gum = InlineKeyboardButton(text="Гуманитарий", callback_data=profile.new(profile="gum"))
profile_se = InlineKeyboardButton(text="Соцэконом", callback_data=profile.new(profile="se"))
profile_bh = InlineKeyboardButton(text="Биохим", callback_data=profile.new(profile="bh"))
profile_all = InlineKeyboardButton(text="Всему классу", callback_data=profile.new(profile="class_all"))
user_choose_profile_11 = InlineKeyboardMarkup(row_width=2).add(
    profile_fm, profile_gum, profile_se, profile_bh, cancel_butt
)
broadcast_choose_profile_11 = InlineKeyboardMarkup(row_width=2).add(profile_fm, profile_gum, profile_se, profile_bh,
                                                                    profile_all, cancel_butt)

# choose profile for 10 class
profile_med = InlineKeyboardButton(text="Медицинский", callback_data=profile.new(profile="med"))
profile_media = InlineKeyboardButton(text="Медиа", callback_data=profile.new(profile="media"))
profile_akadem = InlineKeyboardButton(text="Академический", callback_data=profile.new(profile="akadem"))
profile_it = InlineKeyboardButton(text="Инженеры/IT", callback_data=profile.new(profile="it"))
user_choose_profile_10 = InlineKeyboardMarkup(row_width=2).add(
    profile_med, profile_media, profile_akadem, profile_it, cancel_butt
)
broadcast_choose_profile_10 = InlineKeyboardMarkup(row_width=2).add(profile_med, profile_media, profile_akadem,
                                                                    profile_it, profile_all, cancel_butt)
letter_a = InlineKeyboardButton(text="А", callback_data=profile.new(profile="a"))
letter_b = InlineKeyboardButton(text="Б", callback_data=profile.new(profile="b"))
letter_v = InlineKeyboardButton(text="В", callback_data=profile.new(profile="v"))
user_choose_letter = InlineKeyboardMarkup(row_width=2).row(letter_a, letter_b, letter_v).row(cancel_butt)
broadcast_choose_letter = InlineKeyboardMarkup(row_width=2).add(letter_a, letter_b, letter_v, cancel_butt)

# choosing math level
math_prof = InlineKeyboardButton(text='Профиль', callback_data=math.new(math='prof'))
math_base = InlineKeyboardButton(text='База', callback_data=math.new(math='basic'))
math_all = InlineKeyboardButton(text='Всему профилю', callback_data=math.new(math='all'))
user_choose_math = InlineKeyboardMarkup(row_width=2).add(math_prof, math_base, cancel_butt)
broadcast_choose_math = InlineKeyboardMarkup(row_width=2).add(math_prof, math_base, math_all, cancel_butt)

# choosing day
day_1 = InlineKeyboardButton(text="Понедельник", callback_data=week.new(day="1"))
day_2 = InlineKeyboardButton(text="Вторник", callback_data=week.new(day="2"))
day_3 = InlineKeyboardButton(text="Среда", callback_data=week.new(day="3"))
day_4 = InlineKeyboardButton(text="Четверг", callback_data=week.new(day="4"))
day_5 = InlineKeyboardButton(text="Пятница", callback_data=week.new(day="5"))
user_choose_day = InlineKeyboardMarkup(row_width=2).add(day_1, day_2, day_3, day_4, day_5, cancel_butt)

# other_schedule buttons
profile_fm_other = InlineKeyboardButton(text='Физмат',
                                        callback_data=profile_other.new(profile='fm', math='prof', day='None'))
profile_gum_other = InlineKeyboardButton(text="Гуманитарий(П)",
                                         callback_data=profile_other.new(profile="gum", math='prof', day='None'))
profile_gum_base_other = InlineKeyboardButton(text="Гуманитарий(Б)",
                                              callback_data=profile_other.new(profile="gum", math='basic', day='None'))
profile_se_other = InlineKeyboardButton(text="Соцэконом(П)",
                                        callback_data=profile_other.new(profile="se", math='prof', day='None'))
profile_se_base = InlineKeyboardButton(text="Соцэконом(Б)",
                                       callback_data=profile_other.new(profile="se", math='basic', day='None'))
profile_bh_other = InlineKeyboardButton(text="Биохим(П)",
                                        callback_data=profile_other.new(profile="bh", math='prof', day='None'))
profile_bh_base = InlineKeyboardButton(text="Биохим(Б)",
                                       callback_data=profile_other.new(profile="bh", math='basic', day='None'))
prev_day = InlineKeyboardButton(text="🔚", callback_data=profile_other.new(profile='None', math='None', day='prev'))
next_day = InlineKeyboardButton(text="🔜", callback_data=profile_other.new(profile='None', math='None', day='next'))


def make_buttons():
    markup_1 = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup_1.row(profile_fm_other).row(profile_gum_other, profile_gum_base_other).row(
        profile_se_other, profile_se_base).row(profile_bh_other, profile_bh_base).row(prev_day, next_day).row(
        cancel_butt)
    return markup_1


def make_buttons_y():
    markup_2 = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup_2.row(letter_a, letter_b, letter_v).row(cancel_butt)
    return markup_2


async def make_buttons_class():
    markup = InlineKeyboardMarkup(row_width=2)
    data = ctx_data.get()
    repo = data.get("repo")
    grades = await repo.get_classes()
    for grade, short_name in grades:
        markup.insert(InlineKeyboardButton(text=grade, callback_data=classes.new(classes=short_name)))
    return markup


async def make_buttons_profile():
    markup1 = InlineKeyboardMarkup(row_width=2)
    data = ctx_data.get()
    repo = data.get("repo")
    profiles = await repo.get_classes()
    for grade, short_name in profiles:
        markup1.insert(InlineKeyboardButton(text=grade, callback_data=classes.new(classes=short_name)))
    return markup1
