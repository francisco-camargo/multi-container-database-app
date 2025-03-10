import os
import time
import mariadb
from dotenv import load_dotenv
from src.logging_config import setup_logging

# Set up logger
logger = setup_logging()

def execute_sql_file(cursor, filepath):
    logger.info(f"Attempting to execute SQL file: {filepath}")
    try:
        with open(filepath, 'r') as file:
            sql_commands = file.read().split(';')
            for command in sql_commands:
                if command.strip():
                    logger.debug(f"Executing SQL command: {command}")
                    cursor.execute(command)
    except FileNotFoundError:
        logger.error(f"ERROR: SQL file not found at {filepath}")
        raise

def initialize_database():
    load_dotenv()

    # Regular user connection parameters
    config = {
        'host': os.getenv('MARIADB_HOST'),
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE'),
        'connect_timeout': 20
    }

    max_retries = 30  # Increase retries
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect as user (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Explicitly select database
            database = config['database']
            cursor.execute(f"USE {database}")

            sql_directory = 'sql'
            logger.info(f"Looking for SQL files in: {sql_directory}")

            # Execute schema
            schema_path = os.path.join(sql_directory, 'schema.sql')
            if os.path.exists(schema_path):
                logger.info("Creating tables...")
                execute_sql_file(cursor, schema_path)
            else:
                logger.error(f"ERROR: schema.sql not found at {schema_path}")
                return

            # Execute seed data
            seed_path = os.path.join(sql_directory, 'seed.sql')
            if os.path.exists(seed_path):
                logger.info("Inserting seed data...")
                execute_sql_file(cursor, seed_path)
            else:
                logger.warning(f"WARNING: seed.sql not found at {seed_path}")

            connection.commit()

            # Verify tables were created
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            logger.info(f"Created tables: {[table[0] for table in tables]}")

            logger.info("Database initialization completed successfully!")
            break

        except mariadb.Error as e:
            logger.error(f"Error connecting to MariaDB Platform: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not initialize database.")
                return

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

if __name__ == "__main__":
    initialize_database()
