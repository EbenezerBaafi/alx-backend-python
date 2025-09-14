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

def paginate_users(page_size, offset):
    """
    Fetches a specific page of users from the database.
    Args:
        page_size (int): Number of users per page
        offset (int): Number of records to skip (for pagination)     
    Returns:
        list: List of user dictionaries for the requested page
    """
    connection = connect_to_alx_prodev()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        query = """
        SELECT * 
        FROM user_data 
        ORDER BY name 
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (page_size, offset))
        rows = cursor.fetchall()
        
        # Convert rows to list of dictionaries
        users = []
        for row in rows:
            user_data = {
                'user_id': row[0],
                'name': row[1],
                'email': row[2],
                'age': row[3]
            }
            users.append(user_data)
        
        return users
        
    except Error as e:
        print(f"Error fetching paginated data: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def lazy_paginate(page_size):
    """
    Generator function that lazily loads paginated user data.
    Fetches the next page only when needed, starting from offset 0.    
    Args:
        page_size (int): Number of users per page      
    Yields:
        list: Page of user records as dictionaries
    """
    offset = 0
    
    while True:  # Single loop as required
        # Fetch the current page
        page_data = paginate_users(page_size, offset)
        
        # If no data returned, we've reached the end
        if not page_data:
            break
        
        # Yield the current page
        yield page_data
        
        # Move to next page
        offset += page_size

# Example 
def main():
    print("Lazy pagination demo with page size 3:")
    print("=" * 50)
    
    page_number = 1
    for page in lazy_paginate(3):
        print(f"\nPage {page_number}:")
        print("-" * 20)
        for user in page:
            print(f"  {user['name']} ({user['email']}) - Age: {user['age']}")
        
        page_number += 1
        
        # Optional: Stop after a certain number of pages for demo
        if page_number > 5:  # Limit demo to 5 pages
            print(f"\n... (stopping demo after {page_number-1} pages)")
            break

if __name__ == "__main__":
    main()