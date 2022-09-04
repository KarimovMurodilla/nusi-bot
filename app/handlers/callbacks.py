from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .. import buttons, config, connection

bot = Bot(token=config.BOT_TOKEN, parse_mode = 'html')


class Confirmation(StatesGroup):
	get_geo = State()


async def callback_view(c: types.CallbackQuery, state: FSMContext):
	try:
		user_id = c.from_user.id
		connection.updatePag(user_id, '0')	
		pag = connection.getUser(user_id)[5]
		all_data = connection.getBiscuits()[pag]

		await bot.send_photo(
			chat_id = c.from_user.id, 
			photo = all_data[2],
			caption = f"<b>Название:</b> {all_data[1]}\n"
					  f"<b>Цена:</b> {all_data[5]}\n"
					  f"<b>В коробке:</b> {all_data[4]} kg\n"
					  f"<b>Цена за коробки:</b> {all_data[6]}\n"
					  f"<b>Срок годности:</b> {all_data[7]}\n\n"
					  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
					  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}",
						reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))
	
	except:
		await bot.send_message(c.from_user.id, "Добро пожаловать!", reply_markup = buttons.sendRegButton())




async def callback_add(c: types.CallbackQuery, state: FSMContext):
	user_id = c.from_user.id
	ids = c.data[4:].split(',')
	pag = connection.getUser(user_id)[5]
	all_data = connection.getBiscuits()[pag]
	connection.addBasket(user_id, ids[1], '+')
	await bot.answer_callback_query(c.id, show_alert = False, text = '➕')

	await bot.edit_message_media(
			media = types.InputMedia(
				type = 'photo', 
				media = all_data[2], 
				caption = f"<b>Название:</b> {all_data[1]}\n"
						  f"<b>Цена:</b> {all_data[5]}\n"
						  f"<b>В коробке:</b> {all_data[4]} kg\n"
						  f"<b>Цена за коробки:</b> {all_data[6]}\n"
						  f"<b>Срок годности:</b> {all_data[7]}\n\n"
						  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
						  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}"),		
				chat_id = c.message.chat.id,
				message_id = c.message.message_id,
					reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))


async def callback_remove(c: types.CallbackQuery, state: FSMContext):
	user_id = c.from_user.id
	ids = c.data[7:].split(',')
	pag = connection.getUser(user_id)[5]
	all_data = connection.getBiscuits()[pag]
	
	connection.addBasket(user_id, ids[1], '-')
	await bot.answer_callback_query(c.id, show_alert = False, text = '➖')
	
	await bot.edit_message_media(
			media = types.InputMedia(
				type = 'photo', 
				media = all_data[2], 
				caption = f"<b>Название:</b> {all_data[1]}\n"
						  f"<b>Цена:</b> {all_data[5]}\n"
						  f"<b>В коробке:</b> {all_data[4]} kg\n"
						  f"<b>Цена за коробки:</b> {all_data[6]}\n"
						  f"<b>Срок годности:</b> {all_data[7]}\n\n"
						  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
						  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}"),		
				chat_id = c.message.chat.id,
				message_id = c.message.message_id,
					reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))


async def callback_back(c: types.CallbackQuery, state: FSMContext):
	user_id = c.from_user.id
	connection.updatePag(user_id, '-')		
	pag = connection.getUser(user_id)[5]
	all_data = connection.getBiscuits()[pag]
	
	if pag < 0:
		connection.updatePag(user_id, '+')		
		await bot.answer_callback_query(c.id, show_alert = False, text = "❗️Вы находитесь на первом каталоге списка")	


	else:
		await bot.answer_callback_query(c.id, show_alert = False, text = '⬅️')
		await bot.edit_message_media(
				media = types.InputMedia(
					type = 'photo', 
					media = all_data[2], 
					caption = f"<b>Название:</b> {all_data[1]}\n"
							  f"<b>Цена:</b> {all_data[5]}\n"
							  f"<b>В коробке:</b> {all_data[4]} kg\n"
							  f"<b>Цена за коробки:</b> {all_data[6]}\n"
							  f"<b>Срок годности:</b> {all_data[7]}\n\n"
							  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
							  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}"),		
					chat_id = c.message.chat.id,
					message_id = c.message.message_id,
						reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))


async def callback_next(c: types.CallbackQuery, state: FSMContext):
	try:
		user_id = c.from_user.id
		connection.updatePag(user_id, '+')			
		pag = connection.getUser(user_id)[5]	
		all_data = connection.getBiscuits()[pag]

		await bot.answer_callback_query(c.id, show_alert = False, text = '➡️')
		await bot.edit_message_media(
				media = types.InputMedia(
					type = 'photo', 
					media = all_data[2], 
					caption = f"<b>Название:</b> {all_data[1]}\n"
							  f"<b>Цена:</b> {all_data[5]}\n"
							  f"<b>В коробке:</b> {all_data[4]} kg\n"
							  f"<b>Цена за коробки:</b> {all_data[6]}\n"
							  f"<b>Срок годности:</b> {all_data[7]}\n\n"
							  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт\n\n"
							  f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[0])[2] * float(all_data[5]) * float(all_data[4]))}"),		
					chat_id = c.message.chat.id,
					message_id = c.message.message_id,
						reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))

	except Exception as e:
		print(e)
		await bot.answer_callback_query(c.id, show_alert = True, text = "❗️Вы находитесь на последнем каталоге списка")


async def callback_done(c: types.CallbackQuery, state: FSMContext):
	try:
		user_id = c.from_user.id
		all_data = connection.getAllBasket(user_id, None, status = False)
		msg = ''.join([(f"<b>Название:</b> {connection.getBiscuitsFromId(all_data[i][1])[1]}\n"
					    f"<b>Цена:</b> {connection.getBiscuitsFromId(all_data[i][1])[5]}\n"
					  	f"<b>В коробке:</b> {connection.getBiscuitsFromId(all_data[i][1])[4]} kg\n"
					  	f"<b>Цена за коробки:</b> {connection.getBiscuitsFromId(all_data[i][1])[6]}\n"
					  	f"<b>Срок годности:</b> {connection.getBiscuitsFromId(all_data[i][1])[7]}\n\n"
					  	f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[i][1])[2]} шт\n"
					  	f"<b>Сумма:</b> {'%.3f' %(connection.getBasket(user_id, all_data[i][1])[2] * float(connection.getBiscuitsFromId(all_data[i][1])[5]) * float(connection.getBiscuitsFromId(all_data[i][1])[4]))}\n\n\n\n")
							for i in range(len(all_data)) if connection.getBasket(user_id, all_data[i][1])[2] != 0])

		total = [float(connection.getBasket(user_id, all_data[i][1])[2] * float(connection.getBiscuitsFromId(all_data[i][1])[5]) * float(connection.getBiscuitsFromId(all_data[i][1])[4]))
			for i in range(len(all_data)) if connection.getBasket(user_id, all_data[i][1])[2] != 0]

		if not total:
			await bot.answer_callback_query(c.id, show_alert = True, text = "❗️Вы еще ничего не выбрали")

		else:
			await bot.send_message(c.from_user.id, f"{msg}<b>Общая сумма:</b> {'%.3f' %(sum(total))}", 
				reply_markup = buttons.menuConfirm())

	except Exception as e:
		print(e)
		await bot.answer_callback_query(c.id, show_alert = True, text = "❗️Вы еще ничего не выбрали")


async def callback_choose(c: types.CallbackQuery, state: FSMContext):
	user_id = c.from_user.id
	pag = c.data[5:]
	connection.updatePag(user_id, pag)
	all_data = connection.getBiscuits()[int(pag)]

	await bot.send_photo(
		chat_id = user_id, 
		photo = all_data[2],
		caption = f"<b>Название:</b> {all_data[1]}\n"
				  f"<b>Цена:</b> {all_data[5]}\n"
				  f"<b>В коробке:</b> {all_data[4]} kg\n"
				  f"<b>Цена за коробки:</b> {all_data[6]}\n"
				  f"<b>Срок годности:</b> {all_data[7]}\n\n"
				  f"<b>Выбрано коробок:</b> {connection.getBasket(user_id, all_data[0])[2]} шт",
				  	reply_markup = buttons.sendBiscuitButtons(user_id, all_data[0]))


async def callback_confirm(c: types.CallbackQuery, state: FSMContext):
	await Confirmation.get_geo.set()
	await bot.delete_message(c.from_user.id, c.message.message_id)
	await bot.send_message(c.from_user.id, "Отправьте мне свою локацию, чтобы донести заказ",
		reply_markup = buttons.sendGeo())


async def input_geo(message: types.Message, state: FSMContext):
	user_id = message.from_user.id
	latitude = message.location.latitude
	longitude = message.location.longitude
	order_id = len(connection.getOrders())
	all_data = connection.getAllBasket(user_id, None, status = False)

	all_orders = ''.join([(f"{connection.getBiscuitsFromId(all_data[i][1])[1]} - {connection.getBasket(user_id, all_data[i][1])[2]} шт\n")
		for i in range(len(all_data)) if connection.getBasket(user_id, all_data[i][1])[2] != 0])

	await bot.send_message(message.chat.id, 'Спасибо за покупку!', reply_markup = buttons.sendMainMenu())
	connection.addOrder(user_id, order_id, all_orders, latitude, longitude)
	connection.deleteBasket(user_id)

	for i in config.ADMINS:
		await bot.send_message(i, f"{all_orders}\n\n"
								  f"Номер покупателя: <b>{connection.getUser(user_id)[3]}</b>\n"
								  f"Telegram: @{connection.getUser(user_id)[1]}",
			reply_markup = buttons.showInfo(user_id, latitude, longitude))


async def callback_show_geo(c: types.CallbackQuery, state: FSMContext):
	ids = c.data[9:].split(',')
	latitude = ids[0]
	longitude = ids[1]
	print(ids)

	await bot.send_location(c.from_user.id, latitude, longitude)


async def callback_show_profil(c: types.CallbackQuery, state: FSMContext):
	ids = c.data[12:].split(',')
	user_data = connection.getUser(ids[0])

	await bot.send_photo(
		chat_id = c.from_user.id, 
		photo = user_data[4],
		caption = f"<b>{user_data[2]}</b>\n\n"
				  f"Номер: <code>{user_data[3]}</code>")


async def callback_end_order(c: types.CallbackQuery, state: FSMContext):
	order_id = c.data[10:]

	if connection.getOrderWhereId(order_id)[5] == '🔴':
		await bot.answer_callback_query(c.id, show_alert = True, text = '❗️Вы уже закончили этот заказ')
	
	else:
		connection.updateOrderStatus(order_id)
		await bot.answer_callback_query(c.id, show_alert = True, text = '✅ Заказ завершен')




def register_callback_handlers(dp: Dispatcher):
	dp.register_callback_query_handler(callback_view, lambda c: c.data == 'change',  state = '*')

	dp.register_callback_query_handler(callback_add, lambda c: c.data.startswith('add'),  state = '*')  
	dp.register_callback_query_handler(callback_remove, lambda c: c.data.startswith('remove'),  state = '*')    

	dp.register_callback_query_handler(callback_back, lambda c: c.data == 'backP',  state = '*')
	dp.register_callback_query_handler(callback_next, lambda c: c.data == 'nextP',  state = '*')
	dp.register_callback_query_handler(callback_done, lambda c: c.data.startswith('done'),  state = '*')  

	dp.register_callback_query_handler(callback_choose, lambda c: c.data.startswith('chuz'),  state = '*')

	dp.register_callback_query_handler(callback_confirm, lambda c: c.data == 'confirm',  state = '*')
	dp.register_message_handler(input_geo, content_types = ['location', 'venue'],  state = Confirmation.get_geo)

	dp.register_callback_query_handler(callback_show_geo, lambda c: c.data.startswith('show_geo'),  state = '*')    
	dp.register_callback_query_handler(callback_show_profil, lambda c: c.data.startswith('show_profil'),  state = '*')  

	dp.register_callback_query_handler(callback_end_order, lambda c: c.data.startswith('end_order'),  state = '*')    



