import telebot
import config
from telebot import types


bot = telebot.TeleBot(config.TOKEN)


class Question:
    def __init__(self, chat_id, text, answers, question_type, row_width):
        # self.keyboard_name = keyboard_name
        self.row_width = row_width
        self.chat_id = chat_id
        self.text = text
        self.answers = answers
        self.question_type = question_type

    def generate_message(self):
        keyboard = types.InlineKeyboardMarkup(row_width=self.row_width)
        buttons = []
        for i in self.answers:
            buttons.append(types.InlineKeyboardButton(text=i, callback_data=i))
        keyboard.add(*buttons)
        bot.send_message(self.chat_id, self.text, parse_mode="HTML", reply_markup=keyboard)


# @bot.message_handler(commands="start")
# def send_message(message):
#     first_question = QuestionGenerator(message.chat.id,
#                                        "To be or not to be?",
#                                        4,
#                                        ["to be", "not to be", "be to", "be to not"],
#                                        "select",
#                                        1
#                                        )
#     first_question.generate_message()
    # print(type(first_question.keyboard), first_question)
    # print(first_question.text, first_question.num_of_answers, first_question.answers, first_question.question_type)

# first_question_keyboard1 = types.InlineKeyboardMarkup(row_width=1)
# first_question_buttons1 = [
#     types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"),
#     types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"),
#     types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"),
#     types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет")
# ]
# first_question_keyboard1.add(*first_question_buttons1)
# print(first_question_keyboard1, "first_question_keyboard1")
#
# second_question_keyboard = types.InlineKeyboardMarkup(row_width=1)
# second_question_buttons = [
#     types.InlineKeyboardButton(text="до 40м2", callback_data="до 40м2"),
#     types.InlineKeyboardButton(text="40-60м2", callback_data="40-60м2"),
#     types.InlineKeyboardButton(text="60-85м2", callback_data="60-85м2"),
#     types.InlineKeyboardButton(text="85-120м2", callback_data="85-120м2"),
#     types.InlineKeyboardButton(text="Более 120м2", callback_data="Более 120м2"),
#     types.InlineKeyboardButton(text="Рассмотрю все варианты", callback_data="Рассмотрю все варианты"),
#     types.InlineKeyboardButton(text="🔙 Предыдущий вопрос", callback_data="previous")
# ]
# second_question_keyboard.add(*second_question_buttons)
#
# third_question_keyboard = types.InlineKeyboardMarkup(row_width=1)
# third_question_buttons = [
#     types.InlineKeyboardButton(text="1-10 этаж", callback_data="1-10 этаж"),
#     types.InlineKeyboardButton(text="10-25 этаж", callback_data="10-25 этаж"),
#     types.InlineKeyboardButton(text="25-45 этаж", callback_data="25-45 этаж"),
#     types.InlineKeyboardButton(text="45-60 этаж", callback_data="45-60 этаж"),
#     types.InlineKeyboardButton(text="Выше 60 этажа", callback_data="Выше 60 этажа"),
#     types.InlineKeyboardButton(text="Этаж не важен", callback_data="Этаж не важен"),
#     types.InlineKeyboardButton(text="Предыдущий вопрос", callback_data="previous")
# ]
# third_question_keyboard.add(*third_question_buttons)
#
# fourth_question_keyboard = types.InlineKeyboardMarkup(row_width=1)
# fourth_question_buttons = [
#     types.InlineKeyboardButton(text="1 месяц", callback_data="1 месяц"),
#     types.InlineKeyboardButton(text="3-6 месяцев", callback_data="3-6 месяцев"),
#     types.InlineKeyboardButton(text="6-12 месяцев", callback_data="6-12 месяцев"),
#     types.InlineKeyboardButton(text="Более 12 месяцев", callback_data="Более 12 месяцев"),
#     types.InlineKeyboardButton(text="Предыдущий вопрос", callback_data="previous")
# ]
# fourth_question_keyboard.add(*fourth_question_buttons)

# Сделать возможность делать кастомный callback_data
# Осуществить это можно так:
# В функцию в качестве параметра передаётся массив словарей, где значение - текст сообщение, а ключ - callback_data
@bot.message_handler(commands=["start"])
def any_msg(message):
    config.chat_id = message.chat.id
    config.user_name = f"{message.chat.first_name} {message.chat.last_name}"
    greeting = Question(config.chat_id, config.generate_greeting(), config.first_question_answers, "select", 1)
    first_question = Question(config.chat_id, config.generate_greeting(),
                                       config.first_question_answers, "select", 1)
    greeting.generate_message()


# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     if call.data == "ready":
#         config.current_question = 1
#         bot.edit_message_text(
#             chat_id=call.message.chat.id,
#             message_id=call.message.message_id,
#             text=config.first_question_txt,
#             reply_markup=first_question_keyboard
#         )
#     else:
#         if call.data == "previous":
#             config.current_question -= 1
#             # bot.send_message(call.message.chat.id, "The 'Previous question' btn has been pressed")
#         elif config.current_question == 1:
#             config.first_question_answer = call.data
#             config.current_question = 2
#             bot.edit_message_text(
#                 chat_id=call.message.chat.id,
#                 message_id=call.message.message_id,
#                 text=config.second_question_txt,
#                 reply_markup=second_question_keyboard
#             )
#         elif config.current_question == 2:
#             config.second_question_answer = call.data
#             config.current_question = 3
#             bot.edit_message_text(
#                 chat_id=call.message.chat.id,
#                 message_id=call.message.message_id,
#                 text=config.third_question_txt,
#                 reply_markup=third_question_keyboard
#             )
#         elif config.current_question == 3:
#             config.third_question_answer = call.data
#             config.current_question = 4
#             bot.edit_message_text(
#                 chat_id=call.message.chat.id,
#                 message_id=call.message.message_id,
#                 text=config.fourth_question_txt,
#                 reply_markup=fourth_question_keyboard
#             )
#         else:
#             config.fourth_question_answer = call.data
#             bot.edit_message_text(
#                 chat_id=call.message.chat.id,
#                 message_id=call.message.message_id,
#                 text=config.generate_goodbye()
#             )


bot.polling()
