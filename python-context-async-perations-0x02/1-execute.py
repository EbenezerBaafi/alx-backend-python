import psycopg2
from psycopg2 import sql

class ExecuteQuery:
    """A reusable context manager for executing database queries with automatic connection management."""
    
    def __init__(self, query, params=None, host='localhost', database='mydb', user='postgres', password='password', port=5432):
        """
        Initialize the query execution context manager.
        
        Args:
            query (str): SQL query to execute
            params (tuple/list): Parameters for the query (optional)
            host (str): Database host
            database (str): Database name
            user (str): Database user_data
            password (str): Database password
            port (int): Database port
        """
        self.query = query
        self.params = params or ()
        self.host = host
        self.database = 'ALX_prodev'
        self.user = 'postgres'
        self.password = '2Cedicray123@.'
        self.port = port
        self.connection = None
        self.cursor = None
        self.results = None
    
    def __enter__(self):
        """
        Enter the context manager - establish connection and execute query.
        
        Returns:
            list: Query results
        """
        try:
            print(f"Opening database connection to: {self.host}:{self.port}/{self.database}")
            
            # Establish connection
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            
            print(f"Executing query: {self.query}")
            if self.params:
                print(f"With parameters: {self.params}")
            
            # Execute the query with parameters
            self.cursor.execute(self.query, self.params)
            
            # Check if it's a SELECT query (returns results)
            if self.query.strip().upper().startswith('SELECT'):
                self.results = self.cursor.fetchall()
                print(f"Query executed successfully. Retrieved {len(self.results)} rows.")
            else:
                # For INSERT, UPDATE, DELETE queries
                affected_rows = self.cursor.rowcount
                print(f"Query executed successfully. {affected_rows} rows affected.")
                self.results = affected_rows
            
            return self.results
            
        except psycopg2.Error as e:
            print(f"Database error occurred: {e}")
            if self.connection:
                self.connection.rollback()
            raise
        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager - handle cleanup and transaction management.
        
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
            print(f"Error during cleanup: {e}")
        
        # Return False to propagate any exception that occurred
        return False


# Example usage demonstrating the context manager
if __name__ == "__main__":
    
    try:        
        # Example 1: Execute the specified query with parameter
        print("=" * 60)
        print("EXAMPLE 1: Query user_data WHERE age > 25")
        print("=" * 60)
        
        query = "SELECT * FROM user_data WHERE age > %s"
        parameter = 25
        
        with ExecuteQuery(query, (parameter,)) as results:
            print(f"\nResults for users with age > {parameter}:")
            print("-" * 50)
            
            if results:
                # Print header (assuming we know the column structure)
                print(f"{'ID':<5} | {'Name':<15} | {'Email':<25} | {'Age':<5} | {'Created At'}")
                print("-" * 70)
                
                # Print each row
                for row in results:
                    print(f"{row[0]:<5} | {row[1]:<15} | {row[2]:<25} | {row[3]:<5} ")
            else:
                print(f"No users found with age > {parameter}")
        
        # Example 2: Another query with different parameters
        print("\n" + "=" * 60)
        print("EXAMPLE 2: Query users WHERE age BETWEEN 20 AND 30")
        print("=" * 60)
        
        query2 = "SELECT name, email, age FROM user_data WHERE age BETWEEN %s AND %s ORDER BY age"
        
        with ExecuteQuery(query2, (20, 30)) as results:
            print(f"\nResults for user_data with age between 20 and 30:")
            print("-" * 50)
            
            if results:
                print(f"{'Name':<15} | {'Email':<25} | {'Age':<5}")
                print("-" * 50)
                
                for row in results:
                    print(f"{row[0]:<15} | {row[1]:<25} | {row[2]:<5}")
            else:
                print("No users found in the specified age range")
        
        print("\n" + "=" * 60)
        print("Context manager successfully handled all operations!")
        print("=" * 60)
        
    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")