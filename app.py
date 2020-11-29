import telebot
import config
import os
from dotenv import load_dotenv
from telebot import types

load_dotenv()

bot = telebot.TeleBot(os.environ.get("BOT_TOKEN"), parse_mode="HTML")


class Store:
    questions = [
        {
            "type": "",
            "text": "",
            "answers": "",
            "buttons": ["Поехали"]
        },
        {
            "type": "select",
            "text": "<b>1 из 5:</b> Когда планируете снять офис?",
            "answers": ["В течение недели", "В течение месяца", "Через несколько месяцев",
                        "Точных ориентиров нет"],
            "buttons": []
        },
        {
            "type": "select",
            "text": "<b>2 из 5:</b> Помещение какой площади вы рассматриваете?",
            "answers": ["до 40м2", "40-60м2", "60-85м2", "85-120м2", "Более 120м2",
                        "Рассмотрю все варианты"],
            "buttons": []
        },
        {
            "type": "select",
            "text": "<b>3 из 5:</b> На каком этаже должен располагаться офис?",
            "answers": ["1-10 этаж", "10-25 этаж", "25-45 этаж", "45-60 этаж",
                        "Выше 60 этажа", "Этаж не важен"],
            "buttons": []
        },
        {
            "type": "select",
            "text": "<b>4 из 5:</b> На какой срок собираетесь въезжать?",
            "answers": ["1 месяц", "3-6 месяцев", "6-12 месяцев",
                        "Более 12 месяцев"],
            "buttons": []
        },
        {
            "type": "checkbox",
            "text": "<b>5 из 5:</b> Какие дополнительные параметры вам нужны?",
            "answers": ["Вид на город", "Скидка на паркинг", "Без ремонта", "Интернет по Wi-Fi",
                        "Наличие мебели", "Возможность установки перегородок"],
            "buttons": ["Вперёд"]
        }
    ]

    users = []

    def __init__(self):
        self.chat_id = ""
        self.current_question = 0
        self.user_name = ""

    # This func gets data from the database and rewrites the "question" variable to use it when work with keyboards
    def get_questions(self):
        pass

    def get_user(self, chat_id):
        for item in store.users:
            if chat_id == item["chat_id"]:
                return item
            else:
                return None

    def set_user(self, message):
        if message.from_user.first_name is None or message.from_user.last_name is None:
            if message.from_user.first_name is None:
                user_name = message.from_user.username
            else:
                user_name = message.from_user.first_name
        else:
            user_name = f"{message.from_user.first_name} {message.from_user.last_name}"

        new_user = {
            "chat_id": message.chat.id,
            "user_name": user_name,
            "mobile_phone": "",
            "user_answers": {}
        }
        store.users.append(new_user)
        return new_user

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

        self.answers = [] if answers is None else answers
        self.call_data = [] if call_data is None else call_data

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

    def send_generated_message(self, chat_id):
        bot.send_message(chat_id, self.text, reply_markup=self.keyboard)


store = Store()
question = Question("select",
                    store.questions[store.current_question]["text"],
                    store.questions[store.current_question]["buttons"],
                    store.questions[store.current_question]["answers"])


@bot.message_handler(commands=["start"])
def start_msg(message):
    user = store.get_user(message.chat.id)
    if user is None:
        user = store.set_user(message)

    chat_id = user["chat_id"]
    user_name = user["user_name"]

    greeting = f"""
Здравствуйте, {user_name}, я <b>Бот Арнком</b>, Ваш личный помощник.\n
Ответьте на <b>5 вопросов</b> и менеджер подберёт <b>идеально подходящее Вам</b> предложение.\n
Если готовы - <b>нажмите на кнопку</b>.
    """

    store.current_question = 0
    question.text = greeting
    question.buttons = store.questions[0]["buttons"]
    question.answers = []
    question.call_data = []
    question.question_type = "select"
    question.keyboard = question.generate_keyboard()
    question.send_generated_message(chat_id)
    print(f"message: {message}")
    print(question.check())
    print(store.users)
    bot.register_next_step_handler_by_chat_id(message.chat.id, process_0_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[0]["buttons"])
def process_0_question(call):
    store.current_question = 1
    question.text = store.questions[1]["text"]
    question.answers = store.questions[1]["answers"]
    question.buttons = store.questions[1]["buttons"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)
    print(f"call: {call}")
    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_1_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[1]["answers"])
def process_1_question(call):
    store.current_question = 2
    user = store.get_user(call.message.chat.id)
    user_ind = store.users.index(user)
    store.users[user_ind]["user_answers"][1] = call.data

    question.question_type = "select"
    question.text = store.questions[2]["text"]
    question.answers = store.questions[2]["answers"]
    question.buttons = store.questions[2]["buttons"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)

    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_2_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[2]["answers"])
def process_2_question(call):
    store.current_question = 3
    user = store.get_user(call.message.chat.id)
    user_ind = store.users.index(user)
    store.users[user_ind]["user_answers"][2] = call.data

    question.question_type = "select"
    question.text = store.questions[3]["text"]
    question.answers = store.questions[3]["answers"]
    question.buttons = store.questions[3]["buttons"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)

    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_3_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[3]["answers"])
def process_3_question(call):
    store.current_question = 4
    user = store.get_user(call.message.chat.id)
    user_ind = store.users.index(user)
    store.users[user_ind]["user_answers"][3] = call.data

    question.question_type = "select"
    question.text = store.questions[4]["text"]
    question.answers = store.questions[4]["answers"]
    question.buttons = store.questions[4]["buttons"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)

    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_4_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[4]["answers"])
def process_4_question(call):
    store.current_question = 5
    user = store.get_user(call.message.chat.id)
    user_ind = store.users.index(user)
    store.users[user_ind]["user_answers"][4] = call.data

    question.question_type = "checkbox"
    question.text = store.questions[5]["text"]
    question.answers = store.questions[5]["answers"]
    question.buttons = store.questions[5]["buttons"]
    question.keyboard = question.generate_keyboard()
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=question.text, reply_markup=question.keyboard)

    bot.register_next_step_handler_by_chat_id(call.message.chat.id, process_5_question)


@bot.callback_query_handler(lambda call: call.data in store.questions[5]["answers"]
                            or call.data in store.questions[5]["buttons"])
def process_5_question(call):
    user = store.get_user(call.message.chat.id)
    user_ind = store.users.index(user)

    if call.data in store.questions[5]["buttons"]:
        goodbye = f"""Итак, вот что Вы выбрали:
1. <b>Когда?</b> {store.users[user_ind]["user_answers"][1]}
2. <b>Площадь?</b> {store.users[user_ind]["user_answers"][2]}
3. <b>Этаж?</b> {store.users[user_ind]["user_answers"][3]}
4. <b>На какой срок?</b> {store.users[user_ind]["user_answers"][4]}
5. <b>Дополнительные параметры?</b>
{store.users[user_ind]["user_answers"][5]}\n

Ваши ответы были отправлены менеджеру. Он уже ищет подходящее Вам предложение.
Спасибо за уделённое время, Бот Арнком"""
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=goodbye, reply_markup=None)
        print(store.users)
    else:
        # Adding and remove picked and unpicked answers from a list
        if store.users[user_ind]["user_answers"].get(5):
            if call.data in store.users[user_ind]["user_answers"][5]:
                store.users[user_ind]["user_answers"][5].remove(call.data)
            else:
                store.users[user_ind]["user_answers"][5].append(call.data)
        else:
            store.users[user_ind]["user_answers"][5] = [call.data]

        question.call_data = store.users[user_ind]["user_answers"][5]
        question.keyboard = question.generate_keyboard()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=question.text, reply_markup=question.keyboard)


if __name__ == "__main__":
    bot.infinity_polling()
