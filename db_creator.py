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
stud = [('Иван', 'Иванов', 'Иванович', '160001'),
        ('Барак', 'Обама', 'Джонович', '160002'),
        ('Тимур', 'Тимуров', 'Тимурович', '160003'),
        ('Петр', 'Петров', 'Петрович', '160004'),
        ('Эмиль', 'Эмилев', 'Эмилевич', '160005'),
        ('Николай', 'Сергеев', 'Айнурович', '160006'),
        ('Мария', 'Петрова', 'Ивановна', '160007'),
        ('Анна', 'Чудная', 'Андреевна', '160008'),
        ('Алла','Орехова', 'Еремеевна', '160009'),
        ('Евдокия', 'Ефремова', 'Васильевна', '160010'),
        ('Якуб', 'Шурупов', 'Юриевич', '160011'),
        ('Алла', 'Васильева', 'Максимовна', '160012'),
        ('Борис', 'Ухов', 'Изяславович', '160013'),
        ('Платон', 'Янко', 'Феликсович', '160014'),
        ('Алина', 'Жданова', 'Степановна', '160015'),
        ('Юлия', 'Петрова', 'Александрова', '160016'),
        ('Харитон', 'Невский', 'Модестович', '160017'),
        ('Марианна', 'Сафонова', 'Тимуровна', '160018'),
        ('Тимур', 'Савин', 'Егорович', '160019'),
        ('Андрей', 'Дроков', 'Изяславович', '160020'),]

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

uch = [(1, 99, 0, 1),
       (3, 78, 1, 3),
       (2, 59, 4, 2), (4, 71, 2, 1), (5, 100, 0, 0),
       (6, 56, 3, 6), (7, 45, 9, 5), (8, 86, 1, 2),
       (9, 65, 3, 3), (10, 87, 2, 1), (11, 100, 0, 0),
       (12, 27, 10, 10), (13, 61, 5, 4), (14, 91, 1, 1),
       (15, 73, 2, 3), (16, 97, 1, 0), (17, 39, 5, 8),
       (18, 78, 4, 2), (19, 100, 0, 0), (20, 89, 2, 2)]

cursor.executemany("INSERT INTO uchet(id, points, misses, debts) VALUES (?,?,?,?)", uch)
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
