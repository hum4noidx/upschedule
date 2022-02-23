import logging
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
        data = ctx_data.get()
        repo = data.get("repo")
        exists = await repo.check_registered(user_id)
        name = await greeting(user_id)
        school = await repo.db_get_user_school(user_id)
        dialog_manager.current_context().dialog_data["school"] = school
        date = await current_date()
        return {
            "registered": exists,
            'not_registered': not exists,
            'name': name,
            'user_id': user_id,
            'date': date[0],
            'next_date': date[1],
            'school': school
        }

    async def get_schools(dialog_manager: DialogManager, **kwargs):
        data = ctx_data.get()
        repo = data.get("repo")
        schools = await repo.get_schools()

        return {
            "schools": schools,
        }

    async def get_grades(dialog_manager: DialogManager, **kwargs):
        school = dialog_manager.current_context().dialog_data.get("school", None)
        data = ctx_data.get()
        repo = data.get("repo")
        grades = await repo.get_grades(school)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "grades": grades,
        }

    async def get_profiles(dialog_manager: DialogManager, **kwargs):
        grade = dialog_manager.current_context().dialog_data.get("grade", None)
        data = ctx_data.get()
        repo = data.get("repo")
        profiles = await repo.get_profiles(grade)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "profiles": profiles,
        }

    async def get_maths(dialog_manager: DialogManager, **kwargs):
        data = ctx_data.get()
        repo = data.get("repo")
        math = await repo.get_maths()

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "maths": math,
        }

    async def get_days(dialog_manager: DialogManager, **kwargs):
        data = ctx_data.get()
        repo = data.get("repo")
        days = await repo.get_days()
        logging.info(days)
        return {
            'days': days,
        }

    async def get_user_grades(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.event.from_user.id
        data = ctx_data.get()
        repo = data.get("repo")
        school = await repo.db_get_user_school(user_id)
        grades = await repo.get_grades(school)
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
        if user_date_chosen:
            user_date = user_date_chosen
        data = ctx_data.get()
        repo = data.get("repo")

        user_data = await repo.get_timetable(user_id)
        user_class = user_data['user_class_id']
        user_profile = user_data['user_prof_id']
        user_math = user_data['user_math_id']

        dialog_manager.current_context().dialog_data['user_class'] = user_class
        dialog_manager.current_context().dialog_data['user_profile'] = user_profile
        dialog_manager.current_context().dialog_data['user_math'] = user_math
        dialog_manager.current_context().dialog_data['user_date'] = user_date

        timetable = await repo.get_schedule(int(user_class), int(user_profile), int(user_math), int(user_date))
        c_date = await current_date()

        dates = {'⏮️': 'prev_date', '⏭️': 'next_date'}
        dates = list(dates.items())
        extended = dialog_manager.current_context().dialog_data.get('profile_extended', None)
        return {
            'timetable': timetable,
            'date': c_date[0],
            'next_date': c_date[1],
            'days': dates,
            'extended': extended,
        }
