import telebot
from utils import *


API_KEY = "6044967219:AAHfyB0ZZo8B_s207pW3Ax3tNNxsBTvVQFE"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я помогу тебе проанализировать, высока ли вероятность банкротства компании. Для того, чтобы начвать, введи команду /analyze")


@bot.message_handler(commands=["analyze"])
def pair(message):

    bot.send_message(message.chat.id, "Вставьте во 2 столбец таблицы по ссылке финансовые показатели компании. После того, как вы вставите информацию, напишите боту: готово!")

    url = "https://docs.google.com/spreadsheets/d/1VH56vqu7FNdHQvRwrhsUZSU61mmBJVUCWqf6pCqenhE"

    bot.send_message(message.chat.id, f'[Google sheets link]({url})', disable_web_page_preview=True, parse_mode="MarkdownV2")
    bot.register_next_step_handler(message, give_link, url)


def give_link(message, url):
    bot.send_message(message.chat.id, "Анализирую информацию")
    bot.send_message(message.chat.id, make_prediction(data_preprocessing((gs_to_df(url)))))
    clear_column(url,2)

bot.polling()


