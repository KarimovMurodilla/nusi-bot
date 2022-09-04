import datetime
import os
import sqlite3 as sql

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

with sql.connect(os.path.join(BASE_DIR, 'bot.db'), check_same_thread=False) as con:
	cur = con.cursor()


# ---For Users---
def createUserTable():
	cur.execute("""CREATE TABLE IF NOT EXISTS users(
				user_id INT,
				username TEXT,				
				name TEXT,
				contact TEXT,
				photo TEXT,
				pagination INT DEFAULT 0,
				date_registration timestamp
				)""")
	con.commit()


def createBiscuitTable():
	cur.execute("""CREATE TABLE IF NOT EXISTS biscuits(
				id INT,
				biscuit_name TEXT,
				picture TEXT,
				picture_url TEXT,				
				kg INT,
				price_per_kg TEXT,
				price TEXT,
				shelf_life TEXT
				)""")
	con.commit()


def createBasketTable():
	cur.execute("""CREATE TABLE IF NOT EXISTS basket(
				user_id INT,
				biscuit_id INT,
				amount INT
				)""")
	con.commit()


def createOrdersTable():
	cur.execute("""CREATE TABLE IF NOT EXISTS orders(
				user_id INT,
				description TEXT,
				latitude TEXT,
				longitude TEXT,
				status TEXT
				)""")
	con.commit()


# createUserTable()
# createBiscuitTable()
# createBasketTable()
# createOrdersTable()


# ---USER TABLE---
def getUser(user_id: str):
	user = cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchone()
	return user


def regUser(user_id, username, name, contact, photo, date_registration):
	if not getUser(user_id):
		cur.execute("INSERT INTO users (user_id, username, name, contact, photo, date_registration) VALUES (?,?,?,?,?,?)", (user_id, username, name, contact, photo, date_registration,))
		con.commit()

	else:
		cur.execute("UPDATE users SET name = ?, contact = ?, photo = ? WHERE user_id = ?", (name, contact, photo, user_id,))
		con.commit()


def updatePag(user_id: str, value: str):
	if value == '+':
		cur.execute("UPDATE users SET pagination = pagination+1 WHERE user_id = ?", (user_id,))
		con.commit()

	elif value == '-':
		cur.execute("UPDATE users SET pagination = pagination-1 WHERE user_id = ?", (user_id,))
		con.commit()			

	else:
		cur.execute("UPDATE users SET pagination = ? WHERE user_id = ?", (value, user_id,))
		con.commit()		


# ---BISCUITS---
def getBiscuits():
	bis = cur.execute("SELECT *, rowid FROM biscuits").fetchall()
	return bis


def getBiscuitsFromId(biscuit_id):
	bis = cur.execute("SELECT * FROM biscuits WHERE id = ?", (biscuit_id,)).fetchone()
	return bis


# ---BASKET---
def getBasket(user_id, biscuit_id):
	bis = cur.execute("SELECT * FROM basket WHERE user_id = ? AND biscuit_id = ?", (user_id, biscuit_id,)).fetchone()
	if bis:
		return bis

	else:
		return ['yep', 'yo', 0]

def getAllBasket(user_id, biscuit_id, status = True):
	if status:
		all_bis = cur.execute("SELECT * FROM basket WHERE user_id = ? AND biscuit_id = ?", (user_id, biscuit_id,)).fetchone()
		return all_bis
	else:
		all_bis1 = cur.execute("SELECT * FROM basket WHERE user_id = ?", (user_id,)).fetchall()
		return all_bis1	


def addBasket(user_id, biscuit_id, amount, latitude = None, longtitude = None):
	if not getAllBasket(user_id, biscuit_id) and amount == '+':
		cur.execute("INSERT INTO basket (user_id, biscuit_id, amount)VALUES(?,?,?)", (user_id, biscuit_id, 1))
		con.commit()
	
	else:
		if amount == '+':
			cur.execute("UPDATE basket SET amount = amount+1 WHERE user_id = ? AND biscuit_id = ?", (user_id, biscuit_id,))
			con.commit()

		elif amount == '-' and getAllBasket(user_id, biscuit_id)[2] != 0:
			cur.execute("UPDATE basket SET amount = amount-1 WHERE user_id = ? AND biscuit_id = ?", (user_id, biscuit_id,))
			con.commit()


def deleteBasket(user_id):
	cur.execute("DELETE FROM basket WHERE user_id = ?", (user_id,))
	con.commit()


# ORDERS TABLE
def addOrder(user_id, order_id, description, latitude, longitude):
	today = datetime.datetime.now().strftime('%d.%m.%Y')
	cur.execute("INSERT INTO orders (user_id, order_id, description, latitude, longitude, status, date_added)VALUES(?,?,?,?,?,?,?)", (user_id, order_id, description, latitude, longitude, '🟢', today))
	con.commit()


def getOrders():
	all_orders = cur.execute("SELECT * FROM orders").fetchall()
	return all_orders
	

def getOrderWhereId(order_id):
	order = cur.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,)).fetchone()
	return order


def updateOrderStatus(order_id):
	cur.execute("UPDATE orders SET status = ? WHERE order_id = ?", ('🔴', order_id,))
	con.commit()