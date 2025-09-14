import psycopg2
from psycopg2 import Error

def connect_to_alx_prodev():
    """Connects to the alx_prodev database in PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='ALX_prodev',
            user='postgres',  # Replace with your PostgreSQL username
            password='2Cedicray123@.'  # Replace with your PostgreSQL password
        )
        return connection
    except Error as e:
        print(f"Error connecting to alx_prodev database: {e}")
        return None

def stream_user_ages():
    """
    Generator function that yields user ages one by one.
    Memory-efficient streaming of ages from the database.
    
    Yields:
        float: User age
    """
    connection = connect_to_alx_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor(name='age_cursor')
        cursor.itersize = 1000  # Fetch in chunks for memory efficiency
        
        query = "SELECT age FROM user_data"
        cursor.execute(query)
        
        # Yield ages one by one using server-side cursor
        for row in cursor:  # Loop 1
            yield float(row[0])
            
    except Error as e:
        print(f"Error streaming ages: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def calculate_average_age():
    """
    Calculates the average age of users using the generator.
    Memory-efficient computation without loading entire dataset.
    """
    total_age = 0
    user_count = 0
    
    for age in stream_user_ages():  # Loop 2
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found in the database.")

# Example usage
def main():
    calculate_average_age()

if __name__ == "__main__":
    main()