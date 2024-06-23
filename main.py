import sqlite3

conn = sqlite3.connect('school.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
''')

cursor.executemany('''
INSERT INTO countries (title) VALUES (?)
''', [('Кыргызстан',), ('Германия',), ('Китай',)])

cursor.execute('''
CREATE TABLE IF NOT EXISTS cities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    area REAL DEFAULT 0,
    country_id INTEGER,
    FOREIGN KEY (country_id) REFERENCES countries (id)
)
''')

cursor.executemany('''
INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)
''', [
    ('Бишкек', 127.0, 1),
    ('Ош', 182.0, 1),
    ('Берлин', 891.8, 2),
    ('Мюнхен', 310.7, 2),
    ('Пекин', 16410.54, 3),
    ('Шанхай', 6340.5, 3),
    ('Гуанчжоу', 7434.4, 3)
])

cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    city_id INTEGER,
    FOREIGN KEY (city_id) REFERENCES cities (id)
)
''')

cursor.executemany('''
INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)
''', [
    ('Алик', 'Карабаев', 1),
    ('Айгуль', 'Суранова', 1),
    ('Марат', 'Токтосунов', 2),
    ('Эльвира', 'Абдраимова', 2),
    ('Ганс', 'Мюллер', 3),
    ('Клаус', 'Шмитт', 3),
    ('Лиза', 'Беккер', 4),
    ('Софи', 'Крафт', 4),
    ('Вэй', 'Ли', 5),
    ('Мин', 'Хуан', 5),
    ('Джин', 'Чен', 6),
    ('Сяо', 'Лю', 6),
    ('Хун', 'Вонг', 7),
    ('Ченг', 'Фен', 7),
    ('Лин', 'Фу', 7)
])

conn.commit()
conn.close()


def display_students_by_city(city_id):
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT students.first_name, students.last_name, countries.title, cities.title, cities.area
    FROM students
    JOIN cities ON students.city_id = cities.id
    JOIN countries ON cities.country_id = countries.id
    WHERE students.city_id = ?
    ''', (city_id,))

    students = cursor.fetchall()

    if students:
        for student in students:
            print(
                f"Имя: {student[0]}, Фамилия: {student[1]}, Страна: {student[2]}, Город: {student[3]}, Площадь города: {student[4]} км²")
    else:
        print("Нет учеников в данном городе.")

    conn.close()


def main():
    conn = sqlite3.connect('school.db')
    cursor = conn.cursor()

    print(
        "Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")

    cursor.execute('SELECT id, title FROM cities')
    cities = cursor.fetchall()

    for city in cities:
        print(f"{city[0]}. {city[1]}")

    while True:
        try:
            city_id = int(input("Введите id города: "))
            if city_id == 0:
                break
            display_students_by_city(city_id)
        except ValueError:
            print("Пожалуйста, введите корректный номер города.")

    conn.close()


if __name__ == "__main__":
    main()
