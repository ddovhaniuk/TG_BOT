import telebot
import webbrowser

bot = telebot.TeleBot('7784812218:AAFrZ4D0mOC1AE4oAk9BeJFpJgRv0Tc-dWs')

@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://nltu.edu.ua/')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id,f'Привіт, {message.from_user.first_name} {message.from_user.last_name}!' ' Раді вітати в нашому телеграм боті! Тут ти зможеш знайти розклад занять для студентів НТЛУ, та інші потрібні функції. Весь список команд можеш переглянути за допомогою /commands')


bot.polling(none_stop=True)