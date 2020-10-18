chat_id = ""
user_name = ""

current_question = 0
goodbye = ""
greeting = ""
something_went_wrong = "Что-то пошло не так. Чтобы начать диалог с ботом заново - отправьте комманду \"/start\""
didnt_pick = "Вы ничего не выбрали. Выберите вариант, подходящий Вам и нажмите кнопку \"Вперёд\""
hint_message = """Чтобы перейти к следующему вопросу, выберите подходящий вам вариант 
ответа и нажмите кнопку \"Вперёд >\". Чтобы вернуться назад - нажмите кнопку \"< Назад\"."""


def generate_goodbye():
    global goodbye
    goodbye = f"""Итак, вот что Вы выбрали:
1. <b>Когда?</b> {user_answers[1]}
2. <b>Площадь?</b> {user_answers[2]}
3. <b>Этаж?</b> {user_answers[3]}
4. <b>На какой срок?</b> {user_answers[4]}
5. <b>Дополнительные параметры?</b>
{user_answers[5]}\n

Ваши ответы были отправлены менеджеру. Он уже ищет подходящее Вам предложение.
Спасибо за уделённое время, Бот Арнком"""
    return goodbye


questions = [
    {
        "text": "",
        "answers": "",
        "buttons": ["Поехали"]
    },
    {
        "text": "<b>1 из 5:</b> Когда планируете снять офис?",
        "answers": ["В течение недели", "В течение месяца", "Через несколько месяцев",
                    "Точных ориентиров нет"],
        "buttons": ["Вперёд >"]
    },
    {
        "text": "<b>2 из 5:</b> Помещение какой площади вы рассматриваете?",
        "answers": ["до 40м2", "40-60м2", "60-85м2", "85-120м2", "Более 120м2",
                    "Рассмотрю все варианты"],
        "buttons": ["< Назад", "Вперёд >"]
    },
    {
        "text": "<b>3 из 5:</b> На каком этаже должен располагаться офис?",
        "answers": ["1-10 этаж", "10-25 этаж", "25-45 этаж", "45-60 этаж",
                    "Выше 60 этажа", "Этаж не важен"],
        "buttons": ["< Назад", "Вперёд >"]
    },
    {
        "text": "<b>4 из 5:</b> На какой срок собираетесь въезжать?",
        "answers": ["1 месяц", "3-6 месяцев", "6-12 месяцев",
                    "Более 12 месяцев"],
        "buttons": ["< Назад", "Вперёд >"]
    },
    {
        "text": "<b>5 из 5:</b> Какие дополнительные параметры вам нужны?",
        "answers": ["Вид на город", "Скидка на паркинг", "Без ремонта", "Интернет по Wi-Fi",
                    "Наличие мебели", "Возможность установки перегородок"],
        "buttons": ["< Назад", "Вперёд >"]
    }
]

user_answers = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: [],
}
