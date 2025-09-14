import psycopg2
import csv
import uuid
from psycopg2 import Error

def connect_db():
    """Connects to the PostgreSQL database server"""
    try:
        connection = psycopg2.connect(
            host='localhost',
            user='postgres',  # Replace with your PostgreSQL username
            password='2Cedicray123@.',  # Replace with your PostgreSQL password
            database='postgres'  # Connect to default postgres database first
        )
        connection.autocommit = True
        return connection
    except Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def create_database(connection):
    """Creates the database alx_prodev if it does not exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'ALX_prodev'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE ALX_prodev")
            print("Database ALX_prodev created successfully")
        else:
            print("Database ALX_prodev already exists")
        
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connects to the ALX_prodev database in PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='ALX_prodev',
            user='postgres',  # Replace with your PostgreSQL username
            password='2Cedicray123@.'  # Replace with your PostgreSQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields"""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id UUID PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            age DECIMAL NOT NULL
        )
        """
        cursor.execute(create_table_query)
        
        # Create index on user_id (optional since PRIMARY KEY already creates one)
        create_index_query = """
        CREATE INDEX IF NOT EXISTS idx_user_id ON user_data (user_id)
        """
        cursor.execute(create_index_query)
        
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data):
    """Inserts data in the database if it does not exist"""
    try:
        cursor = connection.cursor()
        
        for row in data:
            # Check if user already exists
            check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
            cursor.execute(check_query, (row['email'],))
            exists = cursor.fetchone()[0]
            
            if exists == 0:
                # Generate UUID for user_id
                user_id = str(uuid.uuid4())
                insert_query = """
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_id, row['name'], row['email'], int(row['age'])))
        
        connection.commit()
        cursor.close()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

def main():
    # Since database and table already exist, connect directly to alx_prodev
    prodev_connection = connect_to_prodev()
    if prodev_connection:
        print("Connected to ALX_prodev database successfully")
        
        # Read CSV data and insert
        try:
            # Get the directory where the script is located
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            csv_path = os.path.join(script_dir, "C://ALX/alx-backend-python/python-generators-0x00/user_data.csv")
            print(f"Looking for CSV at: {csv_path}")
            
            with open("C://ALX/alx-backend-python/python-generators-0x00/user_data.csv", 'r') as file:
                csv_reader = csv.DictReader(file)
                data = list(csv_reader)
                
                # Insert data
                insert_data(prodev_connection, data)
                
        except FileNotFoundError:
            print("user_data.csv file not found")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
        
        prodev_connection.close()
    else:
        print("Failed to connect to alx_prodev database")

if __name__ == "__main__":
    main()