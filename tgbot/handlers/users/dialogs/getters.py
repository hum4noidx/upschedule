import logging
from datetime import datetime, date

from aiogram.dispatcher.handler import ctx_data
from aiogram_dialog import DialogManager

from tgbot.handlers.admins.admin import greeting


class Getter:
    async def check_exists(dialog_manager: DialogManager, **kwargs):
        user_id = dialog_manager.current_context().dialog_data.get("user_id", None)
        name = dialog_manager.current_context().dialog_data.get("name", None)
        logging.info(name)
        data = ctx_data.get()
        repo = data.get("repo")
        exists = await repo.check_registered(user_id)
        name = await greeting(user_id)
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
        }

    async def get_data1(dialog_manager: DialogManager, **kwargs):
        data = ctx_data.get()
        repo = data.get("repo")
        schools = await repo.get_schools()
        return {
            "schools": schools,
        }

    async def get_data2(dialog_manager: DialogManager, **kwargs):
        school = dialog_manager.current_context().dialog_data.get("school", None)
        data = ctx_data.get()
        repo = data.get("repo")
        grades = await repo.get_grades(school)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "grades": grades,
        }

    async def get_data3(dialog_manager: DialogManager, **kwargs):
        grade = dialog_manager.current_context().dialog_data.get("grade", None)
        data = ctx_data.get()
        repo = data.get("repo")
        profiles = await repo.get_profiles(grade)

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "profiles": profiles,
        }

    async def get_data4(dialog_manager: DialogManager, **kwargs):
        math = dialog_manager.current_context().dialog_data.get("profile", None)
        data = ctx_data.get()
        repo = data.get("repo")
        math = await repo.get_maths()

        return {
            "name": dialog_manager.current_context().dialog_data.get("name", ""),
            "maths": math,
        }
