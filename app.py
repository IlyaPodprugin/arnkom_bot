import telebot
import config
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


class Store:
    messages = []
    questions = [
        {
            "text": "",
            "answers": "",
            "buttons": ["Поехали"]
        },
        {
            "text": "<b>1 из 5:</b> Когда планируете снять офис?",
            "answers": ["В течение недели", "В течение месяца", "Через несколько месяцев",
                        "Точных ориентиров нет"],
            "buttons": ["Назад"]
        },
        {
            "text": "<b>2 из 5:</b> Помещение какой площади вы рассматриваете?",
            "answers": ["до 40м2", "40-60м2", "60-85м2", "85-120м2", "Более 120м2",
                        "Рассмотрю все варианты"],
            "buttons": ["Назад"]
        },
        {
            "text": "<b>3 из 5:</b> На каком этаже должен располагаться офис?",
            "answers": ["1-10 этаж", "10-25 этаж", "25-45 этаж", "45-60 этаж",
                        "Выше 60 этажа", "Этаж не важен"],
            "buttons": ["Назад"]
        },
        {
            "text": "<b>4 из 5:</b> На какой срок собираетесь въезжать?",
            "answers": ["1 месяц", "3-6 месяцев", "6-12 месяцев",
                        "Более 12 месяцев"],
            "buttons": ["Назад"]
        },
        {
            "text": "<b>5 из 5:</b> Какие дополнительные параметры вам нужны?",
            "answers": ["Вид на город", "Скидка на паркинг", "Без ремонта", "Интернет по Wi-Fi",
                        "Наличие мебели", "Возможность установки перегородок"],
            "buttons": ["Назад", "Вперёд"]
        }
    ]

    def __init__(self):
        self.chat_id = ""
        self.current_question = 0
        self.user_name = ""

        self.user_answers = {
            1: "",
            2: "",
            3: "",
            4: "",
            5: [],
        }

    # This func gets data from the database and rewrites the "question" variable to use it when work with keyboards
    def get_questions(self):
        pass

    def get_user(self):
        pass

    def set_user(self):
        pass

    def inc_question(self):
        self.current_question += 1

    def dec_question(self):
        self.current_question -= 1

    def edit_message(self):
        pass


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

    def get_info(self):
        pass

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
Current question: {store.current_question}
---------------------------------------------------------------\n""")

    def send_generated_message(self):
        bot.send_message(store.chat_id, self.text, reply_markup=self.keyboard)


store = Store()
question = Question("select",
                    store.questions[store.current_question]["text"],
                    store.questions[store.current_question]["buttons"],
                    store.questions[store.current_question]["answers"])

# print(question.check())


@bot.message_handler(commands=["start"])
def start_msg(message):
    store.current_question = 0
    store.chat_id = message.chat.id
    store.user_name = f"{message.chat.first_name} {message.chat.last_name}"
    greeting = f"""
Здравствуйте, {store.user_name}, я <b>Бот Арнком</b>, Ваш личный помощник.\n
Ответьте на <b>5 вопросов</b> и менеджер подберёт <b>идеально подходящее Вам</b> предложение.\n
Если готовы - <b>нажмите на кнопку</b>.
    """

    question.text = greeting
    question.buttons = store.questions[store.current_question]["buttons"]
    question.answers = []
    question.call_data = []
    question.question_type = "select"
    question.keyboard = question.generate_keyboard()
    question.send_generated_message()
    print(f"message: {message}")
    # print(question.check())


@bot.callback_query_handler(lambda call: call.data in store.questions[store.current_question]["buttons"])
def buttons_callback(call):
    if call.data == "Назад":
        store.current_question -= 1
    elif call.data == "Поехали":
        store.current_question += 1
    elif call.data == "Вперёд":
        if store.user_answers[store.current_question] == "":
            bot.answer_callback_query(callback_query_id=call.id, text=config.didnt_pick, show_alert=True)
            return
        else:
            bot.edit_message_text(chat_id=store.chat_id, message_id=call.message.message_id,
                                  text=config.generate_goodbye())
            print(f"call.message: {call.message}")
            # print(question.check())
            return

    if store.current_question != 0:
        question.question_type = "select"
        question.call_data = store.user_answers[store.current_question]
        question.text = store.questions[store.current_question]["text"]
        question.buttons = store.questions[store.current_question]["buttons"]
        question.answers = store.questions[store.current_question]["answers"]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=store.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(f"call.message: {call.message}")
        # print(question.check())
    else:
        question.text = config.greeting
        question.buttons = store.questions[store.current_question]["buttons"]
        question.answers = []
        question.call_data = []
        question.question_type = "select"
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=store.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(f"call.message: {call.message}")
        # print(question.check())


@bot.callback_query_handler(lambda call: call.data in store.questions[store.current_question]["answers"])
def answers_callback(call):
    if store.current_question == 5:

        # Adding and remove picked and unpicked answers from a list
        if call.data in store.user_answers[store.current_question]:
            store.user_answers[store.current_question].remove(call.data)
        else:
            store.user_answers[store.current_question].append(call.data)

        question.call_data = store.user_answers[store.current_question]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=store.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(f"call.message: {call.message}")
    else:
        store.user_answers[store.current_question] = call.data
        store.current_question += 1
        if store.current_question == 5:
            question.question_type = "checkbox"
        else:
            question.question_type = "select"

        question.call_data = call.data
        question.text = store.questions[store.current_question]["text"]
        question.buttons = store.questions[store.current_question]["buttons"]
        question.answers = store.questions[store.current_question]["answers"]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=store.chat_id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)
        print(f"call.message: {call.message}")
        # print(question.check())


if __name__ == "__main__":
    bot.infinity_polling()
