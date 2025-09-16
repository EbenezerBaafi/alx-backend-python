import psycopg2
from psycopg2 import sql

class DatabaseConnection:
    """A context manager for handling PostgreSQL database connections automatically using psycopg2."""
    
    def __init__(self, host='localhost', database='database', user='postgres', password='password', port=5432):
        """
        Initialize the database connection context manager.
        
        Args:
            host (str): Database host
            database (str): Database name
            user (str): Database user
            password (str): Database password
            port (int): Database port
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        try:
            print(f"Opening database connection to: {self.host}:{self.port}/{self.database}")
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            return self.cursor
        except psycopg2.Error as e:
            print(f"Error opening database: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - close database connection.
        
        Args:
            exc_type: Exception type (if any)
            exc_value: Exception value (if any)
            traceback: Exception traceback (if any)
        """
        try:
            if self.cursor:
                self.cursor.close()
                print("Database cursor closed")
            
            if self.connection:
                if exc_type is None:
                    # No exception occurred, commit changes
                    self.connection.commit()
                    print("Transaction committed")
                else:
                    # Exception occurred, rollback changes
                    self.connection.rollback()
                    print("Transaction rolled back due to error")
                
                self.connection.close()
                print("Database connection closed")
        
        except psycopg2.Error as e:
            print(f"Error closing database: {e}")
        
        # Return False to propagate any exception that occurred
        return False


# Example usage demonstrating the context manager
if __name__ == "__main__":
    try:
        
        # Use the context manager to query users
        with DatabaseConnection(
            host='localhost',
            database='ALX_prodev',
            user='postgres',
            password='2Cedicray123@.'
        ) as cursor:
            
            # Execute the SELECT query
            cursor.execute("SELECT * FROM user_data")
            
            # Fetch and print results
            results = cursor.fetchall()
            
            print("\nQuery Results:")
            print("-" * 50)
            
            if results:
                # Get column names
                column_names = [desc[0] for desc in cursor.description]
                print(f"{'  |  '.join(column_names)}")
                print("-" * 50)
                
                # Print each row
                for row in results:
                    print(f"{'  |  '.join(str(value) for value in row)}")
            else:
                print("No users found in the database")
        
        print("\nContext manager automatically handled connection cleanup!")
        
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")