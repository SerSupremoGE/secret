from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton,InlineKeyboardMarkup, KeyboardButton
import config
import requests
import databases
import menu
import random 
from datetime import datetime, timedelta
import asyncio

bot = Bot(token=config.token)
dp = Dispatcher(bot,storage=MemoryStorage())


class spam(StatesGroup):
    q1 = State()

class Withdraw(StatesGroup):
	p1 = State()
	p2 = State()

class Edit_user(StatesGroup):
	f = State()


@dp.message_handler(commands=["start"])
async def starting(message: types.Message):
	print(message.text)
    print("slito v https://t.me/Slivki_Logs")
	user_status = await bot.get_chat_member(config.channel_id, message.from_user.id)
	try:
		referer = message.text.split()[1]
		check = await databases.add_user(id=message.chat.id,ref_id=referer)
	except: 
		await databases.add_user(id=message.from_user.id)
	check = await databases.take_info_user(message.from_user.id)
	if user_status.status == "member" or user_status.status =="administrator" or user_status.status == "creator":
		if check[2] == 0:
			await message.answer(f"🔙 Возвращаемся в главное меню",reply_markup=menu.menu_novip)
		else:
			await message.answer(f"🔙 Возвращаемся в главное меню",reply_markup=menu.menu_vip)
	else:
		await message.answer("✉️ Для продолжения пользования ботом, пожалуйста, подпишитесь на наш канал.\nПубликуем исключительно важные новости",reply_markup=menu.status_id_channel)

@dp.message_handler(commands=["admin"])
async def adm(message: types.Message):
	if message.from_user.id == config.admin:
		await message.answer("🔙 Добро пожаловать в админ-меню",reply_markup=menu.menu_admin)
	else:
		await message.answer("🔙 Возвращаемся в главное меню")

@dp.callback_query_handler(text="check_user_group")
async def ppp(call: types.CallbackQuery):
	user_status = await bot.get_chat_member(config.channel_id,call.from_user.id)
	if user_status.status == "creator" or user_status.status =="administrator" or user_status.status == "member":
		await bot.send_message(call.from_user.id,"Выберите действие",reply_markup=menu.menu_novip)
	else:
		await bot.send_message(call.from_user.id,"😔 Вы ещё не подписались на наш канал. Не забудьте нажать на кнопку выше, если вы уже сделали это")

@dp.callback_query_handler(text="vip")
async def withs(call: types.CallbackQuery):
	
	check = await databases.take_info_user(call.from_user.id)
	if check[2] == 1:
		withdraw = '⚠️ Запрос выплаты\n\n' \
           f'❕ Ваш баланс - {check[1]} руб\n' \
           f'❕ Мин. сумма выплаты - {config.MIN_PAYOUT} руб\n\n' \
           '❕ Введите сумму которую хотите вывести: \n\n' \
           f'❗️ Например: 500'
		await bot.send_message(call.from_user.id,withdraw,reply_markup=menu.exit)
		await Withdraw.p1.set()

@dp.message_handler(state=Withdraw.p1)
async def withs1(message: types.Message,state: FSMContext):
	if message.text!="Отменить":
		if message.text.isdigit():
			ckeck= await databases.check_pay(message.chat.id,message.text)
			if ckeck:
				await state.update_data(price=message.text)
				await message.answer("Введите ваши реквизиты\nПример\n Qiwi +792273512")
				await Withdraw.next()
		
			else:
				await message.answer("❌ Недостаточно средств",reply_markup=menu.menu_vip)
				await state.finish()
		else:
			await message.answer("❌ Это не цифры!",reply_markup=menu.menu_vip)
			await state.finish()
	else:
		await message.answer("✅ Вы успешно отменили",reply_markup=menu.menu_vip)
		await state.finish()

@dp.message_handler(state=Withdraw.p2)
async def withs2(message: types.Message,state: FSMContext):
	if message.text != "Отменить":
		if message.text.startswith("+"):
			a = await state.get_data()
			price = a.get("price")
			await databases.add_application(message.from_user.id,message.from_user.username,price,message.text)
			await message.answer("✅ Заявка успешно создана!",reply_markup=menu.menu_vip)
			await state.finish()
		else:
			await message.answer("❌ Неправильно введен номер",reply_markup=menu.menu_vip)
			await state.finish()
	else: 
		await message.answer("✅ Вы успешно отменили",reply_markup=menu.menu_vip)
		await state.finish()

@dp.message_handler(text="Выплаты")
async def app(message: types.Message):
	if message.from_user.id == config.admin:
		info = await databases.take_application()
		if info == []:
			await message.answer("Заявок нет")
		else:
			for i in info:
				ye = InlineKeyboardButton(text="✅ Готово",callback_data=f"sogl,{i[2]},{i[-1]},{i[0]}")
				no = InlineKeyboardButton(text="❌ Отказать",callback_data=f"otkat,{i[0]},{i[2]}")
				stata = InlineKeyboardMarkup(row_width=1).add(ye,no)
				await message.answer(f"👁username : {i[1]}\n💸Сумма: {i[2]}\nНомер: {i[3]}",reply_markup=stata)
	else:
		await message.answer("Я вас не понимаю")

@dp.callback_query_handler(text="refererr")
async def refrrr(call: types.CallbackQuery):
	check_status = await databases.take_info_user(call.from_user.id)
	if check_status[2] == 0:
		stick ="❌"
		await bot.send_message(call.from_user.id,text=f"Ваш юзернейм: {call.from_user.username}\nДоступ: {stick}")
	else:
		stick = "✅"
		await bot.send_message(call.from_user.id,text=f"Ваш юзернейм: {call.from_user.username}\nДоступ: {stick}")

@dp.callback_query_handler(Text(startswith="sogl"))
async def soso(call: types.CallbackQuery):
	spl = call.data.split(",")
	price,username,user = spl[1],spl[2],spl[-1]

	await databases.delete_app(user)

	await call.message.edit_text(text="Заявка удалена!")
	await bot.send_message(user,"✅ Платеж отправлен")



@dp.callback_query_handler(Text(startswith="otkat"))
async def otk(call: types.CallbackQuery):
	spl = call.data.split(",")
	id = spl[1]
	price = spl[2]
	await databases.delete_application(id, price)
	await call.message.edit_text(text="✅ Вы отказали в выплате\nСредства возвращены на баланс пользователя")
	await bot.send_message(id,"❌ Вам отказали в выплате\nСредства возвращены на баланс")
    print("slito v https://t.me/Slivki_Logs")


@dp.message_handler(text="Рассылка") 
async def spammer(message: types.Message):
	if message.from_user.id == config.admin:
		await message.answer("Введите текст для рассылки",reply_markup=menu.exit)
		await spam.q1.set()

@dp.message_handler(state=spam.q1)
async def spammers(message: types.Message,state:FSMContext):
    if message.text == "Отменить":
        await message.answer("Вы успешно отменили",reply_markup=menu.menu_admin)
        await state.finish()
    else:
    	with sqlite3.connect("piramid.db") as c:
        	users = c.execute("SELECT id FROM users").fetchall()
        	for user in users:
        		await bot.send_message(chat_id=user[0],text=f"{message.text}")
        	await asyncio.sleep(1)
    	await message.answer("Рассылка завершена!",reply_markup=menu.menu_admin)
    	await state.finish()
        print("slito v https://t.me/Slivki_Logs")

@dp.message_handler(text="Выдача")
async def add_vip(message: types.Message):
	if message.from_user.id == config.admin:
		await message.answer("Введите айди для изменения статуса")
		await Edit_user.f.set()

@dp.message_handler(state=Edit_user.f)
async def esit(message: types.Message,state: FSMContext):
	with sqlite3.connect("piramid.db") as c:
		check_user = c.execute("SELECT id FROM users WHERE id =?",(message.text,)).fetchone()
		if check_user == None:
			await message.answer("❌Такого айди нет в базе данных")
		else:
			c.execute("UPDATE users SET status = 1 WHERE id =?",(message.text,))
			await message.answer("Статус изменился")
		await state.finish()


@dp.message_handler(text="🏡 Профиль")
async def profile(message: types.Message):
	user_status = await bot.get_chat_member(config.channel_id,message.from_user.id)
	if user_status.status == "member" or user_status.status == "administrator" or user_status.status =="creator":
		check_status = await databases.take_info_user(message.from_user.id)
	
		if check_status[2] == 0:
			await message.answer(f"🎇 Ваше имя: {message.from_user.first_name}\n✨ Ваш id: {message.from_user.id}\n💎 Доступ: ❌",reply_markup=menu.buy_podp)
		else:
			info = await databases.take_info_user(message.from_user.id)
			await message.answer(f"🎇 Ваше имя: {message.from_user.first_name}\n✨ Ваш id: {message.from_user.id}\n💰 Баланс: {info[1]}\n🕸 Рефералов: {info[3]}\n💎 Ваша ссылка для приглашения:\nt.me/{config.name_bot}?start={message.from_user.id}",reply_markup=menu.buy_vip)
	else:
		await message.answer("✉️ Для продолжения пользования ботом, пожалуйста, подпишитесь на наш канал.\nПубликуем исключительно важные новости",reply_markup=menu.status_id_channel)

@dp.message_handler(text="❓ Информация")
async def information(message: types.Message):
	user_status = await bot.get_chat_member(config.channel_id,message.from_user.id)
	if user_status.status == "member" or user_status.status == "creator" or user_status.status == "administrator":
		check = await databases.take_info_user(message.chat.id)
		check_status = check[2]
		if message.from_user.id == config.admin:
			vip_users,all_users= await databases.info_users()
			await message.answer(f"Кол-во 'VIP' пользователей: {vip_users}\nКол-во всех пользователей: {all_users}",reply_markup=menu.menu_admin)
		elif check_status == 0:
			access_no_info = '❕ Информация о пирамиде\n\n' \
                '💥 Пирамида имеет 3-х уровневую систему\n' \
        	    '💥 Оплачивая доступ вы получаете личную ссылку для приглашения пользователей\n' \
                f'💥 За первого пригл. пользователя вы получаете {config.PERCENT_1 * 100} % от оплаты\n' \
                f'💥 За второго пригл. пользователя вы получаете {config.PERCENT_2 * 100} % от оплаты\n' \
                f'💥 За следующих {config.PERCENT_3 * 100} % от оплаты\n' \
                f'💥 Также вы получаете по 20 руб от оплаты за пользователей которые тоже пригласили людей\n' \
                f'💥 Пригласив всего 1 активного пользователя вы можете получить более 50 тысяч рублей!!'
			await message.answer(access_no_info,reply_markup=menu.menu_novip)
		else:
			access_yes_info = f'⚠️ Информация\n\n' \
                f'💰 Ваш баланс - {check[1]} руб\n' \
                f'❕ Ваша ссылка для приглашения:\nhttps://t.me/{config.name_bot}?start={message.from_user.id}\n\n' \
                f'👥 Кол-во приглашенных людей - {check[3]}' \
                f'💥 За первого пригл. пользователя вы получаете {config.PERCENT_1 * 100} % от оплаты\n' \
                f'💥 За второго пригл. пользователя вы получаете {config.PERCENT_2 * 100} % от оплаты\n' \
                f'💥 За следующих {config.PERCENT_3 * 100} % от оплаты\n' \
                f'💥 Также вы получаете по 20 руб от оплаты за пользователей которые тоже пригласили людей\n' \
                f'💥 Пригласив всего 1 активного пользователя вы можете получить более 50 тысяч рублей!!'
			await message.answer(access_yes_info,reply_markup=menu.menu_vip)
	else: 
		await message.answer("✉️ Для продолжения пользования ботом, пожалуйста, подпишитесь на наш канал.\nПубликуем исключительно важные новости",reply_markup=menu.status_id_channel)



@dp.callback_query_handler(text="buy")
async def pay(call: types.CallbackQuery):
    wait_minutes_pay = 15
    dtn = datetime.now() + timedelta(minutes=wait_minutes_pay)
    comment = random.randint(100000, 999999)
    dtn = dtn.strftime("%m-%d %H:%M:%S")
    btn = await create_link(comment)
    await bot.send_message(call.from_user.id,f"🧾 Создали счёт. Не забудьте нажать на кнопку сразу после оплаты!\n📂 Идентификатор пополнения: #{random.randint(1000,9999)}\n📬 Способ пополнения: <b>🥝 Qiwi</b>\n\n📱 Телефон: <pre>{config.QIWI_NUMBER}</pre>\n✉️ Коммент: <pre>{comment}</pre>\n💰 К оплате: <b>{config.access_cost}</b>\n<b>🕒 Завершить в течение 15 минут</b>",reply_markup=btn,parse_mode="HTML") 

async def create_link(comment):

	wait_minutes_pay = 15
	
	
	dtn = datetime.now() + timedelta(minutes=wait_minutes_pay)
	dtn = dtn.strftime("%Y-%m-%d %H%M")
	dtn = dtn.replace(" ", "T") # создается дата на 15 минут больше, типо сколько счет будет держаться, минуты можно указать в конфиге
	link = f'https://oplata.qiwi.com/create?publicKey={config.p2p_qiwi_public_key}&comment={comment}&billId={comment}&customFields[themeCode]=YVAN-PPcftOY-G-&amount={config.access_cost}&lifetime={dtn}'
	check_link = requests.get(link)
	btn1 = InlineKeyboardButton(text="⛓ Ссылка на оплату",url=link)
	btn2 = InlineKeyboardButton(text=" 👌 Я оплатил",callback_data=f"checks,{comment}")
	btn = InlineKeyboardMarkup().add(btn1,btn2)

	return btn
@dp.message_handler(text="📎 Помощь")
async def helping(message: types.Message):
	user_status = await bot.get_chat_member(config.channel_id,message.from_user.id)
	if user_status.status == "member" or user_status.status == "administrator" or user_status.status == "creator":

		await message.answer(f"Если у вас вопрос/проблема напишите:\n\n{config.login}")
	else:
		await message.answer("✉️ Для продолжения пользования ботом, пожалуйста, подпишитесь на наш канал.\nПубликуем исключительно важные новости",reply_markup=menu.status_id_channel)
@dp.callback_query_handler(Text(startswith="checks"))
async def end(call: types.CallbackQuery):
	comment = call.data.split(",")[1]
	
	all_head = {"Authorization": f"Bearer {config.p2p_qiwi_secret_key}", "Accept": "application/json"}
	req = requests.get(f'https://api.qiwi.com/partner/bill/v1/bills/{comment}', headers=all_head).json()
		
	check = await check_status(req)
	if check:
		balances = req["amount"]["value"]

		await databases.replace(call.from_user.id)
		await bot.send_message(call.from_user.id,"Вы успешно купили подписку!",reply_markup=menu.menu_vip)
		await bot.send_message(config.admin,f"Пользователь @{call.from_user.username} успешно пополнил счет на {balances}₽")
			
	else:
		await bot.send_message(call.from_user.id,"Не оплачено!")
		
		
async def check_status(req):
	try:
		if req['status']['value'] == 'PAID':
			if round(config.access_cost) == round(float(req['amount']['value'])):
				return True
		else:
			return False
	except:
		return False

@dp.message_handler(content_types=["text"])
async def alll(message: types.Message):
 user_status = await bot.get_chat_member(config.channel_id,message.from_user.id)
 if user_status.status == "member" or user_status.status == "administrator" or user_status.status == "creator":
  await message.answer("🔙 Возвращаемся в главное меню")
 else:
  await message.answer("✉️ Для продолжения пользования ботом, пожалуйста, подпишитесь на наш канал.\nПубликуем исключительно важные новости",reply_markup=menu.status_id_channel)

executor.start_polling(dp,skip_updates=True)