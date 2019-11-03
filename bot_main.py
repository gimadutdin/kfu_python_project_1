import telebot, sqlite3

bot = telebot.TeleBot('1061478384:AAG4tawKAjUiTZ_59uEhUptfdSkd7nlxtDM')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветствует бот! /help - помощь по командам')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/login_stud фио, номер_зачетки - вход для студента')



@bot.message_handler(commands=['login_stud'])
def login_stud_message(message):
    #print('Helo world!')
    arr = message.text.split(' ')
    fio = arr[1] + ' ' + arr[2] + ' ' + arr[3]
    num_zach = arr[4]
    print(fio, num_zach, end = '\n')
    ans = ''
    
    conn = sqlite3.connect("bot_database.db")
    cursor = conn.cursor()
    sel_res = cursor.execute('SELECT * FROM students WHERE fio=? and num_zach=?', (fio, int(num_zach)))
    
    print(cursor.fetchone())
    if cursor.fetchone() != None:
        ans = 'Найден'
    else:
        ans = 'НЕ найден'
    cursor.close()
    conn.close()
        
    bot.send_message(message.chat.id, ans)

@bot.message_handler(content_types=['text'])
def send_text(message):
    json = yandex_translate_text(message.text)
    bot.send_message(message.chat.id, ''.join(json["text"]))



################################################################
if __name__ == "__main__":
    conn = sqlite3.connect("bot_database.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute("""CREATE TABLE if not exists students
                      (id integer primary key,
                       fio text,
                       num_zach integer)
                   """)

    conn.commit()

    stud = [('Альбертов Альберт Альбертович', 1337),
            ('Обамов Барак Баракович', 15552),
            ('Джонов Джон Джонович', 73336)]
    cursor.executemany("INSERT INTO students(fio, num_zach) VALUES (?,?)", stud)
    conn.commit()

    #for row in cursor.execute('SELECT * FROM students'):
        #print(row)


    bot.polling()


    cursor.close()
    conn.close()
    #cursor.close()
    #conn.close()
    #conn = sqlite3.connect(location)
    #cursor = conn.cursor()
