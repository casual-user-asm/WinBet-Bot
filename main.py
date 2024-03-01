import telebot
from schedule_matches import matches_schedule
from pars import prediction

matches = matches_schedule()
upcoming_matches = matches[0]
live_matches = matches[1]
heroes_info = matches[2]
live_match = matches[3]

bot = telebot.TeleBot('6116891770:AAHw6zmNt4yLo0dRwVK2fMM9aT1Y9v1ZFXs')


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id, "Hello, buddy. U can use commands /schedule to know schedule matches on today and /prediction when match started to know bot's prediction about drafts")


@bot.message_handler(commands=['schedule'])
def schedule(message):

    all_matches = ''
    for upcoming in upcoming_matches:
        all_matches += f'{upcoming}\n\n'
    bot.send_message(message.chat.id, all_matches)


@bot.message_handler(commands=['live_matches'])
def live_schedule(message):

    all_matches_live = ''
    for live in live_matches:
        all_matches_live += f'{live}\n\n'
    bot.send_message(message.chat.id, all_matches_live)


@bot.message_handler(commands=['prediction'])
def predict(message):

    result = prediction(heroes_info, live_match)
    all_predictions = ''
    for predict in result:
        all_predictions += f'{predict}\n\n'
    bot.send_message(message.chat.id, all_predictions)


bot.polling(non_stop=True)
