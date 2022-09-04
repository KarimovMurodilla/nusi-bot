from aiogram import types


def sendRegButton():
	btn = types.InlineKeyboardMarkup(row_width = 1)
	reg = types.InlineKeyboardButton(text = "Зарегистрироваться", callback_data = 'reg')
	btn.add(reg)

	return btn


def sendMainMenu():
	menu_customer = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
	to_order = types.KeyboardButton("Заказать")
	my_profil = types.KeyboardButton("Мой профиль")
	menu_customer.add(to_order, my_profil)

	return menu_customer


# def viewBiscuits():
# 	btns_view = types.InlineKeyboardMarkup(resize_keyboard = True, row_width = 1)
# 	view = types.InlineKeyboardButton("Просмотреть", callback_data = 'view')
# 	view_list = types.InlineKeyboardButton("Просмотреть список", switch_inline_query_current_chat = '!get_biscuits')
# 	btns_view.add(view, view_list)

# 	return btns_view


def editProfil():
	btn = types.InlineKeyboardMarkup(row_width = 1)
	edit = types.InlineKeyboardButton(text = "Редактировать", callback_data = 'edit')
	btn.add(edit)

	return btn


def sendCancelBtn():
	btn_canc = types.ReplyKeyboardMarkup(resize_keyboard = True)
	canc = types.KeyboardButton("Отменить")
	btn_canc.add(canc)

	return btn_canc


def sendContact():
	contact = types.ReplyKeyboardMarkup(resize_keyboard = True)
	send_contact = types.KeyboardButton("Поделиться контактом", request_contact = True)
	contact.add(send_contact)

	return contact


def sendSkipBtn():
	btn = types.InlineKeyboardMarkup(row_width = 1)
	skip = types.InlineKeyboardButton(text = "Пропустить", callback_data = 'skip')
	btn.add(skip)

	return btn


def sendBiscuitButtons(user_id, biscuit_name):
	btns = types.InlineKeyboardMarkup(row_width = 3)
	remove = types.InlineKeyboardButton(text = "➖", callback_data = f'remove {user_id},{biscuit_name}')
	add = types.InlineKeyboardButton(text = "➕", callback_data = f'add {user_id},{biscuit_name}')

	view_list = types.InlineKeyboardButton("Просмотреть список", switch_inline_query_current_chat = '!get_biscuits')

	backP = types.InlineKeyboardButton(text = "⬅️", callback_data = 'backP')
	nextP = types.InlineKeyboardButton(text = "➡️", callback_data = 'nextP')
	done = types.InlineKeyboardButton(text = "✅", callback_data = f'done {user_id},{biscuit_name}')

	btns.add(remove, add)
	btns.add(view_list)
	btns.add(backP, done, nextP)


	return btns	


def choose(rowid):
	btn = types.InlineKeyboardMarkup()
	chuz = types.InlineKeyboardButton(text = "Выбрать", callback_data = f'chuz {rowid-1}')
	btn.add(chuz)

	return btn


def menuConfirm():
	btns = types.InlineKeyboardMarkup(row_width=2)
	confirm = types.InlineKeyboardButton(text = "Подтвердить", callback_data = 'confirm')
	change = types.InlineKeyboardButton(text = "Изменить", callback_data = 'change')
	btns.add(confirm, change)

	return btns


def sendGeo():
	location = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width = 1)
	geo = types.KeyboardButton("Отправить геолокацию", request_location = True)
	canc = types.KeyboardButton("Отменить")
	location.add(geo, canc)

	return location	


def showInfo(user_id, latitude, longitude):
	info = types.InlineKeyboardMarkup(row_width=1)
	show_geo = types.InlineKeyboardButton(text = "Показать геолокацию", callback_data = f'show_geo {latitude},{longitude}')
	show_profil = types.InlineKeyboardButton(text = "Показать профиль", callback_data = f'show_profil {user_id}')
	info.add(show_geo, show_profil)

	return info


def changeStatus(order_id):
	end = types.InlineKeyboardMarkup(row_width=1)
	end_order = types.InlineKeyboardButton(text = "Закончить", callback_data = f'end_order {order_id}')
	end.add(end_order)

	return end

def adminPanel():
	admin_panel = types.InlineKeyboardMarkup(row_width=1)
	order = types.InlineKeyboardButton(text = "Посмотреть заказы", switch_inline_query_current_chat = f'!get_orders')
	admin_panel.add(order)

	return admin_panel
