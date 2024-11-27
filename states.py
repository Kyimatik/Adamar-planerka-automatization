from aiogram.fsm.state import StatesGroup , State
#Получение данных 
class PlanerkaStates(StatesGroup):
    dateofplanerka = State() # Дата самой планерки или дня 
    arrival_time = State()# время прихода 
    urgent_tasks = State()# срочные задачи 
    important_tasks = State()# важные задачи 
    additional_tasks = State()# доп задачи 
    result = State() # результат
    problems = State() # проблемы
    comments = State() # комы 
    confirm = State() # Подтверждение 
# Получение текста для рассылки Сотрудникам
class Send(StatesGroup):
    allinfo = State() # инфа которую будем рассылать 
# Получение беспокойства любого сотрудника 
class Problem(StatesGroup):
    problemtext = State() # Проблема которую отправляем в базу 
class Suggest(StatesGroup):
    suggesttext = State() # Предложение которую отправляем в базу 


# Вопрсоы , на каждом этапе получения информации 
QUESTIONS = {
    "dateofplanerka" : "Напишите дату",
    "arrival_time": "Во сколько вы пришли?",
    "urgent_tasks": "Срочные задачи",
    "important_tasks": "Важные задачи",
    "additional_tasks": "Не срочные задачи",
    "result" : "Итоги дня",
    "problems": "Возникли ли у вас проблемы? Если да, опишите их.",
    "comments": "Есть ли комментарии или заметки?",
    "confirm" : "Точно отправлять вашу планерку ? "
}
    