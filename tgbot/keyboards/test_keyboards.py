# import operator
#
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import StatesGroup, State
# from aiogram.types import Message, CallbackQuery
# from aiogram_dialog import (
#     Dialog, DialogManager, Window, DialogRegistry, StartMode
# )
# from aiogram_dialog.widgets.kbd import (
#     Button, Group, Multiselect
# )
# from aiogram_dialog.widgets.text import Format, Const
#
#
# class Register(StatesGroup):
#     hello = State()
#     name = State()
#
#
# # let's assume this is our window data getter
# async def get_data(dialog_manager: DialogManager, **kwargs):
#     profiles_11 = [
#         ('Физмат', 'fm'),
#         ('Гуманитарий', 'gum'),
#         ('Соцэконом', 'se'),
#         ('Биохим', 'bh'),
#     ]
#     classes = [
#         ('10', 'class_10'),
#         ('11', 'class_11'),
#     ]
#     return {
#         'name': 'Test',
#         'profiles_11': profiles_11
#
#     }
#
#
# items = [("One", 1), ("Two", 2), ("Three", 3), ("Four", 4)]
#
# ms_profiles_11 = Multiselect(
#     Format("✓ {item[0]}"), Format("{item[0]}"),
#     "mselect",
#     # itemgetter(0),
#     item_id_getter=operator.itemgetter(1),
#     items='profiles_11',
# )
#
# dialog2 = Dialog(
#     Window(
#         Format('Hello, {name}!'),
#         Group(
#             ms_profiles_11,
#             Button(Const('Подтвердить'), "b1"),
#             width=2
#         ),
#         # multiselect,
#         getter=get_data,
#         state=Register.hello,
#     ))
#
#
# async def start(m: Message, dialog_manager: DialogManager):
#     await dialog_manager.start(Register.hello, mode=StartMode.RESET_STACK)
#
#
# async def choose_classes(c: CallbackQuery, dialog_manager: DialogManager, state: FSMContext):
#     pass
#
#
# async def choose_profiles_11(c: CallbackQuery, dialog_manager: DialogManager, state: FSMContext):
#     print(ms_profiles_11.get_checked(dialog_manager))
#     await state.update_data(profiles=ms_profiles_11.get_checked(dialog_manager))
#
#
# def register_dialog(dp):
#     registry = DialogRegistry(dp)
#     dp.register_message_handler(start, text='/s', state='*')
#     dp.register_callback_query_handler(choose_profiles_11, text='b1', state='*')
#     registry.register(dialog2)
