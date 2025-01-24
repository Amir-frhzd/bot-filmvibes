import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import re
import asyncio
from asyncio import Semaphore

load_dotenv()
# توکن ربات تلگرام
BOT_TOKEN = os.getenv('BOT_TOKEN')
SAVE_CHANNEL_ID = int(os.getenv("SAVE_CHANNEL_ID"))  # آی‌دی کانال خصوصی
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME")  # نام کاربری کانال که کاربر باید عضو آن باشد

#محدودیت 30 پیام در ثانیه

message_semaphore = Semaphore(30)
async def send_and_delete_message(chat_id, message_id, context):
    """مدیریت ارسال و حذف پیام فایل و هشدار برای هر کاربر"""
    async with message_semaphore :
        try:
            # کپی فایل به کاربر
            sent_message = await context.bot.copy_message(
                chat_id=chat_id,
                from_chat_id=SAVE_CHANNEL_ID,
                message_id=message_id
            )

            # ارسال پیام هشدار
            info_message = await context.bot.send_message(
                chat_id=chat_id,
                text="⚠️ پیام بالا را هر چه سریعتر در Saved Message  خود انتقال دهید !\n"
                    "⌛️این پیام زیر 1 دقیقه حذف خواهد شد ."
            )

            # صبر برای 45 ثانیه
            await asyncio.sleep(45)

            # حذف پیام فایل و پیام هشدار
            await context.bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)
            await context.bot.delete_message(chat_id=chat_id, message_id=info_message.message_id)

        except Exception as e:
            print(f"خطا در مدیریت پیام: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """مدیریت پیام‌ها و اجرای همزمانی"""
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
                # اگر عضو کانال باشد، اجرای task به صورت جداگانه برای کاربر
                asyncio.create_task(send_and_delete_message(chat_id, message_id, context))
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