import telebot
import config
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


class Question:

    def __init__(self, question_type, text, buttons, answers=None, call_data=None):
        self.keyboard = types.InlineKeyboardMarkup()
        self.text = text
        if answers is not None:
            self.answers = answers
        else:
            self.answers = []
        if call_data is not None:
            self.call_data = call_data
        else:
            self.call_data = []
        self.buttons = buttons
        self.question_type = question_type

    def generate_keyboard(self):
        buttons_row = []
        if len(self.answers) == 0:
            pass
        else:
            for i in self.answers:
                if i == self.call_data:
                    row = list()
                    row.append(types.InlineKeyboardButton(text="* " + i, callback_data=i))
                    self.keyboard.add(*row)
                else:
                    row = list()
                    row.append(types.InlineKeyboardButton(text=i, callback_data=i))
                    self.keyboard.add(*row)
        for i in self.buttons:
            buttons_row.append(types.InlineKeyboardButton(text=i, callback_data=i))
        self.keyboard.add(*buttons_row)

    def send_generated_message(self):
        bot.send_message(config.chat_id, self.text, reply_markup=self.keyboard)


@bot.message_handler(commands=["start"])
def any_msg(message):
    config.current_question = 0
    config.chat_id = message.chat.id
    config.user_name = f"{message.chat.first_name} {message.chat.last_name}"
    config.questions[config.current_question]["text"] = config.generate_greeting()

    greeting = Question("select", config.generate_greeting(), ["Поехали"])
    greeting.generate_keyboard()
    greeting.send_generated_message()


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["buttons"])
def buttons_callback(call):
    if call.data == "< Назад":
        config.current_question -= 1
    elif call.data == "Вперёд >" or call.data == "Поехали":
        if config.current_question < 5:
            config.current_question += 1
        else:
            bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                  text=config.generate_goodbye())
            return

    question = Question("select",
                        config.questions[config.current_question]["text"],
                        config.questions[config.current_question]["buttons"],
                        config.questions[config.current_question]["answers"])
    question.generate_keyboard()
    bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["answers"])
def answers_callback(call):
    if call.data in config.answers[config.current_question]:
        return
    else:
        config.answers[config.current_question] = call.data
        question = Question("select",
                            config.questions[config.current_question]["text"],
                            config.questions[config.current_question]["buttons"],
                            config.questions[config.current_question]["answers"],
                            call.data)
        question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)


bot.polling()
