import os
import time
import mariadb
from dotenv import load_dotenv
from tabulate import tabulate
from src.logging_config import setup_logging

# Set up logger
logger = setup_logging()

host = os.getenv('MARIADB_HOST')

def show_table_data(
    table_name,
    host=host,
    ):
    logger.info('Running show_data.py')
    load_dotenv()

    config = {
        'host': host,  # Use container service name
        'port': int(os.getenv('MARIADB_PORT')),
        'user': os.getenv('MARIADB_USER'),
        'password': os.getenv('MARIADB_PASSWORD'),
        'database': os.getenv('MARIADB_DATABASE'),
        'connect_timeout': 20
    }

    max_retries = 5
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{max_retries})...")
            connection = mariadb.connect(**config)
            cursor = connection.cursor()

            # Get column names
            logger.debug(f"Fetching column names for table: {table_name}")
            cursor.execute(f"SHOW COLUMNS FROM {table_name}")
            columns = [column[0] for column in cursor.fetchall()]

            # Get table data
            logger.debug(f"Fetching data from table: {table_name}")
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            if rows:
                logger.info(f"Found {len(rows)} records in {table_name}")
                logger.info(f"\nContents of {table_name}:")
                logger.info("\n" + tabulate(rows, headers=columns, tablefmt='grid'))
            else:
                logger.warning(f"No data found in {table_name}")

            break

        except mariadb.Error as e:
            logger.error(f"Database error: {e}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not connect to database.")
                return

        finally:
            if 'cursor' in locals():
                cursor.close()
                logger.debug("Cursor closed")
            if 'connection' in locals():
                connection.close()
                logger.debug("Connection closed")

if __name__ == "__main__":
    tables = ['users', 'posts', 'comments']
    for table in tables:
        show_table_data(table, host='localhost')
