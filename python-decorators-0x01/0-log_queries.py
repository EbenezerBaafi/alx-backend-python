import psycopg2
import functools

#### decorator to log SQL queries

def log_queries(func):
    """
    Decorator that logs SQL queries before executing them.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query from function arguments
        # Assuming 'query' is passed as a keyword argument or the first positional argument
        query = None
        
        # Check if 'query' is in kwargs
        if 'query' in kwargs:
            query = kwargs['query']
        # Check if there are positional arguments and assume first one might be query
        elif args:
            # Look for query in args - it might be any of the arguments
            for arg in args:
                if isinstance(arg, str) and any(keyword in arg.upper() for keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'CREATE', 'DROP', 'ALTER']):
                    query = arg
                    break
        
        # Log the query if found
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("SQL Query: [Query not found in arguments]")
        
        # Execute the original function
        return func(*args, **kwargs)
    
    return wrapper

@log_queries
def fetch_all_users(query):
    # PostgreSQL connection parameters
    conn = psycopg2.connect(
        host="localhost",
        database="ALX_prodev",
        user="postgres",
        password="2Cedicray123@.",
        port="5432"
    )
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM user_data")