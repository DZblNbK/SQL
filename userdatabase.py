from psycopg2 import sql
from logger_config import get_logger
from database import Database
import bcrypt

#Класс для работы с базой данных пользователей.
class UserDatabase(Database):

    # конструктор
    def __init__(self, settings, log_dir: str = "logs"):
        self.logger = get_logger(log_dir, "user_database.log", "INFO")
        super().__init__(settings, self.logger)

    #хэширование пароля
    def _hash_password(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #проверка пароля
    def _check_password(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except ValueError as e:
            self.logger.error(f"Invalid password hash: {e}")
            return False


    def create_user_table(self, table_name: str) -> None:
        create_user_table_sql = sql.SQL("""
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                email VARCHAR(100) UNIQUE,  -- Уникальность email
                password CHAR(60)           -- Фиксированная длина для хеша bcrypt
            );
        """).format(sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(create_user_table_sql)
                self.logger.info(f"Table {table_name} created or already exists")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error creating table {table_name}: {e}")
            raise


    def insert_data(self, table_name: str, name: str, age: int, email: str, password: str) -> None:
        hashed_password = self._hash_password(password)
        check_sql = sql.SQL("SELECT 1 FROM {} WHERE email = %s").format(sql.Identifier(table_name))
        insert_sql = sql.SQL("INSERT INTO {} (name, age, email, password) VALUES (%s, %s, %s, %s);").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(check_sql, (email,))
                if not cursor.fetchall():
                    cursor.execute(insert_sql, (name, age, email, hashed_password))
                    self.logger.info(f"Inserted new user into {table_name}: {name}, {age}, {email}, [hashed password]")
                else:
                    self.logger.info(f"User with email {email} already exists in {table_name}")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error inserting data into {table_name}: {e}")
            raise


    def update_table(self, table_name: str, email: str, name: str) -> None:
        """Обновление имени пользователя по email.

        Args:
            table_name: Название таблицы.
            email: Email пользователя.
            name: Новое имя пользователя.
        """
        update_sql = sql.SQL("""
            UPDATE {}
            SET name = %s
            WHERE email = %s;
        """).format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(update_sql, (name, email))
                if cursor.rowcount > 0:
                    self.logger.info(f"Updated name in {table_name} for email {email}: {name}")
                else:
                    self.logger.info(f"No user found with email {email} in {table_name}")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error updating table {table_name}: {e}")
            raise


    def delete_duplicates(self, table_name: str) -> None:
        """Удаление дубликатов пользователей по email.

        Args:
            table_name: Название таблицы.
        """
        delete_duplicates_sql = sql.SQL("""
            DELETE FROM {} 
            WHERE id NOT IN (SELECT MIN(id) FROM {} GROUP BY email);
        """).format(sql.Identifier(table_name), sql.Identifier(table_name))
        
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(delete_duplicates_sql)
                if cursor.rowcount > 0:
                    self.logger.info(f"Deleted {cursor.rowcount} duplicates in {table_name}")
                else:
                    self.logger.info(f"No duplicates found in {table_name}")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error deleting duplicates in {table_name}: {e}")
            raise


    def update_password_in_table(self, table_name: str, email: str, old_password: str, new_password: str) -> None:
        """Обновление пароля пользователя с проверкой старого пароля.

        Args:
            table_name: Название таблицы.
            email: Email пользователя.
            old_password: Текущий пароль для проверки.
            new_password: Новый пароль (будет хеширован).
        """
        get_password_sql = sql.SQL("SELECT password FROM {} WHERE email = %s;").format(sql.Identifier(table_name))
        update_pass_sql = sql.SQL("UPDATE {} SET password = %s WHERE email = %s;").format(sql.Identifier(table_name))

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(get_password_sql, (email,))
                result = cursor.fetchone()
                
                if not result:
                    self.logger.info(f"User with email {email} not found in {table_name}")
                    return

                stored_hash = result[0]
                if self._check_password(old_password, stored_hash):
                    new_hashed_password = self._hash_password(new_password)
                    cursor.execute(update_pass_sql, (new_hashed_password, email))
                    if cursor.rowcount > 0:
                        self.logger.info(f"Password updated for user with email {email} in {table_name}")
                    else:
                        self.logger.info(f"Failed to update password for {email} in {table_name}")
                else:
                    self.logger.info(f"Old password does not match for {email} in {table_name}")
            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error updating password in {table_name} for {email}: {e}")
            raise