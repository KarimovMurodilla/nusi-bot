from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from .. import connection, buttons, config


bot = Bot(token=config.BOT_TOKEN, parse_mode = 'html')



async def get_biscuits(query: types.InlineQuery):
	item = connection.getBiscuits()
	
	try:
		r = [types.InlineQueryResultArticle( 
				id = f'{n}', 
				title = f'{item[n][1]}', 
				input_message_content = types.InputTextMessageContent(
					message_text =  f"<b>Название:</b> {item[n][1]}\n"
									f"<b>Цена:</b> {item[n][5]}\n"
									f"<b>В коробке:</b> {item[n][4]} kg\n"
									f"<b>Цена за коробки:</b> {item[n][6]}\n"
									f"<b>Срок годности:</b> {item[n][7]}\n\n"),
											reply_markup = buttons.choose(item[n][8]))
						for n in range(len(item))]
			
		await query.answer(r, cache_time = 60)
		
	except Exception as e:
		print(e)


async def get_orders(query: types.InlineQuery):
	item = connection.getOrders()
	
	try:
		if query.from_user.id in config.ADMINS:
			r = [types.InlineQueryResultArticle( 
					id = f'{n}', 
					title = f'{item[n][5]}\tЗАКАЗ - {n+1}', 
					input_message_content = types.InputTextMessageContent(
						message_text =  f"{item[n][2]}\n\n"
									  	f"Номер покупателя: <code>{connection.getUser(item[n][0])[3]}</code>\n"
									  	f"Telegram: @{connection.getUser(item[n][0])[1]}"),
												reply_markup = buttons.changeStatus(item[n][1]))
							for n in range(len(item))]
			
		await query.answer(r, cache_time = 60)
		
	except Exception as e:
		print(e)



def register_inline_mode_handlers(dp: Dispatcher):
	dp.register_inline_handler(get_biscuits, lambda query: query.query ==  f"!get_biscuits", state = '*')
	dp.register_inline_handler(get_orders, lambda query: query.query ==  f"!get_orders", state = '*')
