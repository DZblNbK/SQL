import psycopg2
from config import settings
from psycopg2 import sql
from loger import logger


connection = psycopg2.connect(
    dbname=settings.DB_NAME,
    user=settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    port=settings.DB_PORT,
)

cursor = connection.cursor()


#Просмотр версии
def display_version():

    version_sql = sql.SQL("SELECT version();")

    with connection.cursor() as cursor:
        cursor.execute(
            version_sql
        )
        connection.commit()
        logger.info(f"BD Version: {cursor.fetchone()}")


#Создание таблицы
def create_table(table_name):

    create_table_sql = sql.SQL("""
        CREATE TABLE IF NOT EXISTS {} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INT,
            email VARCHAR(100),
            password VARCHAR(100)
        );
    """).format(sql.Identifier(table_name))
        
    with connection.cursor() as cursor:
        cursor.execute(
            create_table_sql
        )
    logger.info(f"Table {table_name} created")
        
        
#Ввод в таблицу
def insert_data(table_name, name, age, email, password):

    check_sql = sql.SQL("SELECT * FROM {} WHERE email = %s").format(sql.Identifier(table_name))

    insert_sql = sql.SQL("INSERT INTO {} (name, age, email, password) VALUES (%s, %s, %s, %s);").format(sql.Identifier(table_name))

    with connection.cursor() as cursor:
        cursor.execute(
            check_sql, (email,)
        )
        if not cursor.fetchall():
            cursor.execute(
                insert_sql, (name, age, email, password)
            )
            logger.info(f"INSERT INTO ({table_name}): {name}, {age}, {email}, {password}")
        else:
            logger.info(f"Пользователь с email: {email} уже существует!")
            pass

    connection.commit()
    

#Отображение таблицы
def display_table(table_name):

    display_sql = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))

    with connection.cursor() as cursor:
        cursor.execute(
            display_sql
        )
        rows = cursor.fetchall()
        logger.info(f"Data from table {table_name}: {rows}")
        for row in rows:
            print(row)

        
#Изменение таблицы
def update_table(table_name, age, name):

    update_sql = sql.SQL("""
        UPDATE {}
        SET возраст = %s
        WHERE имя = %s;
    """).format(sql.Identifier(table_name))

    with connection.cursor() as cursor:
        cursor.execute(
            update_sql, (age, name)
    )


#Очистка таблицы
def clear_table(table_name):

    clear_sql = sql.SQL("DELETE FROM {};").format(sql.Identifier(table_name))

    with connection.cursor() as cursor:
        cursor.execute(
            clear_sql
        )

# Изменение пароля
def update_password_in_table(table_name, name, old_password, new_password):
    
    change_pass_sql = sql.SQL("UPDATE {} SET password = %s WHERE name = %s AND PASSWORD = %s;").format(sql.Identifier(table_name))
    
    logger.info(f"Attempting to update password for user: {name} with old password: {old_password}")
     
    with connection.cursor() as cursor:
        cursor.execute(
            change_pass_sql, (new_password, name, old_password)
        )
        connection.commit()

        if not cursor.rowcount > 0:
            logger.info(f"Пароль пользователя {name} был изменен!")
        else:
            logger.info(f"Не получилось изменить пароль")


def delete_dublicates(table_name):

    delete_dublicates_sql = sql.SQL("DELETE FROM {} WHERE id NOT IN (SELECT MIN(id) FROM {} GROUP BY email);").format(sql.Identifier(table_name), sql.Identifier(table_name))

    with connection.cursor() as cursor:
        cursor.execute(
            delete_dublicates_sql
        )

    connection.commit

if __name__== "__main__":
    new_table_name = 'vpn_user2'
    display_version()

    
    
    create_table(new_table_name)
    #clear_table(new_table_name)
    delete_dublicates(new_table_name)
    insert_data(new_table_name, 'Иллидан', 22, 'pilvp@gmail.com', '63613')
    #update_password_in_table(new_table_name, 'Иллидан', '09244', '63613')
    display_table(new_table_name)