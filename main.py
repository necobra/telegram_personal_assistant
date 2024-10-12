import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta

import requests
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv
from pytz import timezone

from config import config


load_dotenv()
telegram_token = os.environ['TELEGRAM_BOT_TOKEN']
if not telegram_token:
    logging.error("No TELEGRAM_BOT_TOKEN provided!")
    sys.exit(1)

bot = Bot(telegram_token, parse_mode=ParseMode.HTML)
dp = Dispatcher()

users_list = config.users_list
groups_list = config.groups_list


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    if message.from_user.id in users_list:
        await message.answer("Добрий день, пане Олександре")
    else:
        await message.asnswer("Немає доступу")


@dp.message(F.text, Command("status"))
async def status_handler(message: Message) -> None:
    await message.answer("I`m still working for you!")


@dp.message(F.text, Command("get_id"))
async def status_handler(message: Message) -> None:
    await message.answer(f"Your telegram id: {message.from_user.id}")
    await message.answer(f"Chat telegram id: {message.chat.id}")

@dp.message(F.text, Command("test_data_of_message"))
async def status_handler(message: Message) -> None:
    print(message)
    await message.answer("Thanks!")

async def send_daily_message():
    """Відправка щоденного повідомлення в обраний чат о 8:00 за Київським часом."""
    kyiv_tz = timezone('Europe/Kiev')
    target_time = datetime.now(kyiv_tz).replace(hour=8, minute=00, second=00, microsecond=0)

    # Якщо поточний час вже після 8:00, заплануйте відправку на наступний день
    if datetime.now(kyiv_tz) >= target_time:
        target_time += timedelta(days=1)

    while True:
        # Вирахувати час до наступного відправлення
        delay = (target_time - datetime.now(kyiv_tz)).total_seconds()
        await asyncio.sleep(delay)

        try:
            data: dict = requests.get("http://127.0.0.1:8080/quote").json()
            message = f"{data['text']}\n<i>{data['author']}</i>"
        except Exception as e:
            message = f"Exception during forming daily message: {e}"

        # Надіслати повідомлення
        for user in users_list:
            await bot.send_message(chat_id=user, text=message)

        # Запланувати наступне відправлення на наступний день
        target_time += timedelta(days=1)


async def main() -> None:
    await asyncio.gather(
        dp.start_polling(bot),
        send_daily_message()
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
