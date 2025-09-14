import psycopg2
from psycopg2 import Error

def connect_to_alx_prodev():
    """Connects to the alx_prodev database in PostgreSQL"""
    try:
        connection = psycopg2.connect(
            host='localhost',
            database='ALX_prodev',
            user='postgres',  
            password='2Cedicray123@.'  
        )
        return connection
    except Error as e:
        print(f"Error connecting to alx_prodev database: {e}")
        return None

def stream_users():
    """
    Generator function that streams rows from the user_data table one by one.
    Uses server-side cursor for memory efficiency with large datasets.
    
    Args:
        min_age (int, optional): Minimum age filter
        max_age (int, optional): Maximum age filter
        
    Yields:
        dict: User data with keys: user_id, name, email, age
    """
    connection = connect_to_alx_prodev()
    if not connection:
        return
    
    try:
        # Create named cursor for server-side processing (memory efficient)
        cursor = connection.cursor(name='user_cursor')
        cursor.itersize = 1000  # Fetch 1000 rows at a time from server
        
        # Build dynamic query based on filters
        query = "SELECT user_id, name, email, age FROM user_data"
        conditions = []
        params = []
        
        # if min_age is not None:
        #     conditions.append("age >= %s")
        #     params.append(min_age)
        
        # if max_age is not None:
        #     conditions.append("age <= %s")
        #     params.append(max_age)
        
        # if conditions:
        #     query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY name"
        
        cursor.execute(query, params)
        
        # Yield rows one by one using server-side cursor
        for row in cursor:
            user_data = {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }
            yield user_data
            
    except Error as e:
        print(f"Error streaming data: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Example usage
def main():
    print("Streaming all users:")
    for user in stream_users():
        print(f"{user['name']} ({user['email']}) - Age: {user['age']}")
    
    print("\nStreaming users aged 25-40:")
    for user in stream_users():
        print(f"{user['name']} - Age: {user['age']}")

if __name__ == "__main__":
    main()