import asyncio
import logging
import operator
import os.path
from typing import Any

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.handler import ctx_data
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, DialogRegistry, Window, ChatEvent, StartMode
from aiogram_dialog.widgets.kbd import Button, Select, Row, SwitchTo, Back
from aiogram_dialog.widgets.text import Const, Format, Multi

src_dir = os.path.normpath(os.path.join(__file__, os.path.pardir))

API_TOKEN = "1959988028:AAF6y7mTgOjt2fsaG2reMzZsKw05mGrm-WA"


class DialogSG(StatesGroup):
    greeting = State()
    grade = State()
    profile = State()
    math = State()
    finish = State()
    age = State()


async def get_data(dialog_manager: DialogManager, **kwargs):
    age = dialog_manager.current_context().dialog_data.get("age", None)
    data = ctx_data.get()
    repo = data.get("repo")
    grades = await repo.get_classes()
    return {
        "name": dialog_manager.current_context().dialog_data.get("name", ""),
        "age": age,
        "can_smoke": age in ("18-25", "25-40", "40+"),
        "grade": grades
    }


async def name_handler(c: CallbackQuery, button: Button, manager: DialogManager):
    manager.current_context().dialog_data["name"] = c.from_user.full_name
    await manager.dialog().next()


async def on_finish(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("Thank you. To start again click /start")
    await manager.done()


async def on_age_changed(c: ChatEvent, select: Any, manager: DialogManager,
                         item_id: str):
    manager.current_context().dialog_data["age"] = item_id
    await manager.dialog().next()


dialog = Dialog(
    Window(
        Const('Hi!'),
        Button(Const('Go!'), 'b1', on_click=name_handler),
        state=DialogSG.greeting,
    ),
    Window(
        Format("{name}! Из какого ты класса?"),
        Select(
            Format('{item[0]} класс'),
            id='grade',
            item_id_getter=operator.itemgetter(1),
            items='grade'
        ),
        state=DialogSG.age,
        getter=get_data,
        preview_data={"name": "Tishka17"}
    ),
    Window(
        Multi(
            Format("{name}! Thank you for your answers."),
            Const("Hope you are not smoking", when="can_smoke"),
            sep="\n\n",
        ),
        Row(
            Back(),
            SwitchTo(Const("Restart"), id="restart", state=DialogSG.greeting),
            Button(Const("Finish"), on_click=on_finish, id="finish"),
        ),
        getter=get_data,
        state=DialogSG.finish,
    )
)


async def start(m: Message, dialog_manager: DialogManager):
    # it is important to reset stack because user wants to restart everything
    await dialog_manager.start(DialogSG.greeting, mode=StartMode.RESET_STACK)


async def main():
    # real main
    logging.basicConfig(level=logging.INFO)
    storage = MemoryStorage()
    bot = Bot(token=API_TOKEN)
    dp = Dispatcher(bot, storage=storage)
    dp.register_message_handler(start, text="/start", state="*")
    registry = DialogRegistry(dp)
    registry.register(dialog)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
