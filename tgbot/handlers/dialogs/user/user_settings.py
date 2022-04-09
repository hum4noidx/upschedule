import operator
from typing import Any

from aiogram.dispatcher.handler import ctx_data
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Group, Cancel, Start, Select
from aiogram_dialog.widgets.text import Format, Const

from tgbot.handlers.dialogs.misc.getters import Getter
from tgbot.states.states import UserSettings, RegSG, SubscriptionsSG, RegHoroscopeSG


async def on_horoscope_reg_selected(c: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.current_context().dialog_data["sign"] = item_id
    db = ctx_data.get().get('repo')
    await db.update_user_horoscope_sign(item_id, manager.event.from_user.id)
    await manager.dialog().next()


dialog_user_settings = Dialog(
    Window(
        Format('{settings}'),
        Group(
            Start(Const('Регистрация'), id='register', state=RegSG.school),
            Start(Const('Подписки'), id='subscriptions', state=SubscriptionsSG.subscriptions),
            Cancel(Format('🔝 В главное меню')),
        ),
        getter=Getter.settings_getter,
        state=UserSettings.profile
    ),
)

dialog_subscriptions = Dialog(
    Window(
        Format(
            '<b>Активные подписки:</b>\n{subscription_title}:{subscription_status}\n\n'
            'Раздел дорабатывается, если нужно изменить или отменить подписку - @hum4noidx'),
        Start(Const('Подписаться на гороскопы'), id='h_subscribe', state=RegHoroscopeSG.main),
        Cancel(Const('Назад')),
        getter=Getter.subscriptions_getter,
        state=SubscriptionsSG.subscriptions
    ),
)

dialog_horoscope_subscribe = Dialog(
    Window(
        Const('Выбери знак зодиака'),
        Group(
            Select(
                Format('{item[0]}'),
                id='sign',
                item_id_getter=operator.itemgetter(1),
                items='signs',
                on_click=on_horoscope_reg_selected,
            ),
            Cancel(Const('В главное меню')),
            width=2
        ),
        state=RegHoroscopeSG.main,
        getter=Getter.get_horoscope_signs
    ),
    Window(
        Const('Регистрация успешна'),
        Cancel(Const('В главное меню')),
        state=RegHoroscopeSG.finish
    )
)
