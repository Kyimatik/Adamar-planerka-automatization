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

# dotenv 
from dotenv import load_dotenv
# files import 

from states import Suggest
from states import Problem
from states import Send
from states import QUESTIONS
import buttons
from states import Date, Time, Tasks, Result, Problems, Comments

# Work with json 

from workjson import create_json_file, read_json_file, save_json_file, update_user_info, get_user_data, clear_user_data
from workjson import file_path
# Google connected API's

import gspread
from google.oauth2.service_account import Credentials
# Настройка крона , для отправки каждый день 

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz





load_dotenv("day.env")  # Загружает переменные из файла .env
token = os.getenv("TOKEN")# получение токена из .env файлика Токен бота 
# token = os.getenv("testtok")# получение токена из .env файлика Токен бота 

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
    "596067209" : "Богдан",
    "1584303142" : "Рамис",
    "777257179" : "Бекзат",
    "1294402272" : "Малика",
    "698809367" : "Азирет",
    "389919701" : "Элина"
}


data = read_json_file(file_path=file_path)
if not data:
    logging.warning("Json файла не существует , создаем новый")
    create_json_file(file_path=file_path, user_data=Adamarid)




# Создаем скопик
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)
# Айдишка самой таблицы 
# sheet_id = "1Q0IKtagefSzvMHkvhPBkiL_gck9L18VMieG9c7BLIMI" # Adamar АЙДАЙ
sheet_id = "1eetUrLBU9W0lHbvEBGOjhhxKX_5tE-0jKBMHVWlZ5BI" # Adamar 2025
sheet = client.open_by_key(sheet_id) # обертка самой таблицы , все обращения делаются через нее , то есть к которой мы можем обращаться 




"""Отмена какого либо действия )"""
# Отмена отправки планерки 
@dp.message(F.text.contains("Отмена ❌"))
async def getcanceled(message: Message,state: FSMContext):
    await message.answer("Вы отменили действие!",reply_markup=ReplyKeyboardRemove())
    await state.clear()
    return 






def update_or_create_google_sheet(sheet, user_name, data, max_retries=5, retry_delay=150):
    """
    Обновление или создание данных для планерки в Google Sheets.

    :param sheet: Объект Google Sheet.
    :param user_name: Имя пользователя.
    :param data: Данные для записи/обновления.
    :param max_retries: Максимальное количество попыток.
    :param retry_delay: Интервал между попытками в секундах.
    """
    for attempt in range(1, max_retries + 1):
        try:
            # Проверяем существование листа
            try:
                worksheet = sheet.worksheet(user_name)
            except gspread.exceptions.WorksheetNotFound:
                logging.warning(f"Google Sheets: Лист для пользователя {user_name} не найден, создаётся новый.")
                worksheet = sheet.add_worksheet(title=user_name, rows=100, cols=6)
                headers = ['Дата', 'Время прихода', 'Задачи', 'Итоги', 'Проблемы', 'Комментарии']
                worksheet.append_row(headers)

            # Проверяем, что данные заполнены
            if not data:
                logging.warning(f"Google Sheets: Пустые данные для записи для пользователя {user_name}.")
                return

            # Проверяем, существует ли уже запись с такой датой
            records = worksheet.get_all_records()
            updated = False
            for row_idx, record in enumerate(records, start=2):  # Начинаем с 2, так как 1-я строка — это заголовки
                if record.get('Дата') == data.get('date'):
                    # Если дата совпала, обновляем все данные
                    new_data = [
                        data.get('date', 'N/A'),
                        data.get('arrival_time', 'N/A'),
                        data.get('tasks', 'N/A'),
                        data.get('result', 'N/A'),
                        data.get('problems', 'N/A'),
                        data.get('comments', 'N/A')
                    ]
                    worksheet.update(f"A{row_idx}:F{row_idx}", [new_data])  # Обновляем все данные строки
                    updated = True
                    break

            # Если записи не было, добавляем новую строку
            if not updated:
                new_row = [
                    data.get('date', 'N/A'),
                    data.get('arrival_time', 'N/A'),
                    data.get('tasks', 'N/A'),
                    data.get('result', 'N/A'),
                    data.get('problems', 'N/A'),
                    data.get('comments', 'N/A')
                ]
                worksheet.append_row(new_row)

            # Форматирование заголовков
            worksheet.format('A1:F1', {"textFormat": {"bold": True}})
            worksheet.format(f'A2:F{worksheet.row_count}', {"wrapStrategy": "WRAP"})

            logging.info(f"Google Sheets: Данные успешно записаны для пользователя {user_name}.")
            return 

        except gspread.exceptions.APIError as e:
            logging.error(f"Попытка {attempt} не удалась. Ошибка API: {e}")
            if attempt < max_retries:
                logging.info(f"Повторная попытка через {retry_delay} секунд...")
                time.sleep(retry_delay)
            else:
                logging.error(f"Превышено количество попыток записи в Google Sheets для пользователя {user_name}.")
                raise e  # Выбрасываем исключение после всех неудачных попыток
        except Exception as e:
            logging.error(f"Непредвиденная ошибка на попытке {attempt}: {e}")
            raise e  # Для других ошибок не делаем повторных попыток




# ////////////////////////////////////////////////////////////



""" Обычная кнопочка старт , приветствие людей"""
# Кнопочка /start
@dp.message(Command("start"))
async def letsstart(message: Message):
    await message.answer(f"Привет <b>{message.from_user.first_name}</b>, я бот ADAMAR Планерка",parse_mode="HTML",reply_markup=buttons.mainkb)





""" Блок РАССЫЛКИ для всех пользователей! 
"""

# Кнопочка для рассылки  
@dp.message(Command("send"))
async def sendtoallworkers(message: Message , state :FSMContext):
    admins = [498128668,7095194058,7388391479]
    if message.from_user.id in admins:
        await message.answer(f"""Привет <b>{message.from_user.first_name}</b> 
    Отправьте текст который вы хотите отправить!""",parse_mode="HTML",reply_markup=buttons.cancel)
        await state.set_state(Send.allinfo)
    else:
        await message.answer("Доступ запрещен")
        return
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
    
    await message.answer(f"Количество отправленных рассылок : {j}",reply_markup=ReplyKeyboardRemove()) # Отправка лога о кол-ве отправленных рассылок 

    # Если есть ошибки, уведомляем о них
    if failed_users:
        failed_list = "\n".join([f"ID: {user_id}, Error: {error}" for user_id, error in failed_users])
        await message.answer(f"Не удалось отправить сообщения следующим пользователям:\n{failed_list}")
    
    await state.clear() # Очищение FSM


# Анонимное отправление проблемы
@dp.message(Command("problem"))
async def sendproblem(message: Message,state: FSMContext):
    await message.answer("""Я никому ничего не расскажу 🤐
Что тебя беспокоит ? """,reply_markup=buttons.cancel)
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
    logging.info("Все отправилось !")
    await message.answer("Ваша <b>проблема</b> была отправлена",parse_mode="HTML",reply_markup=ReplyKeyboardRemove()) # ХТМЛ и удаление кнопки 
                                                                                                                
# Анонимное отправление предложения
@dp.message(Command("suggest"))
async def sendsuggest(message: Message,state: FSMContext):
    await message.answer("""Я никому ничего не расскажу 🤐
Что ты хочешь предложить ? """,reply_markup=buttons.cancel)
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
    logging.info("Все отправилось !")
    await message.answer("Ваше предложение было отправлено",parse_mode="HTML",reply_markup=ReplyKeyboardRemove()) # Удаление клавиатуры для suggest в конце 

"""Айдишки стикеров"""
stick = {
    "morning" : "CAACAgIAAxkBAAISYGdf-KBDq5QYDfcnSiv57WNbLZ7YAAKrEwACY42hSbyVV7zak9ODNgQ",
    "evening" : "CAACAgIAAxkBAAISXGdf-GUof7upMwTkrLmWjFIQVKtHAAINEQACiDrRSMMk8ZZ6ZMfcNgQ"
}

"""Отправление напоминалок нашим сотрудникам , каждый день"""
async def send_morning_cron():
    allkyes = [int(key) for key in Adamarid.keys()]  # Преобразование ключей в int
    j = 0
    failed_users = []

    for i in allkyes:
        try:
            name = Adamarid.get(str(i), "друг")  # Получение имени
            try:
                await bot.send_sticker(i, stick['morning'])
            except Exception as e:
                failed_users.append(f"Ошибка при отправке стикера ID {i}: {e}")
                continue

            try:
                await bot.send_message(
                    i,
                    f"""<b> Доброе утро, <i>{name}</i> 🌞  
Не забудь заполнить утреннюю планерку! 📋  
Начни день с улыбки и вдохновения! 😊✨  
Дедлайн — 11:00. Успеешь? 😉</b>""",
                    parse_mode="HTML"
                )
                j += 1
                await asyncio.sleep(1)  # Увеличенный интервал
            except Exception as e:
                failed_users.append(f"Ошибка при отправке сообщения ID {i}: {e}")
        except Exception as e:
            logging.error(f"Неизвестная ошибка для ID {i}: {e}")

    logging.info(f"Количество отправленных рассылок: {j}")
    if failed_users:
        logging.warning(f"Не удалось отправить сообщения: {failed_users}")





async def send_evening_cron():
    allkyes = [int(key) for key in Adamarid.keys()]  # Преобразование ключей в int
    j = 0
    failed_users = []

    for i in allkyes:  # Цикл по ключам словаря
        try:
            name = Adamarid.get(str(i), "друг")  # Получение имени сотрудника
            
            # Отправка стикера
            try:
                await bot.send_sticker(i, stick['evening'])
            except Exception as e:
                failed_users.append(f"Ошибка при отправке стикера ID {i}: {e}")
                continue  # Пропуск текущей итерации
            
            # Отправка сообщения
            try:
                await bot.send_message(
                    i,
                    f"""<b>Добрый вечер, <i><b>{name}!</b></i> 🌙  
Закончим этот день вместе? Не забудь заполнить вечернюю планерку! 📋  
Расскажи, как всё прошло, и получи от нас респект! 😎👍  
Дедлайн — 20:00. Не откладывай! 😉</b>""",
                    parse_mode="HTML"
                )
                j += 1
                await asyncio.sleep(1)  # Увеличенный интервал между отправками
            except Exception as e:
                failed_users.append(f"Ошибка при отправке сообщения ID {i}: {e}")
        except Exception as e:
            logging.error(f"Неизвестная ошибка для ID {i}: {e}")

    # Логирование результатов
    logging.info(f"Количество отправленных вечерних рассылок: {j}")
    if failed_users:
        logging.warning(f"Не удалось отправить сообщения: {failed_users}")


message_cron = """<b>Не забудь отправить твою планерку! 📋</b>
И <i><b>улыбнись</b></i> пожалуйста ! )) 😁😉
"""

# """Получение id , нового или уже имеющегося сотрудника"""
# @dp.message(F.text)
# async def getidofuser(message: Message):
#     msg = message.text
#     await bot.send_message(7095194058,f"""user-id - <code>{message.from_user.id}</code>\n
# user-name - {message.from_user.username}\n
# self text - <code>{msg}</code>""",parse_mode="HTML")

        

"""Получение id , определенного стикера"""
# @dp.message(F.content_type.in_({'sticker'}))
# async def getid(message: Message):
#     await message.answer(message.sticker.file_id)

# Обработка Даты 
@dp.message(F.text.contains("Дата 📅"))
async def editdate(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["dateofplanerka"]}")
    await state.set_state(Date.date)
# Обработка Даты
@dp.message(Date.date)
async def getdataofdate(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "date" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")
    
# Обработка Времени прихода
@dp.message(F.text.contains("Время прихода 🕰"))
async def edittime(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["arrival_time"]}")
    await state.set_state(Time.time)
# Обработка Времени прихода
@dp.message(Time.time)
async def getdataoftime(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "arrival_time" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")

# Обработка Задачи
@dp.message(F.text.contains("Задачи 📝"))
async def edittasks(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["alltasks"]}")
    await state.set_state(Tasks.tasks)
# Обработка Задачи
@dp.message(Tasks.tasks)
async def getdataoftasks(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "tasks" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")


# Обработка Итоги
@dp.message(F.text.contains("Итоги 🎯"))
async def editresult(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["result"]}")
    await state.set_state(Result.result)
# Обработка Итоги
@dp.message(Result.result)
async def getdataofresults(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "result" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")


# Обработка Проблемы
@dp.message(F.text.contains("Проблемы 👹"))
async def editproblem(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["problems"]}")
    await state.set_state(Problems.problem)
# Обработка Проблемы
@dp.message(Problems.problem)
async def getdataofproblems(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "problems" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")


# Обработка Проблемы
@dp.message(F.text.contains("Комментарии 🗣"))
async def editcomments(message: Message,state : FSMContext):
    await message.answer(f"{QUESTIONS["comments"]}")
    await state.set_state(Comments.comment)
# Обработка Проблемы
@dp.message(Comments.comment)
async def getdataofcomments(message: Message,state: FSMContext):
    data = read_json_file(file_path=file_path)
    msg = message.text
    user_id = message.from_user.id
    update_user_info(str(user_id) , "comments" , new_value=f"{msg}")
    await state.clear()
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")


# Очистка самой планерки
@dp.message(F.text.contains("Очистить планерку 🧹"))
async def cleardataofworker(message: Message,state : FSMContext):
    user_id = message.from_user.id
    clear_user_data(str(user_id) , file_path=file_path)
    await message.answer("Данные очистились!")


# Показ самой планерки 
@dp.message(F.text.contains("Моя планерка 🧾"))
async def showhisplanerka(message: Message,state : FSMContext):
    user_id = message.from_user.id
    summary = get_user_data(user_id , file_path)
    await bot.send_message(user_id, summary,parse_mode="HTML")


# Отправка самой планерки  
@dp.message(F.text.contains("Отправить 📤"))
async def sendyourplanerka(message: Message,state : FSMContext):
    data = read_json_file(file_path=file_path)
    user_id = message.from_user.id
    summary = get_user_data(user_id , file_path)
    user_name  = Adamarid[f"{user_id}"]
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)  # Преобразуем строку JSON в словарь

    # Ищем пользователя по user_id
    users = json_data.get('users', [])
    user = next((user for user in users if user['user_id'] == str(user_id)), None)
    
    if user is None:
        return "Пользователь не найден."
    
    # Формируем итоговое сообщение
    summary = (
        f"📋 <b>{user_name}:</b>\n\n"
        f"📅 Дата планерки: <b>{user.get('date', '-')}</b>\n\n"
        f"⏰ Время прихода: <b>{user.get('arrival_time', '-')}</b>\n\n"
        f"🔴 Задачи: <b>{user.get('tasks', '-')}</b>\n\n"
        f"🟠 Итоги, Что выполнено/Что не выполнено✅❌: <b>{user.get('result', '-')}</b>\n\n"
        f"⚠️ Проблемы: <b>{user.get('problems', '-')}</b>\n\n"
        f"💬 Комментарии: <b>{user.get('comments', '-')}</b>"
    )
    ##################################################################################################
    update_or_create_google_sheet(sheet=sheet, user_name=user_name,data=user) # Сама отправка , самая главная функция 
    # chatidof = -1002130834445
    # -1002130834445_4
    await message.answer(summary,parse_mode="HTML")
    await bot.send_message(chat_id=group,text=summary,parse_mode="HTML",message_thread_id=4)





















async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Bishkek"))
    
    # Добавляем задачу на 18:58 с понедельника по пятницу
    trigger_1 = CronTrigger(hour=10, minute=0, day_of_week="0-4", timezone="Asia/Bishkek")
    scheduler.add_job(send_morning_cron, trigger_1)
    
    # Добавляем задачу на 20:04 с понедельника по пятницу
    trigger_2 = CronTrigger(hour=18, minute=0, day_of_week="0-4", timezone="Asia/Bishkek")
    scheduler.add_job(send_evening_cron, trigger_2)
    # Запускаем планировщик в фоновом режиме
    scheduler.start()

    # Запускаем бота
    await dp.start_polling(bot)


    
if __name__ == "__main__":
    logging.basicConfig(
    level=logging.INFO,  # Уровень логов (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат вывода
    filename='app.log',  # Имя файла для логов
    filemode='a'  # 'a' - добавлять новые логи в файл, 'w' - перезаписывать файл каждый раз
)
    asyncio.run(main()) 

# Комментарии , нужно поменять обратно токен и в .env файлике и в самом начале кода где идет конфигурация ,     
