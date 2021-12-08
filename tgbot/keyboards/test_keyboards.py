from operator import itemgetter

from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram_dialog import (
    Dialog, DialogManager, Window, DialogRegistry, StartMode
)
from aiogram_dialog.widgets.kbd import (
    Button, Group, Multiselect
)
from aiogram_dialog.widgets.text import Format


class Register(StatesGroup):
    hello = State()
    name = State()


# let's assume this is our window data getter
async def get_data(dialog_manager: DialogManager, **kwargs):
    fruits = [
        ("Apple", '1'),
        ("Pear", '2'),
        ("Orange", '3'),
        ("Banana", '4'),
    ]
    return {
        'name': 'Test',
        "fruits": fruits,
        "count": len(fruits),
    }


items = [("One", 1), ("Two", 2), ("Three", 3), ("Four", 4)]
multiselect = Multiselect(
    Format("✓ {item[0]}"), Format("{item[0]}"),
    "mselect",
    itemgetter(0),
    items,
)

dialog2 = Dialog(
    Window(
        Format('Hello, {name}!'),
        Group(
            Button(Format("{name}"), "b1"),
        ),
        multiselect,
        getter=get_data,
        state=Register.hello,
    ))


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Register.hello, mode=StartMode.RESET_STACK)


def register_dialog(dp):
    registry = DialogRegistry(dp)
    dp.register_message_handler(start, text='/s', state='*')
    registry.register(dialog2)
