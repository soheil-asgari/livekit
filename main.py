# main.py (اصلاح‌شده)

import os
import logging
import asyncio  # <-- ۱. این ماژول اضافه شد
from dotenv import load_dotenv
from livekit.agents import (
    JobContext,
    WorkerOptions,
    Worker,
)  # <-- ۲. 'main' حذف و 'Worker' اضافه شد
from livekit.agents.llm import LLM
from livekit.plugins.openai import OpenAIRealtimePlugin, OpenAIRealtimeModel

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# تنظیم لاگ‌ها برای دیباگ
logging.basicConfig(level=logging.INFO)


async def entrypoint(ctx: JobContext):
    """
    نقطه ورود اصلی ربات.
    این تابع زمانی که یک "کار" (Job) جدید برای ربات تعریف می‌شود، اجرا می‌گردد.
    (این بخش بدون تغییر است)
    """
    logging.info(f"🚀 Agent در حال پیوستن به اتاق: {ctx.room.name}")

    # ۱. تعریف مدل OpenAI Realtime
    model = OpenAIRealtimeModel(
        model="gpt-4o-realtime-preview",
        voice="alloy",
    )

    # ۲. ایجاد پلاگین OpenAI
    openai_plugin = OpenAIRealtimePlugin(
        model=model,
    )

    # ۳. اتصال پلاگین به ربات
    ctx.connect(openai_plugin.track_input, openai_plugin.track_output)

    logging.info("✅ ربات با موفقیت به پلاگین OpenAI متصل شد.")


#
# ۳. [بخش اصلاح‌شده] تنظیمات و اجرای Worker
#
async def main_entry():
    """
    تابع async اصلی برای راه‌اندازی Worker.
    """
    logging.info("🏁 در حال راه‌اندازی Worker ربات...")

    # تنظیمات Worker برای اتصال به سرور LiveKit شما
    worker_options = WorkerOptions(
        host=os.environ["LIVEKIT_URL"],
        api_key=os.environ["LIVEKIT_API_KEY"],
        api_secret=os.environ["LIVEKIT_API_SECRET"],
    )

    # ایجاد یک نمونه از Worker
    worker = Worker(
        entrypoint_fnc=entrypoint,  # تابع entrypoint که قبلا نوشتیم
        worker_options=worker_options,
    )

    # اجرای Worker
    await worker.run()


if __name__ == "__main__":
    # اجرای تابع async اصلی با استفاده از asyncio
    try:
        asyncio.run(main_entry())
    except KeyboardInterrupt:
        logging.info("🛑 ربات با دستور کاربر متوقف شد.")
