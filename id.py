from telethon.sync import TelegramClient
from datetime import datetime
from telethon.tl.types import DocumentAttributeFilename
# اطلاعات حساب تلگرام شما
API_ID = "26541226"        # API ID شما
API_HASH = "5576f1c7de7da9709990721f39499c83"    # API Hash شما
PHONE_NUMBER = "+989355001378"  # شماره تلفن تلگرام شما (مثلاً +989123456789)

# آی‌دی یا یوزرنیم کانال خصوصی
CHANNEL_ID = -1002372104175 # یا "@YourChannelUsername"

# تاریخ امروز
today = datetime.now().date()

async def get_file_ids():
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        # عضویت در کانال (اگر عضو نیستید)
        await client.get_entity(CHANNEL_ID)

        # گرفتن پیام‌های کانال
        async for message in client.iter_messages(CHANNEL_ID):
            # بررسی اینکه پیام مربوط به امروز باشد
            if message.date.date() == today:
                if message.document:  # اگر پیام شامل فایل باشد
                    file_id = message.document.id
                    file_name = None
                    for attribute in message.document.attributes:
                        if isinstance(attribute, DocumentAttributeFilename):
                            file_name = attribute.file_name
                            break

                    if file_name:
                        print(f"File Name: {file_name}, File ID: {file_id}")
                    else:
                        print(f"File ID: {file_id}, No file name available")

# اجرای تابع
import asyncio
asyncio.run(get_file_ids())