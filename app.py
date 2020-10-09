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
    config.current_question = 0
    config.chat_id = message.chat.id
    config.user_name = f"{message.chat.first_name} {message.chat.last_name}"
    config.questions[config.current_question]["text"] = config.generate_greeting()

    greeting = Question(config.generate_greeting(), ["Поехали"], "select", 1)
    greeting.generate_keyboard()
    greeting.send_generated_message()


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["answers"])
def question_message(call):
    if call.data == "< Назад":
        config.current_question -= 1
        question = Question(config.questions[config.current_question]["text"],
                            config.questions[config.current_question]["answers"], "select", 1)
        question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
    if call.data == "Вперёд >" or call.data == "Поехали":
        if config.current_question < 5:
            if config.current_question != 0:
                config.answers[config.current_question] = call.data
            config.current_question += 1
            question = Question(config.questions[config.current_question]["text"],
                                config.questions[config.current_question]["answers"], "select", 1)
            question.generate_keyboard()
            bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                  text=question.text, reply_markup=question.keyboard)
        else:
            config.answers[config.current_question] = call.data
            bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                  text=config.generate_goodbye())


bot.polling()
