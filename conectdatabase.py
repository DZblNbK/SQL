from psycopg2 import sql
from logger_config import get_logger
from database import Database


# Класс для работы с базой данных подключений
class ConnectionDatabase(Database):

    def __init__(self, settings, log_dir: str = "logs"):
        self.logger = get_logger(log_dir, "connection_database.log", "INFO")
        super().__init__(settings, self.logger)

    
    def create_connection_table(self, table_name):
        create_connection_table_sql = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES vpn_user2(id) ON DELETE CASCADE,
                connection_time TIMESTAMP NOT NULL,
                disconnection_time TIMESTAMP,
                ip_address VARCHAR NOT NULL,
                location VARCHAR
            );
        """).format(sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    create_connection_table_sql
                )
                self.logger.info(f"Table {table_name} created or already exists")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error creating table {table_name}: {e}")
            raise

    
    def insert_data(self, user_table_name: str, table_name: str, email: str, connection_time, disconnection_time, ip_address: str, location: str) -> None:
        # Проверка существования пользователя
        find_user_id_sql = sql.SQL("SELECT id FROM {} WHERE email = %s;").format(sql.Identifier(user_table_name))
        insert_sql = sql.SQL("INSERT INTO {} (user_id, connection_time, disconnection_time, ip_address, location) VALUES (%s, %s, %s, %s, %s);").format(sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    find_user_id_sql, (email,)
                )
                user_id = cursor.fetchone()
                if user_id is None:
                    self.logger.info(f"User with email {email} does not exist in table {user_table_name}.")
                    return
                user_id = user_id[0]
                self.logger.info(f"Id by email {email} is {user_id}")

                cursor.execute(
                    insert_sql, (user_id, connection_time, disconnection_time, ip_address, location)
                )
                self.logger.info(f"Inserted new data in table {table_name}: {user_id}, {connection_time}, {disconnection_time}, {ip_address}, {location}")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error inserting info about connection: {e}. SQL: {insert_sql}, Params: {(user_id, connection_time, disconnection_time, ip_address, location)}")
            raise