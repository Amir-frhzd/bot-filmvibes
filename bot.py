from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات تلگرام
BOT_TOKEN = "7555787267:AAGOqRt9rMSeZ3sVI6g5JGzR2OBNabKKXXA"
SAVE_CHANNEL_ID = -1002372104175  # آی‌دی کانال خصوصی SaveFilm
MESSAGE_ID = 2  # آی‌دی پیام فایل (نسخه 480p)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال فایل هنگام اجرای دستور /start"""
    chat_id = update.effective_chat.id
    #message_id from url
    start_param = update.query.data if update.callback_query else None
    
    try:
        # ارسال فایل از کانال SaveFilm
        await context.bot.forward_message(
            chat_id=chat_id,  # ارسال به کاربر
            from_chat_id=SAVE_CHANNEL_ID,  # کانال خصوصی SaveFilm
            message_id=MESSAGE_ID  # پیام آی‌دی فایل 480
        )
    except Exception as e:
        await update.message.reply_text(f"خطایی رخ داد: {e}")

def main():
    """اجرای ربات"""
    # ساختن اپلیکیشن
    application = Application.builder().token(BOT_TOKEN).build()

    # اضافه کردن هندلر برای دستور /start
    application.add_handler(CommandHandler("start", start))

    # اجرای ربات
    application.run_polling()

if __name__ == "__main__":
    main()