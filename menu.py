from aiogram.types import ReplyKeyboardMarkup,InlineKeyboardButton,KeyboardButton, InlineKeyboardMarkup
import config
menu_novip = ReplyKeyboardMarkup(
    keyboard=[
    [
    
        KeyboardButton(text="🏡 Профиль")
    ],
    [
        KeyboardButton(text="❓ Информация"),
        KeyboardButton(text="📎 Помощь")
    ],
    ],
    resize_keyboard=True
    )

menu_vip = ReplyKeyboardMarkup(
    keyboard=[
    [
    	KeyboardButton(text="🏡 Профиль")
    ],
    [
    	KeyboardButton(text="❓ Информация"),
       KeyboardButton(text="📎 Помощь")
    ],
    ],
    resize_keyboard=True
    )

menu_admin = ReplyKeyboardMarkup(
    keyboard=[
    [
    	KeyboardButton(text="❓ Информация")
    ],
    [
        KeyboardButton(text="Рассылка")
    ],
    [
        KeyboardButton(text="Выплаты")
    ],
    [
        KeyboardButton(text="Выдача")
    ],
    ],
    resize_keyboard=True
	)



exit = ReplyKeyboardMarkup(
	keyboard=[
	[
		KeyboardButton(text="Отменить")
	],
	],
	resize_keyboard=True
	)
buy_podp = InlineKeyboardMarkup()
sjss = InlineKeyboardButton(text="🔓 Оплатить доступ", callback_data="buy")
#reff = InlineKeyboardButton(text="Мои рефералы", callback_data="refererr")
buy_podp.add(sjss)

buy_vip = InlineKeyboardMarkup()
vyplata = InlineKeyboardButton(text="Вывести", callback_data="vip")
buy_vip.add(vyplata)


status_id_channel = InlineKeyboardMarkup(row_width=1)
link =InlineKeyboardButton(text="⛓ Ссылка на канал",url=f"https://t.me/{config.link_channel}")
check_user_group = InlineKeyboardButton(text="✅ Я подписался",callback_data="check_user_group")
status_id_channel.add(link,check_user_group)