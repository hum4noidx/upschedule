from datetime import datetime, date

from aiogram.dispatcher.handler import ctx_data
from aiogram_dialog import DialogManager

from tgbot.handlers.admins.admin import greeting


class Getter:
    async def check_exists(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.event.from_user.id
        name = dialog_manager.event.from_user.full_name
        data = ctx_data.get()
        repo = data.get("repo")
        exists = await repo.check_registered(user_id)
        name = await greeting(user_id)
        school = await repo.db_get_user_school(user_id)
        dialog_manager.current_context().dialog_data["school"] = school
        today = datetime.now()
        wd = date.weekday(today)
        days = ["Пн", "Вт", "Срд", "Чтв", "Пт", "Сб", "Вск"]
        day = days[wd]
        next_wd = wd + 1
        if next_wd == 7:
            next_wd -= 7
        next_date = days[next_wd]
        return {
            "registered": exists,
            'not_registered': not exists,
            'name': name,
            'user_id': user_id,
            'date': day,
            'next_date': next_date,
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
