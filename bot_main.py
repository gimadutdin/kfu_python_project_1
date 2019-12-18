import telebot, sqlite3, hashlib

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
    bot.send_message(message.chat.id, '/join - записаться(войти) на курс, /login_admin - вход для преподавателей, /getinfo - получить информацию для студента, /getrating - посмотреть свой рейтинг')



@bot.message_handler(commands=['join'])
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
    sel_res = cur.execute('SELECT id FROM students WHERE name=? and surname=? and patronymic=? and num_zach=?', (name, surname, patronymic, num_zach))
    first_row = cur.fetchone()
    if first_row != None:#если студент найден то мы должны привязать его телеграм айди
        tid_was = cur.execute('SELECT id FROM joined WHERE telegram_id=?', (message.from_user.id,))
        tid_was_row = cur.fetchone()
        if tid_was_row != None:#если к этому телеграм айди уже был кто то привязан то перепривязать
            cur.execute('UPDATE joined SET id=? WHERE telegram_id=?', (first_row[0], message.from_user.id))
            con.commit()
        else:#если к этому телеграм айди еще никто не был привязан
            cur.execute('INSERT INTO joined(id, telegram_id) VALUES (?, ?)', (first_row[0], message.from_user.id))
            con.commit()
        bot.send_message(message.from_user.id, 'Вы записались вошли и записаны на курс');
    else:
        bot.send_message(message.from_user.id, 'Студента с такими данными не существует!');
    cur.close()
    con.close()
    

#Вход для администраторов
def admin_login_exists(adm_login):
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()
    sel_res = cur.execute('SELECT * FROM admin WHERE login=?', (adm_login,))
    first_row = cur.fetchone()
    return (first_row != None)

def check_admin_password(adm_psw):
    adm_psw_hash = hashlib.md5(adm_psw.encode("ascii")).hexdigest() 
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()
    sel_res = cur.execute('SELECT * FROM admin WHERE password=?', (adm_psw_hash,))
    first_row = cur.fetchone()
    return (first_row != None)
    
@bot.message_handler(commands=['login_admin'])
def login_stud_message(message):
    bot.send_message(message.from_user.id, "Введите логин: ");
    bot.register_next_step_handler(message, get_admin_login);

def get_admin_login(message):
    adm_login = message.text;
    #проверяем верный ли логин
    if admin_login_exists(adm_login):
        bot.send_message(message.from_user.id, 'Введите пароль:');
        bot.register_next_step_handler(message, get_admin_password);
    else:
        bot.send_message(message.from_user.id, 'Неверный логин');

def get_admin_password(message):
    adm_psw = message.text;
    #проверяем верный ли пароль
    if check_admin_password(adm_psw):
        # привязываем телеграм айди собеседника к админской учетке
        con = sqlite3.connect("bot_database.db")
        cur = con.cursor()
        cur.execute('UPDATE admin SET telegram_id=?', (message.from_user.id,))
        con.commit()
        cur.close()
        con.close()
        bot.send_message(message.from_user.id, 'Вы вошли в учетную запись администратора');
    else:
        bot.send_message(message.from_user.id, 'Неверный пароль!');


#отладочная функция..
@bot.message_handler(content_types=['text'])
def send_text(message):
    #print(message.from_user.id)
    con = sqlite3.connect("bot_database.db")
    cur = con.cursor()
    for row in cur.execute('SELECT * FROM students'):# where telegram_id=?', (str(message.from_user.id),)):
        print(row)
    print("\n")

    for row in cur.execute('SELECT * FROM joined'):# where telegram_id=?', (str(message.from_user.id),)):
        print(row)
    print("\n")

    for row in cur.execute('SELECT * FROM admin'):# where telegram_id=?', (str(message.from_user.id),)):
        print(row)
    print("\n")
    
    cur.close()
    con.close()




if __name__ == "__main__":


    
    bot.polling()

