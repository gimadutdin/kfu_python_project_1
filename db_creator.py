import sqlite3, hashlib

conn = sqlite3.connect("bot_database.db")
cursor = conn.cursor()
# Создание таблицы студентов
cursor.execute("""CREATE TABLE students
                  (id integer primary key,
                   name text,
                   surname text,
                   patronymic text,
                   num_zach text)
               """)
conn.commit()
# Заполнение таблицы студентов
stud = [('Иван', 'Иванов', 'Иванович', '1337'),
        ('Барак', 'Обама', 'Джонович', '15552'),
        ('Тимур', 'Тимуров', 'Тимурович', '73336'),
        ('Петр', 'Петров', 'Петрович', '999899'),
        ('Эмиль', 'Эмилев', 'Эмилевич', '897878')]
cursor.executemany("INSERT INTO students(name, surname, patronymic, num_zach) VALUES (?,?,?,?)", stud)
conn.commit()

# Создание таблицы записавшихся на курс
cursor.execute("""CREATE TABLE joined
                  (id integer primary key,
                   telegram_id text,
                   FOREIGN KEY(id) REFERENCES students(id))
               """)
conn.commit()

# Создание таблицы учета
cursor.execute("""CREATE TABLE uchet
                  (id integer primary key,
                   points integer,
                   misses integer,
                   debts integer,
                   FOREIGN KEY(id) REFERENCES students(id))
               """)
conn.commit()

# Создание таблицы в которой будет логин и пароль админа
cursor.execute("""CREATE TABLE admin
                  (login text,
                   password text,
                   telegram_id text)
               """)
conn.commit()

cursor.execute("INSERT INTO admin(login, password, telegram_id) VALUES (?,?,?)", ('administrator', hashlib.md5(b"qwerty123").hexdigest(), 'undefined'))
conn.commit()

#CREATE TABLE if not exists students


# вывести содержимое таблиц
for row in cursor.execute('SELECT * FROM students'):
    print(row)
print()
for row in cursor.execute('SELECT * FROM admin'):
    print(row)

cursor.close()
conn.close()
