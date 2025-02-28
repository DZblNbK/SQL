from psycopg2 import sql
from logger_setup import setup_logger
from database import Database



class UserDatabase(Database):

    def __init__(self, settings):
        super().__init__(settings)
        self.logger = setup_logger('logs', 'user_database.log')

    #создание таблицы
    def create_user_table(self, table_name):
        create_user_table_sql = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                email VARCHAR(100),
                password VARCHAR(100)
            );
        """).format(sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    create_user_table_sql
                )
                if cursor.rowcount > 0:
                    self.logger.info(f"Table {table_name} created")
                else:
                    self.logger.info(f"Table {table_name} already exists")
        except Exception as e:
            self.logger.error(f"Error creating table {table_name}: {e}")


    #Добавление данных
    def insert_data(self, table_name, name, age, email, password):

        check_sql = sql.SQL("SELECT * FROM {} WHERE email = %s").format(sql.Identifier(table_name))

        insert_sql = sql.SQL("INSERT INTO {} (name, age, email, password) VALUES (%s, %s, %s, %s);").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    check_sql, (email,)
                )
                if not cursor.fetchall():
                    cursor.execute(
                        insert_sql, (name, age, email, password)
                    )
                    self.logger.info(f"Insert new data in table {table_name}): {name}, {age}, {email}, {password}")
                else:
                    self.logger.info(f"User with email: {email} already exists")
                    pass

            self.connection.commit()
        except Exception as e:
            self.logger.error(f"")


    #Изменение данных в таблице по email
    def update_table(self, table_name, email, name):
        update_sql = sql.SQL("""
            UPDATE {}
            SET name = %s
            WHERE email = %s;
        """).format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    update_sql, (name, email)
                )
                self.logger.info(f"Dublicates in table {table_name} was deleted")
        except Exception as e:
            self.logger.error(f"Error of updating table {table_name}: {e}")
            

    def delete_dublicates(self, table_name):
        delete_dublicates_sql = sql.SQL("DELETE FROM {} WHERE id NOT IN (SELECT MIN(id) FROM {} GROUP BY email);").format(sql.Identifier(table_name), sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    delete_dublicates_sql
                )
                if cursor.rowcount > 0:
                    self.logger.info(f"Dublicates in table {table_name} was deleted")
                else:
                    self.logger.info(f"Dublicates in table {table_name} not found")
                    
            self.connection.commit
        except Exception as e:
            self.logger.error(f"Error or deleting dublicates in table {table_name}: {e}")


    def update_password_in_table(self, table_name, email, old_password, new_password):
        change_pass_sql = sql.SQL("UPDATE {} SET password = %s WHERE email = %s AND PASSWORD = %s;").format(sql.Identifier(table_name))
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    change_pass_sql, (new_password, email, old_password)
                )
                self.connection.commit()

                if cursor.rowcount > 0:
                    self.logger.info(f"Password of user with email {email} was updating")
                else:
                    self.logger.info(f"Failed to change password")
        except Exception as e:
            self.logger.error(f"Error with try to change password in table {table_name}: {e}") 