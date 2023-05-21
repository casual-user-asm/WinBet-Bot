import telebot
from schedule_matches import schedule_today_matches
from pars import current_match
from random import randint



bot = telebot.TeleBot('6116891770:AAHw6zmNt4yLo0dRwVK2fMM9aT1Y9v1ZFXs')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello, buddy. U can use commands /schedule to know schedule matches on today and /prediction when match started to know bot's prediction about drafts")

@bot.message_handler(commands=['schedule'])
def schedule(message):
    matches_schedule = schedule_today_matches()
    bot.send_message(message.chat.id, matches_schedule)


@bot.message_handler(commands=['prediction'])
def predict(message):
    prediction = current_match()
    bot.send_message(message.chat.id, prediction)

bot.polling(non_stop=True)
