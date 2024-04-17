import telebot
import requests

# Telegram Bot Token
TOKEN = '7131600643:AAGjblUGG3mBl84FRDOn_rxTGhLBXeLTIa0'
bot = telebot.TeleBot(TOKEN)

def shorten_url(url):
    response = requests.get(f'http://localhost:5000/shorten', params={'url': url})
    if response.status_code == 200:
        return response.json()['shortened_url']
    else:
        return "Error: Failed to shorten URL"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me a link, and I'll shorten it for you!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("http"):
        short_url = shorten_url(message.text)
        bot.reply_to(message, f'Shortened URL: {short_url}')
    else:
        bot.reply_to(message, "Please send a valid URL.")

if __name__ == '__main__':
    bot.polling()
