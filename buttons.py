from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove


quskb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Да"),
            KeyboardButton(text="Начать все заново")
        ]
    ],
    resize_keyboard=True
)

cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена ❌")
        ]
    ],
    resize_keyboard=True
)


change = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Дата Планерки")
        ],
        [
            KeyboardButton(text="Время прихода"),
            KeyboardButton(text="Срочные задачи")
        ],
        [
            KeyboardButton(text="Важные задачи"),
            KeyboardButton(text="Дополнительные задачи")
        ],
        [
            KeyboardButton(text="Проблемы"),
            KeyboardButton(text="Комментарии")
        ]
    ],
    resize_keyboard=True
)
