import asyncio
import json
import logging
from datetime import datetime

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.core.bot import bot, storage


async def create_mailing_task(mailing_data: dict) -> None:
    """Create a mailing task in Redis stream."""
    if mailing_data.get("delay"):
        delay_str = mailing_data["delay"]
        delay_dt = datetime.strptime(delay_str, "%d.%m.%Y %H:%M")
        delay_timestamp = int(delay_dt.timestamp())
        mailing_data["scheduled_time"] = delay_timestamp

    await storage.redis.xadd("mailing_stream", {"data": json.dumps(mailing_data)})


async def process_mailing_tasks() -> None:
    while True:
        try:
            tasks = await storage.redis.xrange("mailing_stream")

            for task_id, task_data in tasks:
                task = json.loads(task_data[b"data"].decode("utf-8"))
                if not task.get("scheduled_time") or task.get("scheduled_time") <= int(datetime.now().timestamp()):
                    await send_mailing(task)
                    await storage.redis.xdel("mailing_stream", task_id)

        except Exception as e:
            logging.error(f"Error processing mailing tasks: {e}", exc_info=True)
        await asyncio.sleep(5)


async def send_mailing(mailing_data: dict) -> None:
    """Send mailing to a specific user."""
    chat_id = mailing_data.get("chat_id")
    text = mailing_data.get("text")
    image = mailing_data.get("image")
    button_text = mailing_data.get("button_text")
    button_url = mailing_data.get("button_url")

    keyboard = None
    if button_text and button_url:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=button_text, url=button_url)]])

    try:
        if image:
            await bot.send_photo(chat_id=chat_id, photo=image, caption=text, reply_markup=keyboard)
        elif text:
            await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        await asyncio.sleep(1 / 30)
    except Exception as e:
        logging.error(f"Error sending mailing to {chat_id}: {e}")
