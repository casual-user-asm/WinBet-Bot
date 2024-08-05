<h1>WinbetBot</h1>

WinbetBot is a Telegram bot designed to assist cybersports enthusiasts in making informed decisions on match outcomes by providing statistical insights and predictions.

## Telegram Bot API token to use telebot

1. Create a Bot:

    - Open Telegram and search for the "BotFather" bot.
    - Start a chat with BotFather and use the command /newbot to create a new bot.
    - Follow the prompts to set up your bot. BotFather will give you a token for your new bot.

2. Use the Token:

    - bot = telebot.TeleBot('YOUR_ACTUAL_TOKEN_HERE')

## Installation

First, clone this repository:

<!-- start:code block -->
# Clone this repository
git clone https://github.com/casual-user-asm/WinBet-Bot.git

# Go to project directory
cd WinBet-Bot

# Install dependencies
pip install -r requirements.txt

# Run the bot
python main.py

<!-- end:code block -->
