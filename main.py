"""
This program is designed for spot medium-term trading against the trend 
and long-term spot trading from potential trend reversal points.

The program does not use a loop to update indicator values. 
Since this script is designed to run through the task scheduler (Cron).
"""

from datetime import datetime
from functions import get_tradingview_data, message_for_bot
import telebot, json

# to connect the telegram bot to the script, 
#   you must specify the bot token and the id of the chat to which the bot will send messages, 
#   this data can be specified in the telegram_bot_data file or written through the console
try:
    from telebot_data import TELEGRAM_TOKEN, CHAT_ID
    telegram_token = TELEGRAM_TOKEN
    chat_id = CHAT_ID
except ImportError:
    telegram_token = input("Enter telegram bot token: ")
    chat_id = input("Enter your chat id: ")

telegram_bot = telebot.TeleBot(token=telegram_token)
current_date = f"{datetime.now():%d.%m.%Y %H:%M}"

# in the program, to save the current state of the ticker (under the levels / corrected), the "decline" keys are used, 
#   which are added to the dictionary with cryptocurrency data
# so that these dictionary elements are not lost when the script is restarted, 
#   the data of each ticker is saved in a separate json file
try:
    # if json files with ticker data have not yet been created, the try block is executed
    with open("ticker_data/btc_data.json", "x"), open("ticker_data/eth_data.json", "x"):
        pass
    btc_data = get_tradingview_data("BTCUSDT", current_date)
    eth_data = get_tradingview_data("ETHUSDT", current_date)
    # if json files already exist, a FileExistsError exception is thrown and the except block is executed
except FileExistsError:
    with open("ticker_data/btc_data.json", "r") as btc_data_file, open("ticker_data/eth_data.json", "r") as eth_data_file:
        btc_data = json.load(btc_data_file)
        eth_data = json.load(eth_data_file)

    # dictionaries obtained from json files are updated with actual indicator data for tickers
    btc_data.update(get_tradingview_data("BTCUSDT", current_date))
    eth_data.update(get_tradingview_data("ETHUSDT", current_date))
finally:
    # the values of the btc and eth indicators are passed to the message_for_bot function, 
    #   which returns the received data as the first element of the tuple, 
    #   and returns the message for the telegram bot as the second element, or None if there is no new message
    btc_data, message = message_for_bot(btc_data)

    # in the case when a new message was returned for bitcoin, a message for ethereum is not requested 
    # in this case, a message for ethereum will be requested the next time the script is run, 
    #   since bitcoin will already have a key with its state 
    #   and the message_for_bot function will not return a repeated message about the state of bitcoin
    if not message:
        eth_data, message = message_for_bot(eth_data)
    # if there is a new message, it is sent to the telegram bot
    if message:
        telegram_bot.send_message(chat_id=chat_id, text=message)
    # if there is no new message for the telegram bot, and the script start time is midnight, 
    #   a message will be sent to telegrams stating that the script continues to run through the scheduler
    elif current_date.endswith("00:00"):
        telegram_bot.send_message(chat_id=chat_id, text="Bot is up and running")

    # actual ticker indicator data and ticker status are written to json files 
    #   for reading the next time the script is run
    with open("ticker_data/btc_data.json", "w") as btc_data_file, open("ticker_data/eth_data.json", "w") as eth_data_file:
        json.dump(btc_data, btc_data_file, ensure_ascii=False, indent=4)
        json.dump(eth_data, eth_data_file, ensure_ascii=False, indent=4)