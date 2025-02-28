import psycopg2
from psycopg2 import sql
from config import settings
from logger_setup import setup_logger




class Database:
    #Конструктор
    def __init__(self, settings):
        try:
            self.connection = psycopg2.connect(
                dbname = settings.DB_NAME,
                user = settings.DB_USER,
                password = settings.DB_PASS,
                host = settings.DB_HOST,
                port = settings.DB_PORT
            )

        except Exception as e:
            self.logger.error(f"Connecting to Database {settings.DB_NAME} is failed: {e}")


    #вывод данных из таблицы
    def display_table(self, table_name):
        display_sql = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    display_sql
                )
                rows = cursor.fetchall()
                self.logger.info(f"Data from table {table_name}: {rows}")
                for row in rows:
                    print(row)
        except Exception as e:
            self.logger.error(f"Error display table {table_name}: {e}")


    #очистка таблицы
    def clear_table(self, table_name):
        truncate_sql = sql.SQL("TRUNCATE TABLE {};").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(truncate_sql)
                self.connection.commit()
                self.logger.info(f"Table {table_name} was cleared")
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Error truncating table {table_name}: {e}")

    
    #удаление таблицы
    def delete_table(self, table_name):
        drop_sql = sql.SQL("DROP TABLE {};").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(drop_sql)
                self.connection.commit()
                self.logger.info(f"Table {table_name} was dropped")
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Error dropping table {table_name}: {e}")


    def close(self):
        self.connection.close()
        self.logger.info("Database closed")
