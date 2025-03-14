from config import settings
from datetime import datetime
from users import UserDatabase
from connections import ConnectionDatabase
from servers import ServerDatabase
import time


def user_db_fun(user_db):
    
    table_name = 'vpn_user2'
    name = 'Ilya'
    email = 'piv222@gmail.com'
    age = 22
    password = '63613'
    new_password = '09244'

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
                user_db.create_table(table_name)
                user_db_fun(user_db)
            case '2':
                user_db.insert_data(table_name, name, age, email, password)
                user_db_fun(user_db)
            case '3':
                user_db.update_password(table_name, email, password, new_password)
                user_db_fun(user_db)
            case '4':
                user_db.update_table(table_name, email, name)
                user_db_fun(user_db)
            case '5':
                user_db.delete_duplicates(table_name)
                user_db_fun(user_db)
            case '6':
                user_db.display_table(table_name)
                user_db_fun(user_db)
            case '7':
                user_db.clear_table(table_name)
                user_db_fun(user_db)
            case '8':
                user_db.delete_table(table_name)
                user_db_fun(user_db)
            case '0':
                user_db.close()
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


def server_db_fun(server_db):

    table_name = 'vpn_server'
    server_name = 'FirstServer'
    server_ip = '127.0.0.1:55555'
    status = 'Activate'
    location = 'Latvia'

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
                server_db.create_table(table_name)
                server_db_fun(server_db)
            case '2':
                server_db.insert_data(table_name, server_name, server_ip, status, location)
                server_db_fun(server_db)
            case '3':
                server_db.display_table(table_name)
                server_db_fun(server_db)
            case '4':
                server_db.clear_table(table_name)
                server_db_fun(server_db)
            case '5':
                server_db.delete_table(table_name)
                server_db_fun(server_db)
            case '0':
                server_db.close()
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


def connection_db_fun(connection_db):

    table_name = 'connections'
    user_table_name = 'vpn_user2'
    email = 'pilv2022@gmail.com'
    connection_time = datetime.now()
    time.sleep(2)
    disconnection_time = datetime.now()
    location = 'Moscow'
    connection_ip = '192.168.0.1:5433'

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
                connection_db.create_table(table_name, user_table_name)
                connection_db_fun(connection_db)
            case '2':
                connection_db.insert_data(user_table_name, table_name, email, connection_time, disconnection_time, connection_ip, location)
                connection_db_fun(connection_db)
            case '3':
                connection_db.display_table(table_name)
                connection_db_fun(connection_db)
            case '4':
                connection_db.clear_table(table_name)
                connection_db_fun(connection_db)
            case '5':
                connection_db.delete_table(table_name)
                connection_db_fun(connection_db)
            case '0':
                connection_db.close()
                return
            case _:
                print("Некорректный выбор, попробуйте снова.")


if __name__ == "__main__":
    log_dir = "logs"
    try:
        user_db = UserDatabase(settings, log_dir)
        user_db_fun(user_db)

        server_db = ServerDatabase(settings, log_dir)
        server_db.create_status_type()
        server_db_fun(server_db)

        connection_db = ConnectionDatabase(settings, log_dir)
        connection_db_fun(connection_db)
    except Exception as e:
        print(f"Произошла ошибка: {e}")