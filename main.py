import telebot
from telebot import types
import webbrowser
import requests
from bs4 import BeautifulSoup


bot = telebot.TeleBot('7784812218:AAFrZ4D0mOC1AE4oAk9BeJFpJgRv0Tc-dWs')

# Посилання на Google Таблиці для кожного факультету
faculty_links = {
    'ЛСПГ': 'https://docs.google.com/spreadsheets/d/1SwDK0rV5As5d-XPyc4Y5-sLtL-Bj6oMA/edit',
    'ІМАКІТ': 'https://docs.google.com/spreadsheets/d/1Rpr3gn7Ijjk3Ndj6pnVRTv0uLKbpJJa7/edit',
    'ДТД': 'https://docs.google.com/spreadsheets/d/1dXK-kGi4p8f407QNVo_hmhK0Q8NPN3pG/edit',
    'КНІТ': 'https://docs.google.com/spreadsheets/d/1gn4fBb6QpXvDE985ZvRjKy2iaWkA82z_1WVvXzsdiAQ/edit',
    'БММ': 'https://docs.google.com/spreadsheets/d/1Qg69COdDoXdClE4YThjPHW0ss13htmfx/edit',
    'СНАП': 'https://docs.google.com/spreadsheets/d/1xa-lsisslfVYGIfPL3ogBMxjBRHNhUwt/edit',
}


# Створюємо головне меню
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🌐 Сайт", "📸 Instagram")
    markup.add("📅 Розклад", "🍽 Їдальня")
    return markup


# Команда /start
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        f'Привіт, {message.from_user.first_name} {message.from_user.last_name}!\n\n'
        'Раді вітати в нашому телеграм боті! Тут ти зможеш:\n'
        '• Перейти на офіційний сайт НЛТУ\n'
        '• Переглянути Instagram університету\n'
        '• Отримати розклад занять\n\n'
        'Просто скористайся кнопками нижче ⬇️',
        reply_markup=main_menu()
    )


# Обробка кнопок з меню
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    text = message.text.strip().lower()

    if text == "🌐 сайт":
        webbrowser.open('https://nltu.edu.ua/')


    elif text == "📸 instagram":
        webbrowser.open('https://www.instagram.com/nltu_unfu/')


    elif text == "📅 розклад":
        send_faculty_choices(message)

    elif text == "🍽 їдальня":
        # Надсилаємо локацію (координати НЛТУ їдальні, можна змінити)
        bot.send_location(message.chat.id, latitude=49.82396713611374,  longitude=24.002855615057126)

        # Повідомлення з кнопкою
        msg = (
            "🍲 <b>Їдальня НЛТУ</b>\n\n"
            "Меню та акції ви можете переглядати у телеграм-каналі їдальні нашого університету."
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔗 Відкрити канал", url="https://t.me/lisoteh"))

        bot.send_message(message.chat.id, msg, parse_mode="HTML", reply_markup=markup)


# Показати кнопки факультетів
def send_faculty_choices(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for faculty in faculty_links:
        markup.add(types.KeyboardButton(faculty))
    bot.send_message(message.chat.id, "Оберіть свій факультет:", reply_markup=markup)
    bot.register_next_step_handler(message, send_schedule)


# Відправити посилання на таблицю
def send_schedule(message):
    selected = message.text.strip().upper()
    matched_faculty = None

    for faculty in faculty_links:
        if selected == faculty.upper():
            matched_faculty = faculty
            break

    if matched_faculty:
        link = faculty_links[matched_faculty]
        bot.send_message(message.chat.id, f"Ось розклад для факультету <b>{matched_faculty}</b>:\n{link}",
                         parse_mode='HTML', reply_markup=main_menu())
    else:
        bot.send_message(message.chat.id, "Невірний факультет. Спробуйте ще раз з командою /schedule.",
                         reply_markup=main_menu())


bot.polling(none_stop=True)
