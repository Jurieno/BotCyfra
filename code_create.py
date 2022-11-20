import configparser
import pymysql
import random
import string

def generate_random_string():
    letters = string.ascii_lowercase
    symbol = string.ascii_uppercase
    mas = []
    for i in range(9):
        if i % 2 == 0:
            mas.append(random.choice(letters))
        else:
            mas.append(random.choice(symbol))
            if i % 3 == 0:
                mas.append('-')

    rand_string = ''.join(mas)

    return rand_string

config = configparser.ConfigParser()
config.read('config.ini')

con = pymysql.connect(host=config['database']['host'],
                        user=config['database']['user'],
                        password=config['database']['password'],
                        database=config['database']['db'],
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)

mas = []
n = int(input('Введите количество кодов: '))
id_company = int(input('Введите id компании: '))
input('Приостановка')

with con.cursor() as cur:
    for i in range(n):
        while True:
            gen = generate_random_string()
            cur.execute(f"SELECT * FROM `codes` WHERE `code`='{gen}'")
            rows = cur.fetchall()

            if not rows:
                cur.execute(f'INSERT INTO `codes`(`code`, `id_company`) VALUES ("{gen}",{id_company})')
                con.commit()
                break
            else:
                print(gen, ' - уже существует')

