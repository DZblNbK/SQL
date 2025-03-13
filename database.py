import psycopg2
from psycopg2 import sql

# Класс для работы с базой данных
class Database:
    # Конструктор
    def __init__(self, settings, logger):
        self.logger = logger
        self.connected = False  # Флаг для отслеживания подключения
        self.connection = None  # Инициализация соединения
        self.connecting_to_database(settings)

    def connecting_to_database(self, settings):
        if not self.connected:
            try:
                self.connection = psycopg2.connect(
                    dbname=settings.DB_NAME,
                    user=settings.DB_USER,
                    password=settings.DB_PASS,
                    host=settings.DB_HOST,
                    port=settings.DB_PORT
                )
                self.logger.info(f"Connected to database ({settings.DB_NAME})")
                self.connected = True  # Устанавливаем флаг после успешного подключения
            except Exception as e:
                self.logger.error(f"Connecting to Database {settings.DB_NAME} failed: {e}")
                raise

    # вывод данных из таблицы
    def display_table(self, table_name: str) -> None:
        display_sql = sql.SQL("SELECT * FROM {};").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(display_sql)
                rows = cursor.fetchall()
                self.logger.info(f"Displaying data from table {table_name}: {rows}")
                for row in rows:
                    print(row)
        except Exception as e:
            self.logger.error(f"Error displaying table {table_name}: {e}")

    # очистка таблицы
    def clear_table(self, table_name: str) -> None:
        truncate_sql = sql.SQL("TRUNCATE TABLE {} CASCADE;").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(truncate_sql)
                self.connection.commit()
                self.logger.info(f"Table {table_name} was cleared")
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Error truncating table {table_name}: {e}")

    # удаление таблицы
    def delete_table(self, table_name: str) -> None:
        drop_sql = sql.SQL("DROP TABLE IF EXISTS {};").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(drop_sql)
                self.connection.commit()
                self.logger.info(f"Table {table_name} was dropped")
        except Exception as e:
            self.connection.rollback()
            self.logger.error(f"Error dropping table {table_name}: {e}")

    # закрытие соединения
    def close(self) -> None:
        if self.connected and self.connection is not None:
            self.connection.close()
            self.logger.info("Database closed")
            self.connected = False