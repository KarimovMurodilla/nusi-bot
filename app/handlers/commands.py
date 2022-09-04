from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from .. import connection, config, buttons


bot = Bot(token=config.BOT_TOKEN, parse_mode = 'html')


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    user_id = message.chat.id

    if not connection.getUser(user_id):
        await bot.send_message(message.chat.id, "Добро пожаловать!", reply_markup = buttons.sendRegButton())

    else:
        await bot.send_message(message.chat.id, "Главное меню", reply_markup = buttons.sendMainMenu())


async def cmd_admin(message: types.Message, state: FSMContext):
    await state.finish()

    await bot.send_message(message.chat.id, "Добро пожаловать на админ панель!", reply_markup = buttons.adminPanel())


def register_command_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands = 'start', state="*")
    dp.register_message_handler(cmd_admin, commands = 'admin', chat_id = config.ADMINS, state="*")

