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
        self.btn_row = []
        self.answer_row = []

        self.answers = [] if answers else answers
        self.call_data = [] if call_data else call_data

    def generate_keyboard(self):
        self.keyboard.keyboard.clear()
        self.btn_row.clear()
        self.answer_row.clear()
        print("Check:\n" + self.check())
        if len(self.answers) == 0:
            pass
        else:
            if self.question_type == "select":
                for i in self.answers:
                    if i == self.call_data:
                        self.answer_row.append(types.InlineKeyboardButton(text=f"\U0001F518 {i}", callback_data=i))
                        self.keyboard.add(*self.answer_row)
                        self.answer_row.clear()
                    else:
                        self.answer_row.append(types.InlineKeyboardButton(text=f"\U000026AA {i}", callback_data=i))
                        self.keyboard.add(*self.answer_row)
                        self.answer_row.clear()
                self.btn_row.append(types.InlineKeyboardButton(text=f"\U000021A9 {self.buttons[0]}", callback_data=self.buttons[0]))
                self.keyboard.add(*self.btn_row)
                return self.keyboard

            elif self.question_type == "checkbox":
                for i in self.answers:
                    if i in self.call_data:
                        self.answer_row.append(types.InlineKeyboardButton(text=f"\U00002705 {i}", callback_data=i))
                        self.keyboard.add(*self.answer_row)
                        self.answer_row.clear()
                    else:
                        self.answer_row.append(types.InlineKeyboardButton(text=f"\U00002B1C {i}", callback_data=i))
                        self.keyboard.add(*self.answer_row)
                        self.answer_row.clear()
                for i in self.buttons:
                    if i == "Вперёд":
                        self.btn_row.append(types.InlineKeyboardButton(text=f"\U000021AA {i}", callback_data=i))
                    elif i == "Назад":
                        self.btn_row.append(types.InlineKeyboardButton(text=f"\U000021A9 {i}", callback_data=i))
                self.keyboard.add(*self.btn_row)
                return self.keyboard
        self.btn_row.append(types.InlineKeyboardButton(text=self.buttons[0], callback_data=self.buttons[0]))
        self.keyboard.add(*self.btn_row)
        return self.keyboard

    def check(self):
        return (f"""---------------------------------------------------------------
Type: {self.question_type}
Answers: {self.answers}
Call data: {self.call_data}
Buttons: {self.btn_row}
Answer row: {self.answer_row}
Keyboard: {self.keyboard}
Keyboard components: {self.keyboard.keyboard}
Current qstn: {config.current_question}
---------------------------------------------------------------\n""")

    def send_generated_message(self):
        bot.send_message(config.chat_id, self.text, reply_markup=self.keyboard)


question = Question("select",
                    config.questions[config.current_question]["text"],
                    config.questions[config.current_question]["buttons"],
                    config.questions[config.current_question]["answers"])

print(question.check())


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
    question.answers = []
    question.call_data = []
    question.question_type = "select"
    question.keyboard = question.generate_keyboard()
    question.send_generated_message()
    print(question.check())


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["buttons"])
def buttons_callback(call):
    if call.data == "Назад":
        config.current_question -= 1
    elif call.data == "Поехали":
        config.current_question += 1
    elif call.data == "Вперёд":
        if config.user_answers[config.current_question] == "":
            bot.answer_callback_query(callback_query_id=call.id, text=config.didnt_pick, show_alert=True)
            return
        else:
            bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                                  text=config.generate_goodbye())
            print(question.check())
            return

    if config.current_question != 0:
        question.question_type = "select"
        question.call_data = config.user_answers[config.current_question]
        question.text = config.questions[config.current_question]["text"]
        question.buttons = config.questions[config.current_question]["buttons"]
        question.answers = config.questions[config.current_question]["answers"]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(question.check())
    else:
        question.text = config.greeting
        question.buttons = config.questions[config.current_question]["buttons"]
        question.answers = []
        question.call_data = []
        question.question_type = "select"
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(question.check())


@bot.callback_query_handler(lambda call: call.data in config.questions[config.current_question]["answers"])
def answers_callback(call):
    if config.current_question == 5:

        # Adding and remove picked and unpicked answers from a list
        if call.data in config.user_answers[config.current_question]:
            config.user_answers[config.current_question].remove(call.data)
        else:
            config.user_answers[config.current_question].append(call.data)

        question.call_data = config.user_answers[config.current_question]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
    else:
        config.user_answers[config.current_question] = call.data
        config.current_question += 1
        if config.current_question == 5:
            question.question_type = "checkbox"
        else:
            question.question_type = "select"

        question.call_data = call.data
        question.text = config.questions[config.current_question]["text"]
        question.buttons = config.questions[config.current_question]["buttons"]
        question.answers = config.questions[config.current_question]["answers"]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=config.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(question.check())


bot.infinity_polling()