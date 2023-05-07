from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from infrastructure.database.repositories.user import UserRepo
from tgbot.states.user_states import RegistrationSG


async def on_grade_selected(event: CallbackQuery, widget: Any, manager: DialogManager, grade: str):
    user_repo: UserRepo = manager.middleware_data.get('user_repo')
    await user_repo.update_user_profile(user_id=event.from_user.id, grade=int(grade))
    await manager.switch_to(RegistrationSG.success)
