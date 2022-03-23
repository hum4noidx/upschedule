from datetime import datetime, date

from aiogram.dispatcher.handler import ctx_data
from aiogram_dialog import DialogManager

from tgbot.handlers.admins.admin import greeting


async def current_date():
    today = datetime.now()
    wd = date.weekday(today)
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    day = days[wd]
    next_wd = wd + 1
    if next_wd == 7:
        next_wd -= 7
    next_date = days[next_wd]
    return day, next_date


class Getter:
    async def check_exists(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.event.from_user.id
        db = ctx_data.get().get('repo')
        exists = await db.check_registered(user_id)
        name = await greeting(user_id)
        school = await db.db_get_user_school(user_id)
        dialog_manager.current_context().dialog_data["school"] = school
        date = await current_date()
        admin = await db.get_admins(user_id)
        return {
            "registered": exists,
            'not_registered': not exists,
            'name': name,
            'user_id': user_id,
            'date': date[0],
            'next_date': date[1],
            'school': school,
            'admin': admin
        }

    async def get_schools(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        schools = await db.get_schools()

        return {
            "schools": schools,
        }

    async def get_grades(dialog_manager: DialogManager, **kwargs):
        school = int(dialog_manager.current_context().dialog_data.get("school", None))
        db = ctx_data.get().get('repo')
        grades = await db.reg_get_grades(school)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "grades": grades,
        }

    async def get_profiles(dialog_manager: DialogManager, **kwargs):
        grade = dialog_manager.current_context().dialog_data.get("grade", None)
        db = ctx_data.get().get('repo')
        profiles = await db.get_profiles(grade)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "profiles": profiles,
            'grade': grade,
        }

    async def get_maths(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        math = await db.get_maths()

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "maths": math,
        }

    async def get_days(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        days = await db.get_days()

        return {
            'days': days,
        }

    async def get_user_grades(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.event.from_user.id
        db = ctx_data.get().get('repo')
        grades = await db.get_grades(user_id)
        return {
            'grades': grades,
        }

    async def get_timetable(dialog_manager: DialogManager, **kwargs):
        timetable = dialog_manager.current_context().dialog_data.get("timetable", None)
        return {
            'timetable': timetable,
        }

    async def fast_timetable_getter(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.event.from_user.id
        chosen_date = dialog_manager.current_context().start_data['date']
        user_date_chosen = dialog_manager.current_context().dialog_data.get('user_date', None)
        today = datetime.now()
        wd = date.weekday(today) + 1
        if chosen_date == 'now':
            user_date = wd
        else:
            user_date = wd + 1
        if user_date == 8:
            user_date -= 7
        elif user_date == 0:
            user_date += 7
        if user_date_chosen:
            user_date = user_date_chosen

        db = ctx_data.get().get('repo')
        extended = dialog_manager.current_context().dialog_data.get('profile_extended', None)
        user_data = await db.get_timetable(user_id)
        await db.schedule_user_usage(dialog_manager.event.from_user.id)
        user_class = user_data['user_class_id']
        if extended:
            user_profile = dialog_manager.current_context().dialog_data.get('user_profile', None)
        else:
            user_profile = user_data['user_prof_id']

        dialog_manager.current_context().dialog_data['user_class'] = user_class
        dialog_manager.current_context().dialog_data['user_profile'] = user_profile
        dialog_manager.current_context().dialog_data['user_date'] = user_date

        timetable = await db.get_schedule(int(user_class), int(user_profile), int(user_date))
        c_date = await current_date()

        dates = {'⏮️': 'prev_date', '⏭️': 'next_date'}
        profiles = await db.get_profiles(user_class)
        dates = list(dates.items())

        return {
            'timetable': timetable,
            'date': c_date[0],
            'next_date': c_date[1],
            'days': dates,
            'extended': extended,
            'profiles': profiles
        }

    async def settings_getter(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        # repo = data.get("repo")
        settings = await db.show_user_info(dialog_manager.event.from_user.id)
        return {
            'settings': settings
        }

    async def get_users_count(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        count = await db.users_count()
        return {
            'count': count
        }

    async def get_users_list(dialog_manager: DialogManager, **kwargs):
        users_list = dialog_manager.current_context().dialog_data.get('users_list', None)

        return {
            'users_list': users_list,
        }

    async def get_horoscope_signs(dialog_manager: DialogManager, **kwargs):
        db = ctx_data.get().get('repo')
        signs = await db.db_get_horoscope_signs()

        return {
            'signs': signs
        }
