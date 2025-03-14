from psycopg2 import sql
from logger import get_logger
from db import Database

# Класс для работы с базой данных серверов
class ServerDatabase(Database):
    # Конструктор
    def __init__(self, settings, log_dir: str = "logs"):
        self.logger = get_logger(log_dir, "server_database.log", "INFO")
        super().__init__(settings, self.logger)

    # создание ENUM типа
    def create_status_type(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    DO $$
                    BEGIN
                        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'server_status') THEN
                            CREATE TYPE server_status AS ENUM ('Activate', 'Inactivate');
                        END IF;
                    END $$;
                """)
                self.connection.commit()
                self.logger.info("ENUM type 'server_status' created or already exists.")
        except Exception as e:
            self.logger.error(f"Error creating ENUM type 'server_status': {e}")
            raise
    
    # создание таблицы
    def create_table(self, table_name):
        create_server_table_sql = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                server_name VARCHAR(100) NOT NULL,
                ip_address VARCHAR(100) NOT NULL,
                status server_status NOT NULL,
                location VARCHAR
            );
        """).format(sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_server_table_sql)
                self.logger.info(f"Table {table_name} created or already exists")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error creating table {table_name}: {e}")
            raise

    # добавление данных
    def insert_data(self, table_name: str, server_name: str, ip_address: str, status: str, location: str) -> None:
        check_sql = sql.SQL("SELECT 1 FROM {} WHERE server_name = %s").format(sql.Identifier(table_name))
        insert_sql = sql.SQL("INSERT INTO {} (server_name, ip_address, status, location) VALUES (%s, %s, %s, %s);").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    check_sql, (server_name,)
                )
                if not cursor.fetchall():
                    cursor.execute(
                        insert_sql, (server_name, ip_address, status, location)
                    )
                    self.logger.info(f"Insert new data in table {table_name}: {server_name}, {ip_address}, {status}, {location}")
                else:
                    self.logger.info(f"Server with name: {server_name} already exists")
                    return

            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error with data inserting: {e}")
            raise