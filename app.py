import telebot
import config
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


class Question:

    def __init__(self, text, answers, question_type, _row_width_):
        self._row_width_ = _row_width_
        self.keyboard = types.InlineKeyboardMarkup(row_width=self._row_width_)
        self.text = text
        self.answers = answers
        self.question_type = question_type

    def generate_keyboard(self):
        buttons = []
        for i in self.answers:
            buttons.append(types.InlineKeyboardButton(text=i, callback_data=i))
        self.keyboard.add(*buttons)

    def send_generated_message(self):
        bot.send_message(config.chat_id, self.text, reply_markup=self.keyboard)


@bot.message_handler(commands=["start"])
def any_msg(message):
    config.current_question = 1
    config.chat_id = message.chat.id
    config.user_name = f"{message.chat.first_name} {message.chat.last_name}"

    greeting = Question(config.generate_greeting(), ["Поехали"], "select", 1)
    greeting.generate_keyboard()
    greeting.send_generated_message()


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "Поехали":
        question = Question(config.questions[config.current_question]["text"],
                            config.questions[config.current_question]["answers"], "select", 1)
        question.generate_keyboard()
        bot.edit_message_text(
            chat_id=config.chat_id,
            message_id=call.message.message_id,
            text=config.questions[config.current_question]["text"],
            reply_markup=question.keyboard
        )
        config.current_question = 2
    else:
        if call.data == "< Назад>":
            config.current_question -= 1
            # bot.send_message(call.message.chat.id, "The 'Previous question' btn has been pressed")
        elif config.current_question == 2:
            config.answers[config.current_question - 1] = call.data
            question = Question(config.questions[config.current_question]["text"],
                                config.questions[config.current_question]["answers"], "select", 1)
            question.generate_keyboard()
            bot.edit_message_text(
                chat_id=config.chat_id,
                message_id=call.message.message_id,
                text=config.questions[config.current_question]["text"],
                reply_markup=question.keyboard
            )
            config.current_question = 3
        elif config.current_question == 3:
            config.answers[config.current_question - 1] = call.data
            question = Question(config.questions[config.current_question]["text"],
                                config.questions[config.current_question]["answers"], "select", 1)
            question.generate_keyboard()
            bot.edit_message_text(
                chat_id=config.chat_id,
                message_id=call.message.message_id,
                text=config.questions[config.current_question]["text"],
                reply_markup=question.keyboard
            )
            config.current_question = 4
        elif config.current_question == 4:
            config.answers[config.current_question - 1] = call.data
            question = Question(config.questions[config.current_question]["text"],
                                config.questions[config.current_question]["answers"], "select", 1)
            question.generate_keyboard()
            bot.edit_message_text(
                chat_id=config.chat_id,
                message_id=call.message.message_id,
                text=config.questions[config.current_question]["text"],
                reply_markup=question.keyboard
            )
            config.current_question = 5
        elif config.current_question == 5:
            config.answers[config.current_question - 1] = call.data
            question = Question(config.questions[config.current_question]["text"],
                                config.questions[config.current_question]["answers"], "select", 1)
            question.generate_keyboard()
            bot.edit_message_text(
                chat_id=config.chat_id,
                message_id=call.message.message_id,
                text=config.questions[config.current_question]["text"],
                reply_markup=question.keyboard
            )
            config.current_question = 6
        else:
            config.answers[config.current_question - 1] = call.data
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=config.generate_goodbye()
            )


bot.polling()
