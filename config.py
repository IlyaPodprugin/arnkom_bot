TOKEN = "1334996670:AAHRRRLw0lujGopuDFLFvX84gL5R7DvD5hA"
chat_id = "0"
greeting = """Здравствуйте, я бот Арнком, Ваш личный помошник.
Ответьте на 5 вопросов и менеджер позвонит Вам с выгодным предложением. 
Если готовы - нажмите на кнопку.
"""
quiz_start_phrase = "Чтож, начнём"
first_question_txt = "Первый вопрос: Когда планируете снять офис?"
second_question_txt = "Второй вопрос: Помещение какой площади вы рассматриваете?"
third_question_txt = "Третий вопрос: На каком этаже должен располагаться офис?"
fourth_question_txt = "Четвёртый вопрос: На какой срок собираетесь въезжать?"
fifth_question_txt = "Пятый вопрос: Какие дополнительные параметры вам нужны?"
something_went_wrong = "Что-то пошло не так. Чтобы начать диалог с ботом заново - отправьте комманду \"/start\""

current_question = ""
first_question_answer = ""
second_question_answer = ""
third_question_answer = ""
fourth_question_answer = ""
fifth_question_answer = ""


# @bot.message_handler(commands=["start"])
# def any_msg(message):
#     greeting_keyboard = types.InlineKeyboardMarkup()
#     ready_button = types.InlineKeyboardButton(text="Готов", callback_data="ready")
#     greeting_keyboard.add(ready_button)
#     bot.send_message(message.chat.id, greeting, reply_markup=greeting_keyboard)
#     global chat_id
#     global current_question
#     chat_id = message.chat.id
#     current_question = "ready"
#     print(current_question)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def start_quiz(call):
#     global current_question
#     if call.data == "ready":
#         global current_question
#         bot.send_message(chat_id, quiz_start_phrase)
#         first_question(call)
#         print(current_question)
#     elif current_question == "first":
#         global first_question_answer
#         first_question_answer = call.data
#         second_question(call)
#         print(current_question, first_question_answer)
#     elif current_question == "second":
#         global second_question_answer
#         second_question_answer = call.data
#         third_question(call)
#         print(current_question, second_question_answer)
#     elif current_question == "third":
#         global third_question_answer
#         third_question_answer = call.data
#         fourth_question(call)
#         print(current_question, third_question_answer)
#     elif current_question == "fourth":
#         global fourth_question_answer
#         fourth_question_answer = call.data
#         fifth_question(call)
#         print(current_question, fourth_question_answer)
#     elif current_question == "fifth":
#         global fifth_question_answer
#         fifth_question_answer = call.data
#         print(current_question, fifth_question_answer)
#     else:
#         bot.send_message(chat_id, something_went_wrong)
#
#
# def first_question(call):
#     global current_question
#     current_question = "first"
#     first_question_keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#     buttons.append(types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"))
#     buttons.append(types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"))
#     buttons.append(types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"))
#     buttons.append(types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет"))
#     first_question_keyboard.add(*buttons)
#     bot.send_message(chat_id, first_question_txt, reply_markup=first_question_keyboard)
#     # global fifth_question_answer
#     # first_question_answer = call.data
#     # print(current_question, first_question_answer)
#
#
# def second_question(call):
#     global current_question
#     current_question = "second"
#     second_question_keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#     buttons.append(types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"))
#     buttons.append(types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"))
#     buttons.append(types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"))
#     buttons.append(types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет"))
#     second_question_keyboard.add(*buttons)
#     bot.send_message(chat_id, first_question_txt, reply_markup=second_question_keyboard)
#     # global second_question_answer
#     # second_question_answer = call.data
#     # print(current_question, second_question_answer)
#
#
# def third_question(call):
#     global current_question
#     current_question = "third"
#     third_question_keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#     buttons.append(types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"))
#     buttons.append(types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"))
#     buttons.append(types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"))
#     buttons.append(types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет"))
#     third_question_keyboard.add(*buttons)
#     bot.send_message(chat_id, first_question_txt, reply_markup=third_question_keyboard)
#     # global third_question_answer
#     # third_question_answer = call.data
#     # print(current_question, third_question_answer)
#
#
# def fourth_question(call):
#     global current_question
#     current_question = "fourth"
#     fourth_question_keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#     buttons.append(types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"))
#     buttons.append(types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"))
#     buttons.append(types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"))
#     buttons.append(types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет"))
#     fourth_question_keyboard.add(*buttons)
#     bot.send_message(chat_id, first_question_txt, reply_markup=fourth_question_keyboard)
#     # global fourth_question_answer
#     # fourth_question_answer = call.data
#     # print(current_question, fourth_question_answer)
#
#
# def fifth_question(call):
#     global current_question
#     current_question = "fifth"
#     fifth_question_keyboard = types.InlineKeyboardMarkup()
#     buttons = []
#     buttons.append(types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"))
#     buttons.append(types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"))
#     buttons.append(types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"))
#     buttons.append(types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет"))
#     fifth_question_keyboard.add(*buttons)
#     bot.send_message(chat_id, first_question_txt, reply_markup=fifth_question_keyboard)
#     # global fifth_question_answer
#     # fifth_question_answer = call.data
#     # print(current_question, fifth_question_answer)
