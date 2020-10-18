import telebot
import config
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


class Question:

    def __init__(self, question_type, text, buttons, answers=None, call_data=None):
        self.text = text
        self.question_type = question_type

        self.keyboard = types.InlineKeyboardMarkup()
        self.buttons = buttons

        self.answers = [] if answers is None else answers
        self.call_data = [] if call_data is None else call_data

    def generate_keyboard(self):
        self.keyboard.keyboard.clear()
        buttons_row = []
        if len(self.answers) == 0:
            pass
        else:
            if self.question_type == "select":
                for i in self.answers:
                    if i == self.call_data:
                        row = list()
                        row.append(types.InlineKeyboardButton(text=f"\U0001F518 {i}", callback_data=i))
                        self.keyboard.add(*row)
                    else:
                        row = list()
                        row.append(types.InlineKeyboardButton(text=f"\U000026AA {i}", callback_data=i))
                        self.keyboard.add(*row)
            elif self.question_type == "checkbox":
                for i in self.answers:
                    if i in self.call_data:
                        row = list()
                        row.append(types.InlineKeyboardButton(text=f"\U00002705 {i}", callback_data=i))
                        self.keyboard.add(*row)
                    else:
                        row = list()
                        row.append(types.InlineKeyboardButton(text=f"\U00002B1C {i}", callback_data=i))
                        self.keyboard.add(*row)
        for i in self.buttons:
            buttons_row.append(types.InlineKeyboardButton(text=i, callback_data=i))
        self.keyboard.add(*buttons_row)
        print()
        return self.keyboard

    def send_generated_message(self):
        bot.send_message(config.chat_id, self.text, reply_markup=self.keyboard)


question = Question("select",
                    config.questions[config.current_question]["text"],
                    config.questions[config.current_question]["buttons"],
                    config.questions[config.current_question]["answers"])


@bot.message_handler(commands=["start"])
def any_msg(message):
    config.current_question = 0
    config.chat_id = message.chat.id
    config.user_name = f"{message.chat.first_name} {message.chat.last_name}"
    greeting = f"""
Здравствуйте, {config.user_name}, я <b>Бот Арнком</b>, Ваш личный помощник.\n
Ответьте на <b>5 вопросов</b> и менеджер подберёт <b>идеально подходящее Вам</b> предложение.\n
Если готовы - <b>нажмите на кнопку</b>.
    """

    question.text = greeting
    question.buttons = config.questions[config.current_question]["buttons"]
    question.keyboard = question.generate_keyboard()
    question.send_generated_message()


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["buttons"])
def buttons_callback(call):
    if call.data == "< Назад":
        config.current_question -= 1
    elif call.data == "Поехали":
        config.current_question += 1
        bot.answer_callback_query(callback_query_id=call.id, text=config.hint_message, show_alert=True)
    elif call.data == "Вперёд >":
        if config.user_answers[config.current_question] != "":
            if config.current_question < 5:
                config.current_question += 1
                if config.current_question == 5:
                    question.question_type = "checkbox"
            else:
                bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                      text=config.generate_goodbye())
                return
        else:
            bot.answer_callback_query(callback_query_id=call.id, text=config.didnt_pick, show_alert=True)
            return

    question.text = config.questions[config.current_question]["text"]
    question.buttons = config.questions[config.current_question]["buttons"]
    question.answers = config.questions[config.current_question]["answers"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["answers"])
def answers_callback(call):
    if config.current_question == 5:
        question.question_type = "checkbox"
        if call.data in config.user_answers[config.current_question]:
            config.user_answers[config.current_question].remove(call.data)
        else:
            config.user_answers[config.current_question].append(call.data)

        question.call_data = config.user_answers[config.current_question]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
    else:
        if call.data in config.user_answers[config.current_question]:
            return
        else:
            config.user_answers[config.current_question] = call.data
            question.call_data = call.data
            question.keyboard = question.generate_keyboard()
            bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                  text=question.text, reply_markup=question.keyboard)


bot.polling()
