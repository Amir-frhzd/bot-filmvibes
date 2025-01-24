from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import re

# توکن ربات تلگرام
BOT_TOKEN = "7555787267:AAGOqRt9rMSeZ3sVI6g5JGzR2OBNabKKXXA"
SAVE_CHANNEL_ID = -1002372104175  # آی‌دی کانال خصوصی SaveFilm
CHANNEL_USERNAME = "@Filmvibes_ir"  # نام کاربری کانال که کاربر باید عضو آن باشد

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """ارسال فایل هنگام اجرای دستور /start"""
    chat_id = update.effective_chat.id
    
    # استخراج message_id از پارامتر start
    start_param = update.message.text  # دریافت پارامتر start از متن پیام
    message_id = None
    match = re.search(r"message_id_(\d+)", start_param)  # جستجو برای message_id
    if match:
        message_id = int(match.group(1))  # استخراج message_id از پارامتر

    if message_id:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        try:
            member_status = await context.bot.get_chat_member(CHANNEL_USERNAME, chat_id)
            
            if member_status.status in ['member', 'administrator', 'creator']:
                # اگر عضو کانال باشد، ارسال فایل
                await context.bot.forward_message(
                    chat_id=chat_id,  # ارسال به کاربر
                    from_chat_id=SAVE_CHANNEL_ID,  # کانال خصوصی SaveFilm
                    message_id=message_id  # پیام آی‌دی فایل که از URL دریافت شده
                )
            else:
                # اگر عضو کانال نباشد
                await update.message.reply_text(
                    "لطفاً ابتدا در کانال ما عضو شوید و سپس دوباره تلاش کنید:\n"
                    f"{CHANNEL_USERNAME}"
                )
        except Exception as e:
            await update.message.reply_text(f"خطایی رخ داد: {e}")
    else:
        await update.message.reply_text("message_id در URL مشخص نشده است.")

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