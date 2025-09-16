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
            # Open PostgreSQL database connection
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

def transactional(func):
    """
    Decorator that manages database transactions automatically.
    Commits the transaction if the function succeeds, 
    rolls back if an exception occurs.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Begin transaction (SQLite uses autocommit=False by default)
            print("Starting transaction...")
            
            # Execute the decorated function
            result = func(conn, *args, **kwargs)
            
            # If no exception occurred, commit the transaction
            conn.commit()
            print("Transaction committed successfully")
            return result
            
        except Exception as e:
            # If an exception occurred, rollback the transaction
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception
    
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    # PostgreSQL uses %s for parameter placeholders, not ?
    cursor.execute("UPDATE user_data SET email = %s WHERE user_id = %s", (new_email, user_id))
    print(f"Updated user {user_id} email to {new_email}")
    cursor.close()

#### Update user's email with automatic transaction handling
update_user_email(user_id="330e8400-e29b-41d4-a716-446655440000", new_email='Crawford_Cartwright@hotmail.com')