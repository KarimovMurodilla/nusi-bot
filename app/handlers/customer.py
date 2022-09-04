import datetime

from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .. import buttons, config, connection

bot = Bot(token=config.BOT_TOKEN, parse_mode = 'html')


class StartReg(StatesGroup):
	name = State()
	contact = State()
	photo = State()


async def callback_reg(c: types.CallbackQuery, state: FSMContext):
	await StartReg.name.set()
	await bot.delete_message(c.from_user.id, c.message.message_id)
	await bot.send_message(c.from_user.id, "Отправьте мне свое Имя-Отчество", 
		reply_markup = buttons.sendCancelBtn())


async def process_input_name(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['name'] = message.text

		await StartReg.next()
		msg = await bot.send_message(message.chat.id, "Отправьте мне свой номер телефона", reply_markup = buttons.sendContact())
		data['msg_id'] = msg.message_id


async def process_input_contact(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['contact'] = message.contact.phone_number

		await StartReg.next()
		await bot.delete_message(message.chat.id, data['msg_id'])
		await bot.send_message(message.chat.id, "Отправьте мне ваше фото или фото магазина", reply_markup = buttons.sendSkipBtn())


async def process_input_photo(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['photo'] = message.photo[-1].file_id
		
		user_id = message.from_user.id
		username = message.from_user.username
		name = data['name']
		contact = data['contact']
		photo = data['photo']
		date_registration = datetime.datetime.today().strftime('%d.%m.%Y - %H:%M')


	if not connection.getUser(user_id):		
		connection.regUser(user_id, username, name, contact, photo, date_registration)
		await bot.send_message(message.from_user.id, "Ваш профиль успешно создан!", reply_markup = buttons.sendMainMenu())

	else:
		connection.regUser(user_id, username, name, contact, photo, date_registration)
		await bot.send_message(message.from_user.id, "Ваш профиль успешно отредактирован!", reply_markup = buttons.sendMainMenu())
	
	await state.finish()


async def callback_skip(c: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['photo'] = 'AgACAgIAAxkBAAMVYYKFm95En7QMI0fP2DrsibUWWwgAAuS1MRsl3RlIeIWiIhu5GmcBAAMCAAN4AAMhBA'
		
		user_id = c.from_user.id
		username = c.from_user.username
		name = data['name']
		contact = data['contact']
		photo = data['photo']
		date_registration = datetime.datetime.today().strftime('%d.%m.%Y - %H:%M')


	if not connection.getUser(user_id):		
		connection.regUser(user_id, username, name, contact, photo, date_registration)	
		await bot.delete_message(c.from_user.id, c.message.message_id)
		await bot.send_message(c.from_user.id, "Ваш профиль успешно создан!", reply_markup = buttons.sendMainMenu())

	else:
		connection.regUser(user_id, username, name, contact, photo, date_registration)
		await bot.delete_message(c.from_user.id, c.message.message_id)
		await bot.send_message(c.from_user.id, "Ваш профиль успешно отредактирован!", reply_markup = buttons.sendMainMenu())
	
	await state.finish()


async def get_my_profil(message: types.Message, state: FSMContext):
	await state.finish()	
	user_id = message.from_user.id
	user_data = connection.getUser(user_id)

	await bot.send_photo(
		chat_id = message.chat.id, 
		photo = user_data[4],
		caption = f"<b>{user_data[2]}</b>\n\n"
				  f"Номер: <code>{user_data[3]}</code>", 

		reply_markup = buttons.editProfil())
	

async def to_order(message: types.Message, state: FSMContext):
	try:
		user_id = message.from_user.id
		connection.updatePag(user_id, '0')	
		pag = connection.getUser(user_id)[5]
		all_data = connection.getBiscuits()[pag]

		await bot.send_photo(
			chat_id = message.from_user.id, 
			photo = all_data[2],
			caption = f"<b>Название:</b> {all_data[1]}\n"
					  f"<b>Цена:</b> {all_data[5]}\n"
					  f"<b>В коробке:</b> {all_data[4]} kg\n"
					  f"<b>Цена за коробки:</b> {all_data[6]}\n"
					  f"<b>Срок годности:</b> {all_data[7]}\n\n"
					  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
					  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}",
						reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))
	
	except Exception as e:
		print(e)
		await bot.send_message(message.from_user.id, "Добро пожаловать!", reply_markup = buttons.sendRegButton())


# async def callback_to_order(c: types.CallbackQuery, state: FSMContext):
# 	await bot.send_message(c.from_user.id, "Выберите:", reply_markup = buttons.viewBiscuits())


async def to_canc(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Отменено!", reply_markup = buttons.sendMainMenu())




def register_customer_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(callback_reg, lambda c: c.data == 'reg',  state = '*')  
	dp.register_callback_query_handler(callback_reg, lambda c: c.data == 'edit',  state = '*')    

	dp.register_message_handler(process_input_name, state = StartReg.name)
	dp.register_message_handler(process_input_contact, content_types = 'contact', is_sender_contact = True, state = StartReg.contact)
	dp.register_message_handler(process_input_photo, content_types = 'photo', state = StartReg.photo)
	dp.register_callback_query_handler(callback_skip, lambda c: c.data == 'skip', state = StartReg.photo) 

	dp.register_message_handler(get_my_profil, text = 'Мой профиль', state = '*')
	dp.register_message_handler(to_order, text = 'Заказать', state = '*')
	dp.register_message_handler(to_canc, text = 'Отменить', state = '*')

