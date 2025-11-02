import telebot
import csv
import requests
from io import StringIO

# 🔹 Bot token aur Google Sheet link
BOT_TOKEN = "8301301018:AAFTTllsKTp7WuM0WhhZSx7avsuKz-w-dS4"
CSV_URL = "https://docs.google.com/spreadsheets/d/13rNNmc1qAQeI-U1NyjTnDsdWEcEupNmRNnqq5Hxt2aQ/export?format=csv"

bot = telebot.TeleBot(BOT_TOKEN)

# 🔹 Memory store
users = set()

# 🔹 Google Sheet se movie link lana
def get_movie_link(movie_name):
    response = requests.get(CSV_URL)
    data = response.content.decode('utf-8')
    csv_data = csv.reader(StringIO(data))
    for row in csv_data:
        if movie_name.lower() in row[0].lower():
            return row[1]
    return None

# ---------------- COMMANDS ---------------- #

@bot.message_handler(commands=['start'])
def start(message):
    users.add(message.chat.id)
    bot.reply_to(message, "🎬 *Welcome to Movie Finder Bot!*\n\nSend any movie/anime name and I’ll give you its link 🍿\n\nType /help to see all commands.", parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help(message):
    help_text = """🛠 *Available Commands:*
    
/start - Welcome message  
/help - Show this help  
/about - Info about the bot  
/latest - Show latest 5 movies from sheet  
/stats - Show total users  
/feedback - Send your feedback  
/broadcast - Send message to all users (admin only)
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "🤖 *Movie Finder Bot*\nCreated by: Gurmeet Singh\nLanguage: Python 🐍\nPowered by Google Sheets 📄", parse_mode='Markdown')

@bot.message_handler(commands=['latest'])
def latest(message):
    response = requests.get(CSV_URL)
    data = response.content.decode('utf-8')
    csv_data = list(csv.reader(StringIO(data)))
    latest_movies = csv_data[-5:]  # last 5
    msg = "🎞 *Latest Movies/Anime:*\n\n"
    for row in latest_movies:
        msg += f"• {row[0]} — [Watch Here]({row[1]})\n"
    bot.reply_to(message, msg, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.reply_to(message, f"📊 Total registered users: *{len(users)}*", parse_mode='Markdown')

@bot.message_handler(commands=['feedback'])
def feedback(message):
    bot.reply_to(message, "📝 Please type your feedback message below:")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == 6690196088:  # ✅ Tumhara Telegram ID
        bot.reply_to(message, "✉️ Send the message you want to broadcast:")
        bot.register_next_step_handler(message, send_broadcast)
    else:
        bot.reply_to(message, "❌ You are not authorized to use this command.")

def send_broadcast(message):
    for user_id in users:
        try:
            bot.send_message(user_id, f"📢 {message.text}")
        except:
            pass
    bot.reply_to(message, "✅ Broadcast sent to all users.")

# ---------------- SEARCH FUNCTION ---------------- #

@bot.message_handler(func=lambda message: True)
def reply_link(message):
    users.add(message.chat.id)
    movie_name = message.text.strip()
    link = get_movie_link(movie_name)
    if link:
        bot.reply_to(message, f"🎬 {movie_name} link:\n{link}")
    else:
        bot.reply_to(message, "❌ Sorry, movie/anime nahi mili Google Sheet me.")

print("✅ Bot is running...")
bot.polling()