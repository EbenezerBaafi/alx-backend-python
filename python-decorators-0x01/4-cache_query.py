import time
import psycopg2
import functools

query_cache = {}

def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            host="localhost",
            database="ALX_prodev",
            user="postgres",
            password="2Cedicray123@.",
        )
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # extract the SQL query string
        query = kwargs.get('query')
        if query is None and len(args) > 1:
            # in case query is passed as a positional arg after conn
            query = args[1]
        # if already cached, return directly
        if query in query_cache:
            print("Using cached result for:", query)
            return query_cache[query]
        # else run the function and cache the result
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# assuming with_db_connection is already defined
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM user_data")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM user_data")
