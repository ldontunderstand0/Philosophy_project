from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

faq = KeyboardButton('Правила')
back = KeyboardButton('Назад')

themes = KeyboardButton('Выбор темы')
theme1 = KeyboardButton('Тема 1')
theme2 = KeyboardButton('Тема 2')
theme3 = KeyboardButton('Тема 3')
theme4 = KeyboardButton('Тема 4')
theme5 = KeyboardButton('Тема 5')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(themes, faq)
themeMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(theme1, theme2, theme3, theme4, theme5, back)
gameMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(faq, back)
