
import os
import sys
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

sys.stdout.reconfigure(encoding='utf-8')
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

client = OpenAI(
    api_key=os.environ.get("DEEPFA_API_KEY"),
    base_url="https://deepfa.ir/api/v1" 
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="سلام! من دستیار هوشمند فروشگاه پمپ آب هستم. چطور می‌تونم کمکتون کنم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    try:
        response = client.chat.completions.create(
            model="gpt-6-luna",
            messages=[
                {"role": "system", "content": "شما یک دستیار فروش و پشتیبانی برای یک فروشگاه پمپ آب استوک هستید. پاسخ‌ها باید کوتاه، مودبانه و مفید باشند. اگر مشتری قصد خرید داشت، از او بخواهید مشخصات دقیق پمپ مورد نیازش را بنویسید."},
                {"role": "user", "content": user_text}
            ]
        )
        answer = response.choices[0].message.content
        await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
    except Exception as e:
        print(f"Error: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text="متاسفانه در پردازش پیام خطایی رخ داد.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("ربات تلگرام روشن شد و منتظر پیام‌هاست...")
    application.run_polling()
