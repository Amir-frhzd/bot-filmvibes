from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import re

# توکن ربات تلگرام
BOT_TOKEN = "7555787267:AAGOqRt9rMSeZ3sVI6g5JGzR2OBNabKKXXA"
SAVE_CHANNEL_ID = -1002372104175  # آی‌دی کانال خصوصی
CHANNEL_USERNAME = "@Filmvibes_ir"  # نام کاربری کانال که کاربر باید عضو آن باشد

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """کپی فایل از کانال خصوصی و ارسال آن بدون نمایش Forwarded"""
    chat_id = update.effective_chat.id

    # استخراج message_id از پارامتر start
    start_param = update.message.text
    message_id = None
    match = re.search(r"message_id_(\d+)", start_param)
    if match:
        message_id = int(match.group(1))  # استخراج message_id

    if message_id:
        # بررسی اینکه آیا کاربر عضو کانال است یا خیر
        try:
            member_status = await context.bot.get_chat_member(CHANNEL_USERNAME, chat_id)

            if member_status.status in ['member', 'administrator', 'creator']:
                # اگر عضو کانال باشد
                try:
                    # کپی پیام از کانال خصوصی به کاربر
                    await context.bot.copy_message(
                        chat_id=chat_id,
                        from_chat_id=SAVE_CHANNEL_ID,
                        message_id=message_id
                    )
                except Exception as e:
                    await update.message.reply_text(f"خطا در پردازش پیام: {e}")
            else:
                await update.message.reply_text(
                    f"لطفاً ابتدا در کانال ما عضو شوید:\n{CHANNEL_USERNAME}"
                )
        except Exception as e:
            await update.message.reply_text(f"خطایی رخ داد: {e}")
    else:
        await update.message.reply_text("message_id مشخص نشده است.")

def main():
    """اجرای ربات"""
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

if __name__ == "__main__":
    main()