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

def stream_users_in_batches(batch_size):
    """
    Generator function that fetches rows from user_data table in batches.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: Batch of user records as dictionaries
    """
    connection = connect_to_alx_prodev()
    if not connection:
        return
    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data ORDER BY name")
        
        while True:
            # Fetch batch_size number of rows
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            
            # Convert rows to list of dictionaries
            batch = []
            for row in rows:  # Loop 1
                user_data = {
                    'user_id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'age': row[3]
                }
                batch.append(user_data)
            
            yield batch
            
    except Error as e:
        print(f"Error streaming batches: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def batch_processing(batch_size):
    """
    Processes batches of users and filters users over the age of 25.
    
    Args:
        batch_size (int): Size of each batch to process
    """
    total_processed = 0
    total_over_25 = 0
    
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        batch_count = len(batch)
        filtered_users = []
        
        for user in batch:  # Loop 3
            if user['age'] > 25:
                filtered_users.append(user)
        
        # Process the filtered batch
        total_processed += batch_count
        total_over_25 += len(filtered_users)
        
        print(f"Batch processed: {batch_count} users, {len(filtered_users)} over age 25")
        
        # Display users over 25 in current batch
        for user in filtered_users:
            print(f"  - {user['name']} ({user['email']}) - Age: {user['age']}")
    
    print(f"\nSummary:")
    print(f"Total users processed: {total_processed}")
    print(f"Users over 25: {total_over_25}")

# Example usage
def main():
    print("Processing users in batches of 5:")
    print("-" * 50)
    batch_processing(5)

if __name__ == "__main__":
    main()