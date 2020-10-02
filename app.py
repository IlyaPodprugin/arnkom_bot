import telebot
import config
from telebot import types
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
first_question_keyboard = types.InlineKeyboardMarkup(row_width=2)
first_question_buttons = [
    types.InlineKeyboardButton(text="В течение недели", callback_data="В течение недели"),
    types.InlineKeyboardButton(text="В течение месяца", callback_data="В течение месяца"),
    types.InlineKeyboardButton(text="Через несколько месяцев", callback_data="Через несколько месяцев"),
    types.InlineKeyboardButton(text="Точных ориепнтиров нет", callback_data="Точных ориепнтиров нет")
]
first_question_keyboard.add(*first_question_buttons)

second_question_keyboard = types.InlineKeyboardMarkup(row_width=2)
second_question_buttons = [
    types.InlineKeyboardButton(text="до 40м2", callback_data="до 40м2"),
    types.InlineKeyboardButton(text="40-60м2", callback_data="40-60м2"),
    types.InlineKeyboardButton(text="60-85м2", callback_data="60-85м2"),
    types.InlineKeyboardButton(text="85-120м2", callback_data="85-120м2"),
    types.InlineKeyboardButton(text="Более 120м2", callback_data="Более 120м2"),
    types.InlineKeyboardButton(text="Рассмотрю все варианты", callback_data="Рассмотрю все варианты")
]
second_question_keyboard.add(*second_question_buttons)

third_question_keyboard = types.InlineKeyboardMarkup(row_width=2)
third_question_buttons = [
    types.InlineKeyboardButton(text="1-10 этаж", callback_data="1-10 этаж"),
    types.InlineKeyboardButton(text="10-25 этаж", callback_data="10-25 этаж"),
    types.InlineKeyboardButton(text="25-45 этаж", callback_data="25-45 этаж"),
    types.InlineKeyboardButton(text="45-60 этаж", callback_data="45-60 этаж"),
    types.InlineKeyboardButton(text="Выше 60 этажа", callback_data="Выше 60 этажа"),
    types.InlineKeyboardButton(text="Этаж не важен", callback_data="Этаж не важен")
]
third_question_keyboard.add(*third_question_buttons)

fourth_question_keyboard = types.InlineKeyboardMarkup(row_width=2)
fourth_question_buttons = [
    types.InlineKeyboardButton(text="1 месяц", callback_data="1 месяц"),
    types.InlineKeyboardButton(text="3-6 месяцев", callback_data="3-6 месяцев"),
    types.InlineKeyboardButton(text="6-12 месяцев", callback_data="6-12 месяцев"),
    types.InlineKeyboardButton(text="Более 12 месяцев", callback_data="Более 12 месяцев")
]
fourth_question_keyboard.add(*fourth_question_buttons)


@bot.message_handler(commands=["start"])
def any_msg(message):
    greeting_keyboard = types.InlineKeyboardMarkup()
    ready_button = types.InlineKeyboardButton(text="Пройти тест", callback_data="ready")
    greeting_keyboard.add(ready_button)
    bot.send_message(message.chat.id, config.greeting, reply_markup=greeting_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "ready":
            config.current_question = 1
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.first_question_txt,
                reply_markup=first_question_keyboard
            )
        elif config.current_question == 1:
            config.current_question = 2
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.second_question_txt,
                reply_markup=second_question_keyboard
            )
        elif config.current_question == 2:
            config.current_question = 3
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.third_question_txt,
                reply_markup=third_question_keyboard
            )
        elif config.current_question == 3:
            config.current_question = 4
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.fourth_question_txt,
                reply_markup=fourth_question_keyboard
            )
        # elif config.current_question == 4:
        #     config.current_question = 5
        #     bot.edit_message_text(
        #         chat_id=call.message.chat.id,
        #         message_id=call.message.message_id,
        #         text=config.third_question_txt,
        #         reply_markup=third_question_keyboard
        #     )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.goodbye
            )


bot.polling()
