@bot.message_handler(commands=['start'])
def start_command(message):
    # Удаляем сообщение пользователя
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    # Отправляем фото
    try:
        with open("baba.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption=f"It is a pleasure to meet you, {message.from_user.first_name}"
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            f"It is a pleasure to meet you, {message.from_user.first_name}"
        )

    # Отправляем список команд
    bot.send_message(
        message.chat.id,
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

@bot.message_handler(commands=['help'])
def help_command(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    try:
        with open("jep.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="Is there an error? Contact me on Telegram @chistakovv"
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            'Is there an error? Contact me on Telegram @chistakovv'
        )

@bot.message_handler(commands=['site', 'website'])
def site(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton(
        text="🔗 Click to continue",
        url="https://contract.gosuslugi.ru/"
    )
    markup.add(btn)
    
    bot.send_message(
        message.chat.id,
        "🌐 Click the button below to visit the website:",
        reply_markup=markup
    )

@bot.message_handler(commands=['database'])
def database_command(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
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

@bot.message_handler(commands=['contacts'])
def contacts_command(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    inline_markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Telegram', url='https://t.me/chistakovv')
    inline_markup.row(btn1)
    btn2 = types.InlineKeyboardButton('VK', url='https://vk.com/outnrss')
    btn3 = types.InlineKeyboardButton('Mail', url='https://mail.google.com/mail/?view=cm&to=outnrss@vk.com')
    inline_markup.row(btn2, btn3)

    try:
        with open("ggsell.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="My contacts:",
                reply_markup=inline_markup
            )
    except FileNotFoundError:
        bot.send_message(message.chat.id, "My contacts:", reply_markup=inline_markup)

@bot.message_handler(commands=['exchange'])
def exchange(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    try:
        with open("kanye.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="Welcome to Currency Converter!\n\nEnter the amount:"
            )
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Welcome to Currency Converter!\n\nEnter the amount:")
    bot.register_next_step_handler(message, summa)

@bot.message_handler(func=lambda message: message.text == 'Availability')
def show_databases(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    # Сначала отправляем фото с подписью
    try:
        with open("data.jpg", "rb") as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="📋 <b>Available Databases</b>",
                parse_mode='HTML'
            )
    except FileNotFoundError:
        bot.send_message(
            message.chat.id,
            "📋 <b>Available Databases</b>",
            parse_mode='HTML'
        )
    
    # Отправляем список
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
        message.chat.id,
        databases_text,
        parse_mode='HTML'
    )

@bot.message_handler(func=lambda message: message.text == 'Buy')
def buy_handler(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
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
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass
    
    hide_markup = types.ReplyKeyboardRemove()
    bot.send_message(
        message.chat.id,
        "⚡️ Back to the beginning...",
        reply_markup=hide_markup
    )
    start_command(message)
