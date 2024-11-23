import os
import csv
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "psql_backup")


def backup_postgresql_data():
    """
    Back up all PostgreSQL tables to CSV files.
    """
    if not all([DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
        print("Missing database configuration in .env file.")
        return

    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        # Ensure output directory exists
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Fetch all table names
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            """
        )
        tables = cursor.fetchall()

        # Export each table to CSV
        for table in tables:
            table_name = table[0]
            output_file = os.path.join(OUTPUT_DIR, f"{table_name}.csv")

            cursor.execute(sql.SQL("SELECT * FROM {}").format(sql.Identifier(table_name)))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            with open(output_file, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)

            print(f"Backed up table {table_name} to {output_file}")

        print("Database backup completed successfully.")
    except Exception as e:
        print(f"Error during backup: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
