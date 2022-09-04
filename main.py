import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from app.config import BOT_TOKEN
from app.handlers.commands import register_command_handlers
from app.handlers.customer import register_customer_handlers
from app.handlers.callbacks import register_callback_handlers
from app.handlers.inline_mode import register_inline_mode_handlers




async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Начать")
    ]
    await bot.set_my_commands(commands)


async def main():
	logging.basicConfig(level=logging.INFO)

	storage = MemoryStorage()
	bot = Bot(token=BOT_TOKEN, parse_mode = 'html')
	dp = Dispatcher(bot, storage = storage)

	register_command_handlers(dp)
	register_customer_handlers(dp)
	register_callback_handlers(dp)
	register_inline_mode_handlers(dp)


	await set_commands(bot)

	await dp.start_polling()



if __name__ == '__main__':
	asyncio.run(main())