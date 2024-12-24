from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton , KeyboardButton , ReplyKeyboardRemove

# Кнопка отмены
cancel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Отмена ❌")
        ]
    ],
    resize_keyboard=True
)



# Самая главная клавиатура 
mainkb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Моя планерка 🧾")
        ],
        [
            KeyboardButton(text="Дата 📅"),
            KeyboardButton(text="Время прихода 🕰"),
        ],
        [
            KeyboardButton(text="Задачи 📝"),
            KeyboardButton(text="Итоги 🎯"),
        ],
        [
            KeyboardButton(text="Проблемы 👹"),
            KeyboardButton(text="Комментарии 🗣"),
        ],
        [
            KeyboardButton(text="Очистить планерку 🧹"),
            KeyboardButton(text="Отправить 📤"),
        ]
    ],
    resize_keyboard=True
)
