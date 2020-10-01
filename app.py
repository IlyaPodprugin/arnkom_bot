import telebot
import config
from telebot import types
from config import TOKEN


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["text"])
def any_msg(message):
    greeting_keyboard = types.InlineKeyboardMarkup()
    ready_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
    greeting_keyboard.add(ready_button)
    bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=greeting_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")


bot.polling()
