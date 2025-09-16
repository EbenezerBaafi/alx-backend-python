import psycopg2
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing database connections.
    Opens a connection, passes it as the first argument to the function, 
    and ensures it's closed afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Database connection parameters
        conn = None
        try:
            # Open database connection
            conn = psycopg2.connect(
                host="localhost",
                database="ALX_prodev",
                user="postgres", 
                password="2Cedicray123@.",
                port="5432"
            )
            
            # Call the original function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
            
        except Exception as e:
            print(f"Database error: {e}")
            raise
        finally:
            # Always close the connection
            if conn:
                conn.close()
                print("Database connection closed")
    
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    # PostgreSQL uses %s for parameter placeholders, not ?
    cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

#### Fetch user by ID with automatic connection handling

# Example usage with proper UUID
user = get_user_by_id(user_id="550e8400-e29b-41d4-a716-446655440000")
print("User by UUID:", user)
