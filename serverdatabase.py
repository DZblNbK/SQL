from psycopg2 import sql
from logger_setup import setup_logger
from database import Database
from config import settings



class ServerDatabase(Database):

    def __init__(self, settings):
        super().__init__(settings)
        self.logger = setup_logger('logs', 'server_database.log')
    
    def create_server_status_type(self):
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
    
    
    def create_server_table(self, table_name):
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
                cursor.execute(
                    create_server_table_sql
                )
                if cursor.rowcount > 0:
                    self.logger.info(f"Table {table_name} created")
                else:
                    self.logger.info(f"Table {table_name} already exists")
        except Exception as e:
            self.logger.error(f"Error creating table {table_name}: {e}")


    def insert_data(self, table_name, server_name, ip_address, status, location):

        check_sql = sql.SQL("SELECT * FROM {} WHERE server_name = %s").format(sql.Identifier(table_name))

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
                    pass

            self.connection.commit()
        except Exception as e:
            self.logger.error(f"Error with data inserting: {e}")