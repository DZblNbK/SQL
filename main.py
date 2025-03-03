from config import settings
from logger_setup import setup_logger
from datetime import datetime
from userdatabase import UserDatabase
from conectdatabase import ConnectionDatabase
from serverdatabase import ServerDatabase
import time


def dbuser_fun(dbuser):
    
    table_name = 'vpn_user2'
    name = 'Ilya'
    email = 'piv2002@gmail.com'
    age = 22
    passwd = '63613'
    new_passwd = '09244'

    print(f'Таблица {table_name}')
    print("1 - Создать таблицу")
    print("2 - Добавить данные в таблицу")
    print("3 - Поменять пароль")
    print("4 - Изменить имя по email")
    print("5 - Удалить дубликаты")
    print("6 - Вывести данные из таблицы")
    print("7 - Очистить таблицу")
    print("8 - Удалить таблицу")
    print("0 - Выйти")

    choice = input("Введите номер действия: ")

    match choice:
            case '1':
                dbuser.create_user_table(table_name)
                dbuser_fun(dbuser)
            case '2':
                dbuser.insert_data(table_name, name, age, email, passwd)
                dbuser_fun(dbuser)
            case '3':
                dbuser.update_password_in_table(table_name, email, passwd, new_passwd)
                dbuser_fun(dbuser)
            case '4':
                dbuser.update_table(table_name, email, name)
                dbuser_fun(dbuser)
            case '5':
                dbuser.delete_duplicates(table_name)
                dbuser_fun(dbuser)
            case '6':
                dbuser.display_table(table_name)
                dbuser_fun(dbuser)
            case '7':
                dbuser.clear_table(table_name)
                dbuser_fun(dbuser)
            case '8':
                dbuser.delete_table(table_name)
                dbuser_fun(dbuser)
            case '0':
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


def dbserv_fun(dbserv):

    table_name = 'vpn_server'
    server_name1 = 'FirstServer'
    ip_address1_server = '127.0.0.1:55555'
    status1 = 'Activate'
    location1 = 'Latvia'

    print(f'Таблица {table_name}')
    print("1 - Создать таблицу")
    print("2 - Добавить данные в таблицу")
    print("3 - Вывести данные из таблицы")
    print("4 - Очистить таблицу")
    print("5 - Удалить таблицу")
    print("0 - Выйти")

    choice = input("Введите номер действия: ")

    match choice:
            case '1':
                dbserv.create_server_table(table_name)
                dbserv_fun(dbserv)
            case '2':
                dbserv.insert_data(table_name, server_name1, ip_address1_server, status1, location1)
                dbserv_fun(dbserv)
            case '3':
                dbserv.display_table(table_name)
                dbserv_fun(dbserv)
            case '4':
                dbserv.clear_table(table_name)
                dbserv_fun(dbserv)
            case '5':
                dbserv.delete_table(table_name)
                dbserv_fun(dbserv)
            case '0':
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


def dbcon_fun(dbcon):

    table_name = 'connections'
    user_table_name1 = 'vpn_user2'
    email1 = 'pilv2022@gmail.com'
    connection_time = datetime.now()
    time.sleep(2)
    disconnection_time = datetime.now()
    location = 'Moscow'
    ip = '192.168.0.1:5433'

    print(f'Таблица {table_name}')
    print("1 - Создать таблицу")
    print("2 - Добавить данные в таблицу")
    print("3 - Вывести данные из таблицы")
    print("4 - Очистить таблицу")
    print("5 - Удалить таблицу")
    print("0 - Выйти")

    choice = input("Введите номер действия: ")

    match choice:
            case '1':
                dbcon.create_connection_table(table_name)
                dbcon_fun(dbcon)
            case '2':
                dbcon.insert_data(user_table_name1, table_name, email1, connection_time, disconnection_time, ip, location)
                dbcon_fun(dbcon)
            case '3':
                dbcon.display_table(table_name)
                dbcon_fun(dbcon)
            case '4':
                dbcon.clear_table(table_name)
                dbcon_fun(dbcon)
            case '5':
                dbcon.delete_table(table_name)
                dbcon_fun(dbcon)
            case '0':
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":

    dbuser = UserDatabase(settings)
    dbuser_fun(dbuser)
    dbserv = ServerDatabase(settings)
    dbserv.create_server_status_type()
    dbserv_fun(dbserv)
    dbcon = ConnectionDatabase(settings)
    dbcon_fun(dbcon)