import telebot, sqlite3

name = '';
surname = '';
patronymic = '';
num_zach = ''

bot = telebot.TeleBot('1061478384:AAG4tawKAjUiTZ_59uEhUptfdSkd7nlxtDM')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Вас приветствует бот! /help - помощь по командам')

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '/login_stud - вход для студентов, /login_admin - вход для преподавателей, /join_course')



@bot.message_handler(commands=['login_stud'])
def login_stud_message(message):
    bot.send_message(message.from_user.id, "Введите имя: ");
    bot.register_next_step_handler(message, get_name);

def get_name(message):
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Введите фамилию:');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Введите отчество:');
    bot.register_next_step_handler(message, get_patronymic);

def get_patronymic(message):
    global patronymic;
    patronymic = message.text;
    bot.send_message(message.from_user.id, 'Введите номер зачетки:');
    bot.register_next_step_handler(message, get_num_zach);

def get_num_zach(message):
    global num_zach;
    num_zach = message.text;

    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM students WHERE telegram_id=?", (str(message.from_user.id),))
    cur.execute("INSERT INTO students(telegram_id, name, surname, patronymic, num_zach) VALUES (?,?,?,?,?)", (str(message.from_user.id), name, surname, patronymic, num_zach))
    con.commit()
    cur.close()
    con.close()
    
"""
@bot.message_handler(content_types=['login_admin'])
def login_admin_message(message):
    
    arr = message.text.split(' ')
    login = arr[1] + ' ' + arr[2] + ' ' + arr[3]
    password = arr[4]

    cursor = conn.cursor()
    sel_res = cursor.execute('select * from admins where login=? and password=?', (login, int(password)))
"""
    
    
@bot.message_handler(content_types=['text'])
def send_text(message):
    #print(message.from_user.id)
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM students'):# where telegram_id=?', (str(message.from_user.id),)):
        print(row)
    print("\n")
    cur.close()
    con.close()



################################################################
if __name__ == "__main__":
    conn = sqlite3.connect("bot_database.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    # Создание таблицы
    cursor.execute("""CREATE TABLE if not exists students
                      (id integer primary key,
                       telegram_id text,
                       name text,
                       surname text,
                       patronymic text,
                       num_zach text)
                   """)

    conn.commit()

    #stud = [('Альбертов Альберт Альбертович', 1337),
     #       ('Обамов Барак Баракович', 15552),
      #      ('Джонов Джон Джонович', 73336)]
    #cursor.executemany("INSERT INTO students(fio, num_zach) VALUES (?,?)", stud)
    #conn.commit()

    #for row in cursor.execute('SELECT * FROM students'):
        #print(row)


    bot.polling()


    cursor.close()
    conn.close()
    #cursor.close()
    #conn.close()
    #conn = sqlite3.connect(location)
    #cursor = conn.cursor()
