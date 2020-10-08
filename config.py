TOKEN = "1334996670:AAHRRRLw0lujGopuDFLFvX84gL5R7DvD5hA"
chat_id = ""

current_question = 0
first_question_answer = ""
second_question_answer = ""
third_question_answer = ""
fourth_question_answer = ""
fifth_question_answer = ""
first_question_answers = ["В течение недели", "В течение месяца", "Через несколько месяцев", "Точных ориепнтиров нет"]
goodbye = ""
user_name = ""

greeting = ""
quiz_start_phrase = "Чтож, начнём"
first_question_txt = "Первый вопрос: Когда планируете снять офис?"
second_question_txt = "Второй вопрос: Помещение какой площади вы рассматриваете?"
third_question_txt = "Третий вопрос: На каком этаже должен располагаться офис?"
fourth_question_txt = "Четвёртый вопрос: На какой срок собираетесь въезжать?"
fifth_question_txt = "Пятый вопрос: Какие дополнительные параметры вам нужны?"
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
    goodbye = f"""1. {first_question_answer}
2. {second_question_answer}
3. {third_question_answer}
4. {fourth_question_answer}"""
    return goodbye
