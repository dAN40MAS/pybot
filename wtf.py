import telebot
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="",
)

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может отвечать на твои вопросы. Просто напиши мне что-нибудь!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_chat_action(message.chat.id, 'typing')
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1",
            messages=[
                {
                    "role": "user",
                    "content": message.text
                }
            ]
        )

        bot.reply_to(message, completion.choices[0].message.content, parse_mode="Markdown")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.polling()
