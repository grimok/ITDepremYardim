import time
from datetime import datetime
import telebot
import threading

import data
import textdetection
from sheetsapi import table

adresler = []

API_KEY = '5963282287:AAEwHSvulUKIFMU_gGQ5vX3cXVHQmOuWALQ'

bot = telebot.TeleBot(API_KEY, threaded=False)

sheetcontroler = table()

@bot.message_handler(func=lambda message: message.chat.type == 'group', content_types=['photo'])
def echo_message(message):

    name = message.from_user.first_name
    if name is None:
        name = "Anonym" + str(id)
    last = message.from_user.last_name
    if last is None:
        last = ""

    bot.reply_to(message, '#id' + str(message.chat.id))
    fileID = message.photo[-1].file_id
    bot.reply_to(message, '#fileid' + str(message.photo[-1].file_id))
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open(str(message.chat.id) + ".jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, 'Başvurunuz alındı. Lütfen beklemeye devam edin.')

    textdetection.read_text(str(message.chat.id) + ".jpg", str(message.chat.id))

    caption = message.caption

    if message.caption is None:
        total_name = name + " " + last
    else:
        total_name = str(message.caption)

    read = ""
    builder = ""
    status = ""
    with open(str(message.chat.id) + ".txt", "r") as f:
        read = f.read()
        array = read.lower().split("\n")
        for x in array:
            if x.__contains__("mah") or x.__contains__("sok") or x.__contains__("site") or x.__contains__(
                    "sitesi") or x.__contains__("no:") or x.__contains__("soka") or x.__contains__("blok") \
                    or x.__contains__("adiyaman") or x.__contains__("karhramanmaras") or x.__contains__(
                "hatay") or x.__contains__("antakya") or x.__contains__("cadde") or x.__contains__("cad") \
                    or x.__contains__("ap.") or x.__contains__("apartman") or x.__contains__("kat"):
                if x.__contains__("@"):
                    continue
                builder = builder + x + " "

            if x.__contains__("enkaz") or x.__contains__("gocuk") or x.__contains__("altinda") or x.__contains__(
                    "kazma") or x.__contains__("enkazin") or x.__contains__("gocukte") or x.__contains__("makinasi") or x.__contains__("makina"):
                status = "acil"
            else:
                status = "yemek"


    returning = builder
    builder = ""
    if not (returning == ""):
        if not(adresler.__contains__(returning)):
            bot.send_message(message.chat.id,
                             "📍 [" + returning + "\b].\n\n✅ Başvurunuz Tamamlanmıştır! \n\n❔Okunan adreste yanlışlıklar olabilir. Tüm adresler ekip arkadaşlarımız"
                                                 " ve sistem üzerinden kontrol edilip düzenlenmektedir. Eğer herhangi bir sorun yaşarsanız lütfen bize "
                                                 "contact@neostellar.net üzerinden ulaşın.\n\n📍 Başvurulan kişi: " + total_name)
            sheetcontroler.updateTable("A" + str(data.get_data()),
                                       [[total_name, returning, "", "",
                                         "", "", "", "", "", "Bekleniyor"]])
            adresler.append(returning)
            returning = ""
            status = ""
        else:
            bot.send_message(message.chat.id,
                             "📍Üzgünüm, ancak bu adrese kayıt oluşturulmuş.")

    else:
        bot.send_message(message.chat.id,
                         "📍Üzgünüm, ancak herhangi bir adress tespit edemedim.")
        read = ""
        builder = ""


@bot.message_handler(func=lambda message: message.chat.type == 'private')
def echo_message(message):
    bot.send_message(message.chat.id,
                     "📍Merhaba, ben Deprem Bot! Bana içinde aciliyeti olan bir deprem adresi bulunan fotoğraf gönderebilirsin. "
                     "Amacım bu fotoğraftaki adresi algılayıp yardım göndermektir. Lütfen sadece fotoğraf gönderiniz.")


bot.polling()
