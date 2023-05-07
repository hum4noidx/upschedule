from aiogram_dialog import DialogRegistry

from .dialogs import (
    registration,
)


def setup(registry: DialogRegistry):
    registry.register(registration)
