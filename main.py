import telebot
import requests
import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from telebot import types

# ===== CONFIGURATION =====
BOT_TOKEN = '8333223188:AAEBPgTSCYA8odgfCfoJEpx7xeSBV-X4uN4'
API_KEY = '14a528b05de9f38b88ae0fe1'

bot = telebot.TeleBot(BOT_TOKEN)

# Хранилище для отслеживания первого запуска и ID сообщений от /start
first_start_done = {}
start_message_ids = {}  # ID сообщений от /start, которые нельзя удалять
last_message_id = {}     # ID последних сообщений для удаления

# ===== WEBHOOK HANDLER =====
class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            update = telebot.types.Update.de_json(post_data.decode('utf-8'))
            
            # Отправляем обновление боту
            bot.process_new_updates([update])
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'OK')
        except Exception as e:
            print(f"❌ Webhook error: {e}")
            self.send_response(500)
            self.end_headers()
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running with webhook')

def run_webhook_server():
    port = int(os.environ.get('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    print(f"🌐 Webhook server on port {port}")
    server.serve_forever()


# ===== ВСПОМОГАТЕЛЬНАЯ ФУНКЦИЯ ДЛЯ УДАЛЕНИЯ =====
def delete_previous_message(chat_id):
    # Проверяем, можно ли удалять сообщение (не из /start)
    if chat_id in last_message_id:
        # Проверяем, не является ли это сообщение от /start
        if chat_id in start_message_ids and last_message_id[chat_id] in start_message_ids[chat_id]:
            print(f"⏭️ Пропускаем удаление сообщения от /start: {last_message_id[chat_id]}")
            return
        
        try:
            bot.delete_message(chat_id, last_message_id[chat_id])
            print(f"✅ Удалено сообщение: {last_message_id[chat_id]}")
        except Exception as e:
            print(f"❌ Не удалось удалить: {e}")


# ===== ОБРАБОТЧИКИ КОМАНД =====
@bot.message_handler(commands=['start'])
def start_command(message):
    chat_id = message.chat.id
    
    # Инициализируем хранилище для этого пользователя, если его нет
    if chat_id not in start_message_ids:
        start_message_ids[chat_id] = []
    
    # Проверяем, первый ли это запуск
    if chat_id not in first_start_done:
        print(f"🚀 Первый запуск для пользователя {chat_id}")
        
        # Удаляем сообщение пользователя с командой /start
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        # Отправляем фото
        try:
            with open("baba.jpg", "rb") as photo:
                sent_photo = bot.send_photo(
                    chat_id,
                    photo,
                    caption=f"It is a pleasure to meet you, {message.from_user.first_name}"
                )
                # Сохраняем ID сообщения от /start
                start_message_ids[chat_id].append(sent_photo.message_id)
                # Закрепляем сообщение
                try:
                    bot.pin_chat_message(chat_id, sent_photo.message_id)
                    print(f"✅ Сообщение закреплено: {sent_photo.message_id}")
                except:
                    print(f"❌ Не удалось закрепить сообщение")
        except FileNotFoundError:
            sent_text = bot.send_message(
                chat_id,
                f"It is a pleasure to meet you, {message.from_user.first_name}"
            )
            start_message_ids[chat_id].append(sent_text.message_id)
            try:
                bot.pin_chat_message(chat_id, sent_text.message_id)
            except:
                pass

        # Отправляем список команд
        sent_commands = bot.send_message(
            chat_id,
            "I can provide you with a price list for purchasing highly specialized databases.\n\n"
            "Commands:\n"
            "/start - restart\n"
            "/help - help\n"
            "/site - visit website\n"
            "/database - available databases\n"
            "/contacts - my contacts\n"
            "/exchange - currency converter\n\n"
            "CEO - @chistakovv"
        )
        # Сохраняем ID сообщения от /start
        start_message_ids[chat_id].append(sent_commands.message_id)
        
        # Сохраняем информацию о первом запуске
        first_start_done[chat_id] = True
    else:
        print(f"🔄 Повторный запуск для пользователя {chat_id}")
        
        # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
        delete_previous_message(chat_id)
        
        # Удаляем сообщение пользователя с командой
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        # Отправляем фото
        try:
            with open("baba.jpg", "rb") as photo:
                bot.send_photo(
                    chat_id,
                    photo,
                    caption=f"It is a pleasure to meet you, {message.from_user.first_name}"
                )
        except FileNotFoundError:
            bot.send_message(
                chat_id,
                f"It is a pleasure to meet you, {message.from_user.first_name}"
            )

        # Отправляем список команд
        sent_commands = bot.send_message(
            chat_id,
            "I can provide you with a price list for purchasing highly specialized databases.\n\n"
            "Commands:\n"
            "/start - restart\n"
            "/help - help\n"
            "/site - visit website\n"
            "/database - available databases\n"
            "/contacts - my contacts\n"
            "/exchange - currency converter\n\n"
            "CEO - @chistakovv"
        )
        
        # Сохраняем ID нового сообщения для последующего удаления
        last_message_id[chat_id] = sent_commands.message_id


@bot.message_handler(commands=['database'])
def database_command(message):
    chat_id = message.chat.id
    
    # Проверяем, был ли уже первый запуск
    if chat_id not in first_start_done:
        bot.send_message(chat_id, "Please use /start first to initialize the bot.")
        return
    
    # НЕ удаляем сообщение пользователя с /database
    # НЕ удаляем предыдущие сообщения бота
    
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Availability')
    btn2 = types.KeyboardButton('Buy')
    btn3 = types.KeyboardButton('Back')
    markup.add(btn1, btn2)
    markup.add(btn3)

    definition_text = """A database is an organized electronic information storage system that allows for the convenient storage, structure, search, modification, and analysis of data. It is used to manage large volumes of information—from user and order lists to complex government and corporate systems."""

    # Отправляем фото с определением и клавиатурой
    try:
        with open("database.png", "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption=definition_text,
                reply_markup=markup
            )
    except FileNotFoundError:
        bot.send_message(
            chat_id,
            definition_text,
            reply_markup=markup
        )
    
    # НЕ сохраняем ID для удаления


@bot.message_handler(func=lambda message: message.text == 'Availability')
def handle_availability(message):
    chat_id = message.chat.id
    
    # Проверяем, был ли уже первый запуск
    if chat_id not in first_start_done:
        bot.send_message(chat_id, "Please use /start first to initialize the bot.")
        return
    
    # НЕ удаляем сообщение пользователя с кнопкой
    # НЕ удаляем предыдущие сообщения бота
    
    # Отправляем фото с подписью
    try:
        with open("data.jpg", "rb") as photo:
            bot.send_photo(
                chat_id,
                photo,
                caption="📋 <b>Available Databases</b>",
                parse_mode='HTML'
            )
    except FileNotFoundError:
        bot.send_message(
            chat_id,
            "📋 <b>Available Databases</b>",
            parse_mode='HTML'
        )
    
    # Отправляем большой список
    databases_text = """<b>───── 🇷🇺 RUSSIA ─────</b>
• FR [1995-2021]
• ADIS [2021]
• CCM MIA [2019-2022]
• STSI [1998-2005]
• BO [2022-2025]
• FSB [2017-2025]
• UFSB [2015-2024]
• ESIA [2023]
• HCS [2018-2024]
• USRNE [2000-2025]
• UGISZ [2014]
• NSPK [2015-2017]
• UMVD [2019]

<b>───── 🇰🇿 KAZAKHSTAN ─────</b>
• ACS MIA [2021-2022]
• CBR [2022]
• EBG [2000-2012]
• BB [2023]

<b>───── 🇧🇾 BELARUS ─────</b>
• ACS MIA [2016-2020]
• CBP [2020-2025]
• BG [2014-2017]

<b>───── 🇺🇦 UKRAINE ─────</b>
• UMVD [2000-2016]
• EBR [2005-2023]
• KR [2009-2022]
• BPS [2023-2025]

<b>───── 🇺🇸 USA ─────</b>
• FBI [2000]
• NCIC [2017-2021]
• CJIS [2022-2023]
• NICS [2006]
• DHS [2002]
• USMS [2019]

<b>───── 🇵🇱 POLAND ─────</b>
• KGP [2019-2021]
• KSIP [2001-2007]
• SG [2006-2015]
• ABW [2014-2017]"""

    bot.send_message(
        chat_id,
        databases_text,
        parse_mode='HTML'
    )
    
    # НЕ сохраняем ID для удаления


# ===== ВСЕ ОСТАЛЬНЫЕ КОМАНДЫ (БУДУТ УДАЛЯТЬСЯ) =====
@bot.message_handler(commands=['help', 'site', 'website', 'contacts', 'exchange'])
def other_commands(message):
    chat_id = message.chat.id
    
    # Проверяем, был ли уже первый запуск
    if chat_id not in first_start_done:
        bot.send_message(chat_id, "Please use /start first to initialize the bot.")
        return
    
    # Удаляем сообщение пользователя
    try:
        bot.delete_message(chat_id, message.message_id)
        print(f"✅ Удалено сообщение пользователя: {message.message_id}")
    except:
        pass
    
    # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
    delete_previous_message(chat_id)
    
    # Обрабатываем команды
    if message.text == '/help':
        try:
            with open("jep.jpg", "rb") as photo:
                sent = bot.send_photo(
                    chat_id,
                    photo,
                    caption="Is there an error? Contact me on Telegram @chistakovv"
                )
                last_message_id[chat_id] = sent.message_id
        except FileNotFoundError:
            sent = bot.send_message(
                chat_id,
                'Is there an error? Contact me on Telegram @chistakovv'
            )
            last_message_id[chat_id] = sent.message_id
            
    elif message.text in ['/site', '/website']:
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton(
            text="🔗 Click to continue",
            url="https://contract.gosuslugi.ru/"
        )
        markup.add(btn)
        
        sent = bot.send_message(
            chat_id,
            "🌐 Click the button below to visit the website:",
            reply_markup=markup
        )
        last_message_id[chat_id] = sent.message_id
            
    elif message.text == '/contacts':
        inline_markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Telegram', url='https://t.me/chistakovv')
        inline_markup.row(btn1)
        btn2 = types.InlineKeyboardButton('VK', url='https://vk.com/outnrss')
        btn3 = types.InlineKeyboardButton('Mail', url='https://mail.google.com/mail/?view=cm&to=outnrss@vk.com')
        inline_markup.row(btn2, btn3)

        try:
            with open("ggsell.jpg", "rb") as photo:
                sent = bot.send_photo(
                    chat_id,
                    photo,
                    caption="My contacts:",
                    reply_markup=inline_markup
                )
                last_message_id[chat_id] = sent.message_id
        except FileNotFoundError:
            sent = bot.send_message(chat_id, "My contacts:", reply_markup=inline_markup)
            last_message_id[chat_id] = sent.message_id
            
    elif message.text == '/exchange':
        try:
            with open("kanye.jpg", "rb") as photo:
                sent = bot.send_photo(
                    chat_id,
                    photo,
                    caption="Welcome to Currency Converter!\n\nEnter the amount:"
                )
                last_message_id[chat_id] = sent.message_id
        except FileNotFoundError:
            sent = bot.send_message(
                chat_id,
                "Welcome to Currency Converter!\n\nEnter the amount:"
            )
            last_message_id[chat_id] = sent.message_id
        bot.register_next_step_handler(message, process_amount)


# ===== КНОПКА BUY (ТОЖЕ БУДЕТ УДАЛЯТЬСЯ) =====
@bot.message_handler(func=lambda message: message.text == 'Buy')
def buy_handler(message):
    chat_id = message.chat.id
    
    # Проверяем, был ли уже первый запуск
    if chat_id not in first_start_done:
        bot.send_message(chat_id, "Please use /start first to initialize the bot.")
        return
    
    # Удаляем сообщение пользователя с кнопкой
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
    delete_previous_message(chat_id)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Availability')
    btn2 = types.KeyboardButton('Buy')
    btn3 = types.KeyboardButton('Back')
    markup.add(btn1, btn2)
    markup.add(btn3)

    try:
        with open("Админ.jpg", "rb") as photo:
            sent = bot.send_photo(
                chat_id,
                photo,
                caption=f"Contact before purchasing - @Chistakovv, {message.from_user.first_name}",
                reply_markup=markup
            )
            last_message_id[chat_id] = sent.message_id
    except FileNotFoundError:
        sent = bot.send_message(
            chat_id,
            f"Contact before purchasing - @Chistakovv, {message.from_user.first_name}",
            reply_markup=markup
        )
        last_message_id[chat_id] = sent.message_id


# ===== КНОПКА BACK (ТОЖЕ БУДЕТ УДАЛЯТЬСЯ) =====
@bot.message_handler(func=lambda message: message.text == 'Back')
def back_handler(message):
    chat_id = message.chat.id
    
    # Проверяем, был ли уже первый запуск
    if chat_id not in first_start_done:
        bot.send_message(chat_id, "Please use /start first to initialize the bot.")
        return
    
    # Удаляем сообщение пользователя с кнопкой
    try:
        bot.delete_message(chat_id, message.message_id)
    except:
        pass
    
    # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
    delete_previous_message(chat_id)
    
    hide_markup = types.ReplyKeyboardRemove()
    sent = bot.send_message(
        chat_id,
        "⚡️ Back to the beginning...",
        reply_markup=hide_markup
    )
    last_message_id[chat_id] = sent.message_id
    start_command(message)


# ===== КОНВЕРТЕР ВАЛЮТ =====
amount = 0

def process_amount(message):
    global amount
    chat_id = message.chat.id
    
    try:
        # Пробуем преобразовать ввод в число
        amount = float(message.text.strip().replace(',', '.'))
        
        # Удаляем сообщение пользователя с суммой
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
        delete_previous_message(chat_id)
        
        # Создаем клавиатуру с кнопками выбора валют
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
        btn2 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
        btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
        btn4 = types.InlineKeyboardButton('OTHER', callback_data='other')
        markup.add(btn1, btn2, btn3, btn4)
        
        sent = bot.send_message(
            chat_id,
            f"💰 Amount: {amount}\n\nSelect a currency pair:",
            reply_markup=markup
        )
        last_message_id[chat_id] = sent.message_id
        
    except ValueError:
        # Если ввод не число
        error_msg = bot.send_message(chat_id, "❌ Please enter a valid number (e.g., 100 or 100.50)")
        last_message_id[chat_id] = error_msg.message_id
        bot.register_next_step_handler(message, process_amount)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    global amount
    chat_id = call.message.chat.id
    
    try:
        if call.data != 'other':
            values = call.data.upper().split('/')
            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{values[0]}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data['result'] == 'success':
                rate = data['conversion_rates'][values[1]]
                result = amount * rate
                
                # Удаляем сообщение с кнопками (если это не от /start)
                delete_previous_message(chat_id)
                
                # Создаем новые кнопки для продолжения
                markup = types.InlineKeyboardMarkup(row_width=2)
                btn1 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
                btn2 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
                btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
                btn4 = types.InlineKeyboardButton('OTHER', callback_data='other')
                markup.add(btn1, btn2, btn3, btn4)
                
                sent = bot.send_message(
                    chat_id,
                    f"✅ {amount} {values[0]} = {round(result, 2)} {values[1]}\n\n💰 Amount: {amount}\n\nSelect another currency pair:",
                    reply_markup=markup
                )
                last_message_id[chat_id] = sent.message_id
            else:
                bot.send_message(chat_id, "❌ API Error")
        else:
            # OTHER - пользователь вводит свою пару
            delete_previous_message(chat_id)
            sent = bot.send_message(
                chat_id,
                "✏️ Enter currency pair (e.g., EUR/GBP, JPY/USD):"
            )
            last_message_id[chat_id] = sent.message_id
            bot.register_next_step_handler(call.message, process_other_currency)
            
        bot.answer_callback_query(call.id)
    except Exception as e:
        bot.answer_callback_query(call.id)
        error_msg = bot.send_message(chat_id, f"❌ Error: {e}")
        last_message_id[chat_id] = error_msg.message_id


def process_other_currency(message):
    global amount
    chat_id = message.chat.id
    
    try:
        text = message.text.strip().upper()
        
        # Удаляем сообщение пользователя
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
        
        if '/' not in text:
            error_msg = bot.send_message(chat_id, "❌ Use slash: USD/EUR")
            last_message_id[chat_id] = error_msg.message_id
            bot.register_next_step_handler(message, process_other_currency)
            return

        values = text.split('/')
        if len(values) != 2:
            error_msg = bot.send_message(chat_id, "❌ Use: USD/EUR")
            last_message_id[chat_id] = error_msg.message_id
            bot.register_next_step_handler(message, process_other_currency)
            return

        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{values[0]}"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        if data['result'] == 'success':
            rate = data['conversion_rates'][values[1]]
            result = amount * rate
            
            # Удаляем предыдущее сообщение (если это не от /start)
            delete_previous_message(chat_id)
            
            # Создаем новые кнопки
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton('USD/RUB', callback_data='usd/rub')
            btn2 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd')
            btn3 = types.InlineKeyboardButton('USD/GBP', callback_data='usd/gbp')
            btn4 = types.InlineKeyboardButton('OTHER', callback_data='other')
            markup.add(btn1, btn2, btn3, btn4)
            
            sent = bot.send_message(
                chat_id,
                f"✅ {amount} {values[0]} = {round(result, 2)} {values[1]}\n\n💰 Amount: {amount}\n\nSelect another currency pair:",
                reply_markup=markup
            )
            last_message_id[chat_id] = sent.message_id
        else:
            bot.send_message(chat_id, "❌ API Error")
            
    except Exception as e:
        error_msg = bot.send_message(chat_id, f"❌ Error: {e}")
        last_message_id[chat_id] = error_msg.message_id
        bot.register_next_step_handler(message, process_other_currency)


# ===== INLINE MODE =====
@bot.inline_handler(func=lambda query: True)
def inline_query(query):
    try:
        text = query.query.strip().upper()
        print(f"📩 Inline request: {text}")

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

            url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_curr}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if data['result'] == 'success' and to_curr in data['conversion_rates']:
                rate = data['conversion_rates'][to_curr]
                result = amount * rate
                result_text = f"💱 {amount} {from_curr} = {round(result, 2)} {to_curr}"
            else:
                result_text = f"❌ Error"

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
        print(f"❌ Inline error: {e}")


# ===== CONTENT HANDLERS =====
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'voice'])
def get_file(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        'Sent to the site',
        url='https://www.interpol.int/How-we-work/Notices/Red-Notices/View-Red-Notices'
    ))
    bot.reply_to(message, 'The file has been successfully saved to the server...', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def info(message):
    chat_id = message.chat.id
    
    # Игнорируем команды и кнопки, которые уже обработаны
    if message.text.startswith('/') or message.text in ['Availability', 'Buy', 'Back']:
        return
        
    if message.text.lower() == 'hello':
        # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
        delete_previous_message(chat_id)
        
        # Удаляем сообщение пользователя
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
            
        sent = bot.send_message(chat_id, f'Hello, {message.from_user.first_name}!')
        last_message_id[chat_id] = sent.message_id
    elif message.text.lower() == 'id':
        # Удаляем предыдущее сообщение бота (кроме сообщений от /start)
        delete_previous_message(chat_id)
        
        # Удаляем сообщение пользователя
        try:
            bot.delete_message(chat_id, message.message_id)
        except:
            pass
            
        sent = bot.send_message(chat_id, f'Your ID: {message.from_user.id}')
        last_message_id[chat_id] = sent.message_id


# ===== START =====
if __name__ == '__main__':
    import threading
    import time
    
    print("=" * 50)
    print("✅ Starting bot with webhook...")
    
    # Запускаем веб-сервер в отдельном потоке
    server_thread = threading.Thread(target=run_webhook_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    
    # Получаем URL сервиса
    render_url = os.environ.get('RENDER_EXTERNAL_URL')
    if not render_url:
        render_url = f"https://{os.environ.get('RENDER_SERVICE_NAME', 'localhost')}.onrender.com"
    
    webhook_url = f"{render_url}/webhook"
    print(f"🔗 Setting webhook to: {webhook_url}")
    
    # Устанавливаем вебхук
    bot.remove_webhook()
    time.sleep(1)
    bot.set_webhook(url=webhook_url)
    
    print(f"✅ Webhook set successfully")
    print(f"📱 Bot is running with webhook")
    print("=" * 50)
    
    # Держим главный поток активным
    while True:
        time.sleep(60)
