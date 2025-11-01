import telebot
import csv
import requests
from io import StringIO

# ⬇️ Yahan apna bot token daalo
BOT_TOKEN = "8301301018:AAFTTllsKTp7WuM0WhhZSx7avsuKz-w-dS4"
bot = telebot.TeleBot(BOT_TOKEN)

# ⬇️ Google Sheet CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/13rNNmc1qAQeI-U1NyjTnDsdWEcEupNmRNnqq5Hxt2aQ/export?format=csv"

def get_movie_link(movie_name):
    response = requests.get(CSV_URL)
    data = response.content.decode('utf-8')
    csv_data = csv.reader(StringIO(data))
    for row in csv_data:
        if movie_name.lower() in row[0].lower():
            return row[1]
    return None

@bot.message_handler(func=lambda message: True)
def reply_link(message):
    movie_name = message.text.strip()
    link = get_movie_link(movie_name)
    if link:
        bot.reply_to(message, f"🎬 {movie_name} link:\n{link}")
    else:
        bot.reply_to(message, "❌ Sorry, movie/anime nahi mili Google Sheet me.")

print("✅ Bot is running...")
bot.polling()