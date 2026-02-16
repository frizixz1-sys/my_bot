import telebot
import webbrowser
import requests
from telebot import types

bot = telebot.TeleBot('8333223188:AAEBPgTSCYA8odgfCfoJEpx7xeSBV-X4uN4')
amount = 0


# ===== ИНЛАЙН-РЕЖИМ С РЕАЛЬНЫМ API =====
# Твои курсы (можешь менять цифры)
API_KEY = '14a528b05de9f38b88ae0fe1'


@bot.inline_handler(func=lambda query: True)
def inline_query(query):
    try:
        text = query.query.strip().upper()
        print(f"Запрос: {text}")

        if not text:
            r = types.InlineQueryResultArticle(
                id='1',
                title='💱 Currency Converter',
                description='Example: 100 USD to RUB',
                input_message_content=types.InputTextMessageContent(
                    'Use: 100 USD to RUB'
                )
            )
            bot.answer_inline_query(query.id, [r])
            return

        parts = text.split()

        if len(parts) == 4 and parts[2] == 'TO':
            amount = float(parts[0])
            from_curr = parts[1]
            to_curr = parts[3]

            # Получаем актуальные курсы с ТВОИМ ключом
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_curr}"
            response = requests.get(url, timeout=5)
            data = response.json()

            if data['result'] == 'success':
                if to_curr in data['conversion_rates']:
                    rate = data['conversion_rates'][to_curr]
                    result = amount * rate
                    result_text = f"💱 {amount} {from_curr} = {round(result, 2)} {to_curr}"
                else:
                    result_text = f"❌ Currency {to_curr} not found"
            else:
                result_text = "❌ API error"

            r = types.InlineQueryResultArticle(
                id='1',
                title=result_text,
                description='Click to send',
                input_message_content=types.InputTextMessageContent(result_text)
            )
            bot.answer_inline_query(query.id, [r])
        else:
            r = types.InlineQueryResultArticle(
                id='1',
                title='❌ Invalid format',
                description='Use: 100 USD to RUB',
                input_message_content=types.InputTextMessageContent('✅ Correct: 100 USD to RUB')
            )
            bot.answer_inline_query(query.id, [r])

    except Exception as e:
        print(f"Error: {e}")


print("✅ Бот с API ключом запущен...")
bot.polling(none_stop=True)
# ===== ОБЫЧНЫЙ РЕЖИМ (команды) =====
@bot.message_handler(commands=['start'])
def start_command(message):
    hide_markup = types.ReplyKeyboardRemove()
    try:
        with open("baba.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=f"It is a pleasure to meet you, {message.from_user.first_name}",
                reply_markup=hide_markup
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            f"It is a pleasure to meet you, {message.from_user.first_name}",
            reply_markup=hide_markup
        )

    bot.send_message(
        message.chat.id,
        "The bot can rate your video messages, photos, videos, documents, stickers, and more. "
        "It can also provide you with a price list for purchasing highly specialized databases.\n\n"
        "Commands:\n"
        "/start - restart\n"
        "/help - help\n"
        "/site - view a secret website\n"
        "/database - databases available\n"
        "/contacts - my contacts\n"
        "/exchange - currency converter\n\n"
        "CEO - chistakovv.t.me",
        reply_markup=hide_markup
    )


@bot.message_handler(commands=['exchange'])
def exchange(message):
    try:
        with open("kanye.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="Warm greetings, enter the amount"
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            "Warm greetings. To get started, enter the amount"
        )
    bot.register_next_step_handler(message, summa)


def summa(message):
    global amount
    try:
        amount = float(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, '❌ Invalid format, enter the amount')
        bot.register_next_step_handler(message, summa)
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
    btn2 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
    btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
    btn4 = types.InlineKeyboardButton('OTHER', callback_data='other')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, '📊 Select a currency pair', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global amount
    try:
        if call.data != 'other':
            values = call.data.upper().split('/')
            try:
                # Получаем курс через API
                url = f"https://api.exchangerate-api.com/v4/latest/{values[0]}"
                response = requests.get(url, timeout=5)
                data = response.json()
                rate = data['rates'][values[1]]
                result = amount * rate
                bot.send_message(
                    call.message.chat.id,
                    f'✅ {amount} {values[0]} = {round(result, 2)} {values[1]}'
                )
            except:
                # Запасной вариант
                rates = {'USD': 1.0, 'RUB': 90.0, 'EUR': 0.92, 'GBP': 0.79}
                if values[0] in rates and values[1] in rates:
                    result = amount / rates[values[0]] * rates[values[1]]
                    bot.send_message(
                        call.message.chat.id,
                        f'✅ {amount} {values[0]} ≈ {round(result, 2)} {values[1]} (approx)'
                    )
                else:
                    bot.send_message(
                        call.message.chat.id,
                        f'❌ Rate unavailable'
                    )
        else:
            bot.send_message(
                call.message.chat.id,
                '✏️ Enter a currency pair (e.g., EUR/GBP, JPY/USD, CHF/RUB):'
            )
            bot.register_next_step_handler(call.message, process_other_currency)
    except Exception as e:
        bot.send_message(
            call.message.chat.id,
            f'❌ Error: {e}'
        )


def process_other_currency(message):
    global amount
    try:
        text = message.text.strip().upper()

        if '/' not in text:
            bot.send_message(
                message.chat.id,
                '❌ Invalid format. Use slash: USD/EUR'
            )
            bot.register_next_step_handler(message, process_other_currency)
            return

        values = text.split('/')

        if len(values) != 2:
            bot.send_message(
                message.chat.id,
                '❌ Invalid format. Use: USD/EUR'
            )
            bot.register_next_step_handler(message, process_other_currency)
            return

        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{values[0]}"
            response = requests.get(url, timeout=5)
            data = response.json()
            rate = data['rates'][values[1]]
            result = amount * rate
            bot.send_message(
                message.chat.id,
                f'✅ {amount} {values[0]} = {round(result, 2)} {values[1]}'
            )
        except:
            bot.send_message(
                message.chat.id,
                f'❌ Rate temporarily unavailable'
            )

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f'❌ Error: {e}'
        )
        bot.register_next_step_handler(message, process_other_currency)


# ===== ОСТАЛЬНЫЕ КОМАНДЫ =====
@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        with open("jep.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="Is there an error in the bot? Contact me on Telegram chistakovv.t.me"
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            'Is there an error in the bot? Contact me on Telegram chistakovv.t.me'
        )


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open_new('https://contract.gosuslugi.ru/')


@bot.message_handler(commands=['database'])
def database_command(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Availability')
    btn2 = types.KeyboardButton('Buy')
    btn3 = types.KeyboardButton('Back')
    markup.add(btn1, btn2)
    markup.add(btn3)

    definition_text = """A database is an organized electronic information storage system that allows for the convenient storage, structure, search, modification, and analysis of data. It is used to manage large volumes of information—from user and order lists to complex government and corporate systems."""

    try:
        with open("database.png", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=definition_text,
                reply_markup=markup
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            definition_text,
            reply_markup=markup
        )


@bot.message_handler(func=lambda message: message.text == 'Availability')
def show_databases(message):
    databases_text = """🇷🇺 Russia
FR [ 1995 - 2021 ];
ADIS [ 2021 ];
CCM MIA [ 2019 - 2022 ];
STSI [ 1998 - 2005 ];
BO [ 2022 - 2025 ];
FSB [ 2017 - 2025 ];
UFSB [ 2015 - 2024 ];
ESIA [ 2023 ]
HCS [ 2018 - 2024 ];
USRNE [ 2000 - 2025 ];
UGISZ [ 2014 ];
NSPK [ 2015 - 2017 ];
UMVD [ 2019 ];

🇰🇿 Kazakhstan
ACS MIA [ 2021 - 2022 ];
CBR [ 2022 ];
EBG [ 2000- 2012 ];
BB [ 2023 ];

🇧🇾 Belarus
ACS MIA [ 2016 - 2020 ];
CBP [ 2020 - 2025 ];
BG [ 2014 - 2017 ];

🇺🇦 Ukraine
UMVD [ 2000 - 2016 ];
EBR [ 2005 - 2023 ];
KR [ 2009 - 2022 ];
BPS [ 2023 - 2025 ];

🇺🇸 USA
FBI [ 2000 ];
NCIC [ 2017 - 2021 ];
CJIS [ 2022 - 2023 ];
NICS [ 2006 ];
DHS [ 2002 ];
USMS [ 2019 ];

🇵🇱 Poland
KGP [ 2019 - 2021 ];
KSIP [ 2001 - 2007 ];
SG [ 2006 - 2015 ];
ABW [ 2014 - 2017 ];"""

    try:
        with open("data.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=databases_text
            )
    except FileNotFoundError:
        bot.send_message(message.chat.id, databases_text)


@bot.message_handler(func=lambda message: message.text == 'Buy')
def buy_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Availability')
    btn2 = types.KeyboardButton('Buy')
    btn3 = types.KeyboardButton('Back')
    markup.add(btn1, btn2)
    markup.add(btn3)

    try:
        with open("Админ.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=f"Contact before purchasing - @Chistakovv, {message.from_user.first_name}",
                reply_markup=markup
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            f"Contact before purchasing - @Chistakovv, {message.from_user.first_name}",
            reply_markup=markup
        )


@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    bot.send_message(message.chat.id, "⚡️ Back to the beginning...")
    start_command(message)


@bot.message_handler(content_types=['photo', 'sticker', 'video', 'document', 'audio', 'voice'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'sent to the site',
        url='https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices'
    ))
    bot.reply_to(message, 'The file has been successfully saved to the server...', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Приветствую, {message.from_user.first_name}')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID: {message.from_user.id}')


if __name__ == '__main__':
    print("✅ Бот с реальным API запущен...")
    print("👉 Инлайн: @chistakovbot 100 USD to RUB")
    bot.polling(none_stop=True)