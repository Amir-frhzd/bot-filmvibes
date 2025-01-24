from telethon.sync import TelegramClient
from datetime import datetime
from telethon.tl.types import DocumentAttributeFilename  # وارد کردن این کلاس

# اطلاعات حساب تلگرام شما
API_ID ="26541226"          # API ID شما
API_HASH = "5576f1c7de7da9709990721f39499c83"    # API Hash شما
PHONE_NUMBER = "+989355001378"   # شماره تلفن تلگرام شما (مثلاً +989123456789)

# آی‌دی یا یوزرنیم کانال خصوصی
CHANNEL_ID = -1002372104175  # یا "@YourChannelUsername"


async def get_last_file_id():
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        # عضویت در کانال (اگر عضو نیستید)
        await client.get_entity(CHANNEL_ID)

        # گرفتن پیام‌های کانال
        async for message in client.iter_messages(CHANNEL_ID):
            # بررسی اینکه پیام حاوی فایل باشد
            if message.document:  # اگر پیام شامل فایل باشد
                file_id = message.document.id
                print(f"Last File ID: {file_id}")
                break  # فقط اولین فایل پیدا شده را می‌گیریم که آخرین پیام خواهد بود

# اجرای تابع
import asyncio
asyncio.run(get_last_file_id())