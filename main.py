# жсонка и логирование
import json
import asyncio
import logging
import sys
# Импортим все Aiogramовские библиотеки
from aiogram import Bot, Dispatcher, Router, types , F 
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart , Command
from aiogram.types import Message , CallbackQuery ,FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup , InlineKeyboardMarkup , InlineKeyboardButton ,ReplyKeyboardRemove 

# time and pc 
import os
import time
from datetime import datetime
# Работа с самой jsonкой 
from workwithjson import read_json, write_json, update_user_data, clear_user_data

# dotenv 
from dotenv import load_dotenv
import os
# files import 
from states import Suggest
from states import Problem
from states import Send
from states import QUESTIONS
import buttons
from states import PlanerkaStates

# Google connected API's
import gspread
from google.oauth2.service_account import Credentials



load_dotenv("day.env")  # Загружает переменные из файла .env
token = os.getenv("TOKEN")# получение токена из .env файлика Токен бота 
group = os.getenv("group")# получение токена из .env файлкика Токен группы


admin_id = 7095194058
TOKEN = f"{token}"

bot = Bot(TOKEN)
dp = Dispatcher()
router = Router()

# Все айдишки наших сотрудников 
Adamarid = {
    "498128668" : "Курмет",
    "486553403" : "Айдай",
    "1777950440" : "Нуртилек",
    "314545333" : "Адель моушн-дизайнер",
    "1445703692" : "Элиза",
    "7095194058" : "Эмирлан",
    "7388391479" : "Сания",
    "6366651156" : "Адель",
    "1015135651" : "Ибадат",
    "785058663" : "Мурат",
    "475004396" : "Ажар",
    "6316190199" : "Суаида",
    "596067209" : "Богдан",
    "852617668" : "Жумагуль"
}



# Создаем скопик
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
# Айдишка самой таблицы 
sheet_id = "1_okoGuJ1fWLQ4-8eR0RlXI2ks0EmrvZG8b51jScIr38"
sheet = client.open_by_key(sheet_id) # обертка самой таблицы , все обращения делаются через нее , то есть к которой мы можем обращаться 





# Отмена отправки планерки 
@dp.message(F.text.contains("Отмена ❌"))
async def getcanceled(message: Message,state: FSMContext):
    await message.answer("Вы отменили действие!",reply_markup=ReplyKeyboardRemove())
    await state.clear()
    return 

# Добавление в гугл-таблицы , улучшает читаемость самого кода 
def update_google_sheet(sheet, user_name, data):
    try:
        # Проверяем существование листа
        try:
            worksheet = sheet.worksheet(user_name)
        except gspread.exceptions.WorksheetNotFound:
            # Если лист не найден, создаем новый
            worksheet = sheet.add_worksheet(title=user_name, rows=100, cols=10)
            headers = ['Дата', 'Время прихода', 'Срочные задачи', 'Важные задачи', 
                       'Доп задачи', 'Итог', 'Проблемы', 'Комментарии']
            worksheet.append_row(headers)

        # Добавляем новую строку с данными
        datenow = datetime.now().strftime('%Y-%m-%d')
        new_row = [
            datenow, data['arrival_time'], data['urgent_tasks'],
            data['important_tasks'], data['additional_tasks'], data['result'],
            data['problems'], data['comments']
        ]
        worksheet.append_row(new_row)

        # Форматирование
        worksheet.format('A1:H1', {"textFormat": {"bold": True}})
        worksheet.format(f'A2:H{worksheet.row_count}', {"wrapStrategy": "WRAP"})

        

    except Exception as e:
        print(f"Ошибка при обновлении Google Sheets: {e}")
# ////////////////////////////////////////////////////////////




# Кнопочка /start
@dp.message(Command("start"))
async def letsstart(message: Message):
    await message.answer(f"Привет <b>{message.from_user.first_name}</b>, я бот ADAMAR Планерка",parse_mode="HTML")






# Команда /planerka 
@dp.message(Command("planerka"))
async def start_planerka(message: Message , state : FSMContext):
    usid = message.from_user.id
    if str(usid) not in Adamarid:
        await message.answer("Доступ запрещен")
        return
    else:
        await message.answer(QUESTIONS["dateofplanerka"],reply_markup=buttons.cancel)
        await state.set_state(PlanerkaStates.dateofplanerka)

# Обработчик состояний
# Время прихода 
@dp.message(PlanerkaStates.dateofplanerka)
async def handle_dateofplanerka(message: Message, state: FSMContext):
    await state.update_data(dateofplanerka=message.text)
    await state.set_state(PlanerkaStates.arrival_time)
    await message.answer(QUESTIONS["arrival_time"])
# Время прихода
@dp.message(PlanerkaStates.arrival_time)
async def handle_arrival_time(message: Message, state: FSMContext):
    await state.update_data(arrival_time=message.text)
    await state.set_state(PlanerkaStates.urgent_tasks)
    await message.answer(QUESTIONS["urgent_tasks"])

 # Срочные задачи 
@dp.message(PlanerkaStates.urgent_tasks)
async def handle_urgent_tasks(message: Message, state: FSMContext):
    await state.update_data(urgent_tasks=message.text)
    await state.set_state(PlanerkaStates.important_tasks)
    await message.answer(QUESTIONS["important_tasks"])
# Важные задачи 
@dp.message(PlanerkaStates.important_tasks)
async def handle_important_tasks(message: Message, state: FSMContext):
    await state.update_data(important_tasks=message.text)
    await state.set_state(PlanerkaStates.additional_tasks)
    await message.answer(QUESTIONS["additional_tasks"])
    
 # Дополнительные задачи 
@dp.message(PlanerkaStates.additional_tasks)
async def handle_additional_tasks(message: Message, state: FSMContext):
    await state.update_data(additional_tasks=message.text)
    await state.set_state(PlanerkaStates.result)
    await message.answer(QUESTIONS["result"])
 # Итог
@dp.message(PlanerkaStates.result)
async def handle_problems(message: Message, state: FSMContext):
    await state.update_data(result=message.text)
    await state.set_state(PlanerkaStates.problems)
    await message.answer(QUESTIONS["problems"])

# Проблемы 
@dp.message(PlanerkaStates.problems)
async def handle_problems(message: Message, state: FSMContext):
    await state.update_data(problems=message.text)
    await state.set_state(PlanerkaStates.comments)
    await message.answer(QUESTIONS["comments"]) 

@dp.message(PlanerkaStates.comments)
async def handle_comments(message: Message, state: FSMContext):
    await state.update_data(comments=message.text)
    await state.set_state(PlanerkaStates.confirm)
    await message.answer(QUESTIONS["confirm"],reply_markup=buttons.quskb)

@dp.message(PlanerkaStates.confirm)
async def handle_confirm(message: Message, state: FSMContext):
    if message.text == "Да":
        data = await state.get_data()
        usid = message.from_user.id
        user_name  = Adamarid[f"{usid}"]
        datenow = datetime.now().strftime('%Y-%m-%d')
        summary = (
            f"📋 <b>Ваша планерка:</b>\n\n"
            f"📅 Дата планерки: {data.get('dateofplanerka', 'не указано')}\n\n"
            f"⏰ Время прихода: {data['arrival_time']}\n\n"
            f"🔴 Срочные задачи: {data['urgent_tasks']}\n\n"
            f"🟠 Важные задачи: {data['important_tasks']}\n\n"
            f"🟢 Дополнительные задачи: {data['additional_tasks']}\n\n"
            f"🚀 Итог : {data["result"]}\n\n"
            f"⚠️ Проблемы: {data['problems']}\n\n"
            f"💬 Комментарии: {data['comments']}"
        )
        summaryforteam = (
            f"📋 <b>{user_name}</b>\n\n"
            f"📅 Дата планерки: {data.get('dateofplanerka', 'не указано')}\n\n"
            f"⏰ Время прихода: {data['arrival_time']}\n\n"
            f"🔴 Срочные задачи: {data['urgent_tasks']}\n\n"
            f"🟠 Важные задачи: {data['important_tasks']}\n\n"
            f"🟢 Дополнительные задачи: {data['additional_tasks']}\n\n"
            f"🚀 Итог : {data["result"]}\n\n"
            f"⚠️ Проблемы: {data['problems']}\n\n"
            f"💬 Комментарии: {data['comments']}"
        )
        chatidof = -1002130834445
        # -1002130834445_4
        await message.answer(summary,parse_mode="HTML",reply_markup=ReplyKeyboardRemove())
        await bot.send_message(chat_id=chatidof,text=summaryforteam,parse_mode="HTML",message_thread_id=4)
        update_google_sheet(sheet=sheet,user_name=user_name,data=data)
        print(f"Данные успешно записаны для {user_name}")
        await state.clear()
    else:
        await message.answer("Вы начинаете заново , данные очистились",reply_markup=ReplyKeyboardRemove())
        await state.clear()
        return 










# Кнопочка для рассылки  
@dp.message(Command("send"))
async def sendtoallworkers(message: Message , state :FSMContext):
    await message.answer(f"""Привет <b>{message.from_user.first_name}</b> 
Отправьте текст который вы хотите отправить!""",parse_mode="HTML")
    await state.set_state(Send.allinfo)

# Получение самого текста  
@dp.message(Send.allinfo)
async def starttospread(message: Message, state: FSMContext):
    msg = message.text
    allkyes = list(Adamarid.keys()) # все айдишки наших сотрудников , Adamar group 
    j=0
    failed_users = [] # список людей до которых не дошло сообщение
    try:
        for i in allkyes:
            await bot.send_message(i,msg)
            j+=1 # Увеличение количества 
    except Exception as e:
        failed_users.append(i,str(e)) # добавление людей до которых не дошло сообщение
    finally:
        await asyncio.sleep(0.33)   # Интервал между отправками
    
    await message.answer(f"Количество отправленных рассылок : {j}") # Отправка лога о кол-ве отправленных рассылок 

    # Если есть ошибки, уведомляем о них
    if failed_users:
        failed_list = "\n".join([f"ID: {user_id}, Error: {error}" for user_id, error in failed_users])
        await message.answer(f"Не удалось отправить сообщения следующим пользователям:\n{failed_list}")
    
    await state.clear() # Очищение FSM


# Анонимное отправление проблемы
@dp.message(Command("problem"))
async def sendproblem(message: Message,state: FSMContext):
    await message.answer("""Я никому ничего не расскажу 🤐
Что тебя беспокоит ? """)
    await state.set_state(Problem.problemtext) # ждем проблему от сотрудника
# Получение текста 
@dp.message(Problem.problemtext)
async def problemisonway(message: Message, state: FSMContext):
    msg = message.text # сама проблема 
    founderlist = [498128668]  # Айди  Курмета
    for i in founderlist:
        await bot.send_message(i,f"""<b>Проблема ‼️</b>
{msg}
""")
        await asyncio.sleep(0.33) # интервал между отправками
    print("Все отправилось !")


# Анонимное отправление предложения
@dp.message(Command("suggest"))
async def sendsuggest(message: Message,state: FSMContext):
    await message.answer("""Я никому ничего не расскажу 🤐
Что ты хочешь предложить ? """)
    await state.set_state(Suggest.suggesttext) # ждем предложение от сотрудника
# Получение текста 
@dp.message(Suggest.suggesttext)
async def suggestonhisway(message: Message, state: FSMContext):
    msg = message.text # сама проблема 
    founderlist = [498128668]  # Айди Сании и Курмета  [7095194058]
    for i in founderlist:
        await bot.send_message(i,f"""<b>Предложение  ✏️</b> 
{msg}
""",parse_mode="HTML")
        await asyncio.sleep(0.33) # интервал между отправками
    print("Все отправилось !")







    








async def main() -> None:
    
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    # And the run events dispatching of course bitch 
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main()) 
