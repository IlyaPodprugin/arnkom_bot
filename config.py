chat_id = ""
user_name = ""

current_question = 0
goodbye = "git"
greeting = ""
something_went_wrong = "Что-то пошло не так. Чтобы начать диалог с ботом заново - отправьте комманду \"/start\""


def generate_greeting():
    global greeting
    greeting = f"""<b>Здравствуйте</b>, {user_name}, я бот Арнком, Ваш личный помощник.
Ответьте на 5 вопросов и менеджер позвонит Вам с выгодным предложением. 
Если готовы - нажмите на кнопку.
"""
    return greeting


def generate_goodbye():
    global goodbye
    goodbye = f"""1. {answers[1]}
2. {answers[2]}
3. {answers[3]}
4. {answers[4]}
5. {answers[5]}"""
    return goodbye


questions = {
    0: {
        "text": "",
        "answers": ["Поехали"]
    },
    1: {
        "text": "1. Когда планируете снять офис?",
        "answers": ["В течение недели", "В течение месяца", "Через несколько месяцев",
                    "Точных ориепнтиров нет", "Вперёд >"]
    },
    2: {
        "text": "2. Помещение какой площади вы рассматриваете?",
        "answers": ["до 40м2", "40-60м2", "60-85м2", "85-120м2", "Более 120м2",
                    "Рассмотрю все варианты", "< Назад", "Вперёд >"]
    },
    3: {
        "text": "3. На каком этаже должен располагаться офис?",
        "answers": ["1-10 этаж", "10-25 этаж", "25-45 этаж", "45-60 этаж",
                    "Выше 60 этажа", "Этаж не важен", "< Назад", "Вперёд >"]
    },
    4: {
        "text": "4. На какой срок собираетесь въезжать?",
        "answers": ["1 месяц", "3-6 месяцев", "6-12 месяцев",
                    "Более 12 месяцев", "< Назад", "Вперёд >"]
    },
    5: {
        "text": "5. Какие дополнительные параметры вам нужны?",
        "answers": ["Вид на город", "Скидка на паркинг", "Без ремонта", "Интернет по Wi-Fi",
                    "Наличие мебели", "Возможность установки перегородок", "< Назад", "Вперёд >"]
    }
}

answers = {}
