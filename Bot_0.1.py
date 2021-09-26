import telebot
from telebot import types
import pymysql
sql = "SELECT name FROM main"#Получение словаря имён
sql4 = "SELECT id FROM customers"#Для получения всех айди
connection = pymysql.connect(host='127.0.0.1',
                             user='root',
                             password='55ufufun',                             
                             db='lol',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor) 
print ("connect successful!!")

token = "1409945611:AAEqZPVb2aICD006EyryAN0u1z3evU0Y3SQ"
bot = telebot.TeleBot(token)
sticker = open("D:\St\sticker.webp", 'rb')
@bot.message_handler(commands=['start'])
def start(message):
    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("😊 Як справи?")
    #item2 = types.KeyboardButton("Ввести имя чемпиона")
    item3 = types.KeyboardButton("Хто є найпопулярнішим чемпіоном?")
    markup.add(item1, item3)#item2,
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Привіт, {0.first_name}!\nМене звуть <b>{1.first_name}</b>.\nВведи чемпіона, за якого ти б хотів проголосувати(який, на твою думку, є найкращим у даний момент)"
                     .format(message.from_user, bot.get_me()), parse_mode='html',reply_markup=markup)
@bot.message_handler(content_types=['text'])
def answer(message):
    string1=message.text
    checker=False
    try:
     with connection.cursor() as cursor:
        sql5="insert customers values("+str(message.from_user.id)+",0);"   
        cursor.execute(sql4)
        new_cust=True
        for row in cursor:
            print(message.from_user.id)
            print(row['id'])
            if row['id']==message.from_user.id:
                new_cust=False
        if new_cust==True:
            cursor.execute(sql5)
            connection.commit()
    except Exception as e:
                    print(repr(e))
    if message.chat.type == 'private':
            if message.text == 'Привіт':
                checker = True
                bot.send_sticker(message.chat.id, sticker)
                bot.send_message(message.chat.id, "Привіт)")
            if message.text == '😊 Як справи?': 
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Гарно", callback_data='good')
                item2 = types.InlineKeyboardButton("Не дуже(", callback_data='bad')
 
                markup.add(item1, item2)
                bot.send_message(message.chat.id, 'Нормально, дані збираю, а ти як?', reply_markup=markup)
            elif message.text == 'Хто є найпопулярнішим чемпіоном?': 
                try: 
                    with connection.cursor() as cursor:
                        sq="SET @a:=0;"
                        cursor.execute(sq) 
                        connection.commit()
                        sq1="SET @b:=0;"
                        cursor.execute(sq1) 
                        connection.commit()
                        sq3="SELECT max(sum) into @a FROM main;"
                        cursor.execute(sq3) 
                        connection.commit()
                        sql8="SELECT SUM(sum) into @b FROM main;"
                        cursor.execute(sql8)
                        connection.commit()
                        sql3 = "SELECT name FROM main WHERE main.sum=@a;"#Возвращает имя
                        cursor.execute(sql3)
                        for row in cursor:
                            bot.send_message(message.chat.id, "На данний час найбільш популярним чемпіоном є "+row['name'])
                        #Проценты
                        slqper="UPDATE main SET lastmean = @a/@b WHERE id=1"
                        sqlget="SELECT lastmean FROM main WHERE id=1"
                        cursor.execute(slqper)
                        connection.commit()
                        cursor.execute(sqlget)
                        for row in cursor:
                            per=int(float(row['lastmean'])*100)
                            bot.send_message(message.chat.id, "Відсоток його вибору становить:"+str(per)+"%")
                except Exception as e:
                    print(repr(e))
            else:
                try: 
                    with connection.cursor() as cursor:
                        cursor.execute("set SQL_SAFE_UPDATES = 0;")
                        sql1 = "UPDATE main SET sum = sum+1 WHERE name="+"'"+message.text+"'"+";"#Добавляет 1 голос   
                        sql7 = "UPDATE customers SET state = 1 WHERE id="+str(message.from_user.id)+";"#Изменяет  булевый параметр
                        cursor.execute(sql)                               
                        for row in cursor:
                            if row['name']==string1.strip():
                                sql6="SELECT state FROM customers WHERE id ="+str(message.from_user.id)+";"
                                cursor.execute(sql6)
                                checker=True
                                for row in cursor:
                                    if row['state']==0:
                                        cursor.execute(sql7)
                                        connection.commit()
                                        cursor.execute(sql1)
                                        connection.commit()
                                        bot.send_message(message.chat.id, 'Ок, твій голос зараховано')
                                    else:
                                        bot.send_message(message.chat.id, 'Ти вже голосував')                            
                        if checker == False:
                            bot.send_message(message.chat.id, 'Ти шось не те написав)')
                except Exception as e:
                    print(repr(e))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Це добре)')
            elif call.data == 'bad':            
                bot.send_message(call.message.chat.id, 'Шкода(')
 
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="😊 Як справи?",
                reply_markup=None)
    except Exception as e:
        print(repr(e))
bot.polling(none_stop=True)

