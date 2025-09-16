import asyncio
import asyncpg
import time

# Database connection configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': '2Cedicray123@.',
    'database': 'ALX_prodev'
}

async def async_fetch_users():
    """
    Asynchronously fetch all users from the database.
    
    Returns:
        list: All users from the users table
    """
    print("Starting async_fetch_users...")
    
    try:
        # Create connection
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Execute query
        query = "SELECT * FROM user_data"
        results = await conn.fetch(query)
        
        # Close connection
        await conn.close()
        
        print(f"async_fetch_users completed: Found {len(results)} users")
        return results
        
    except Exception as e:
        print(f"Error in async_fetch_users: {e}")
        return []

async def async_fetch_older_users():
    """
    Asynchronously fetch users older than 40 from the database.
    
    Returns:
        list: Users older than 40
    """
    print("Starting async_fetch_older_users...")
    
    try:
        # Create connection
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Execute query with parameter
        query = "SELECT * FROM user_data WHERE age > $1"
        results = await conn.fetch(query, 40)
        
        # Close connection
        await conn.close()
        
        print(f"async_fetch_older_users completed: Found {len(results)} users older than 40")
        return results
        
    except Exception as e:
        print(f"Error in async_fetch_older_users: {e}")
        return []

async def fetch_concurrently():
    """
    Execute multiple database queries concurrently using asyncio.gather.
    """
    print("=" * 60)
    print("STARTING CONCURRENT DATABASE QUERIES")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Use asyncio.gather to run both queries concurrently
        all_users, older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
        )
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\nConcurrent execution completed in {execution_time:.2f} seconds")
        print("=" * 60)
        
        # Display results for all users
        print("\nALL USERS:")
        print("-" * 40)
        if all_users:
            for user in all_users:
                print(f"ID: {user['user_id']}, Name: {user['name']}, Age: {user['age']}, Email: {user['email']}")
        else:
            print("No users found")
        
        # Display results for older users
        print(f"\nUSERS OLDER THAN 40:")
        print("-" * 40)
        if older_users:
            for user in older_users:
                print(f"ID: {user['user_id']}, Name: {user['name']}, Age: {user['age']}, Email: {user['email']}")
        else:
            print("No users older than 40 found")
        
        print(f"\nSUMMARY:")
        print(f"Total users: {len(all_users)}")
        print(f"Users older than 40: {len(older_users)}")
        
        return all_users, older_users
        
    except Exception as e:
        print(f"Error during concurrent execution: {e}")
        return [], []

async def setup_sample_data():
    """
    Create sample table and insert test data for demonstration.
    """
    print("Setting up sample data...")
    
    try:
        conn = await asyncpg.connect(**DB_CONFIG)
        
        # Create user_data table
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS user_data (
                user_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                age INTEGER NOT NULL
            )
        ''')
        
        # Insert sample data
        sample_users = [
            ('John Doe', 'john@example.com', 35),
            ('Jane Smith', 'jane@example.com', 28),
            ('Bob Johnson', 'bob@example.com', 45),
            ('Alice Brown', 'alice@example.com', 22),
            ('Charlie Wilson', 'charlie@example.com', 52),
            ('Diana Prince', 'diana@example.com', 41),
            ('Frank Miller', 'frank@example.com', 38),
            ('Grace Lee', 'grace@example.com', 29)
        ]
        
        for name, email, age in sample_users:
            try:
                await conn.execute(
                    'INSERT INTO user_data (name, email, age) VALUES ($1, $2, $3)',
                    name, email, age
                )
            except asyncpg.UniqueViolationError:
                # User already exists, skip
                pass
        
        await conn.close()
        print("Sample data setup completed")
        
    except Exception as e:
        print(f"Error setting up sample data: {e}")

# Alternative approach using connection pool for better performance
async def fetch_concurrently_with_pool():
    """
    Execute queries concurrently using a connection pool for better performance.
    """
    print("=" * 60)
    print("CONCURRENT QUERIES WITH CONNECTION POOL")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Create connection pool
        pool = await asyncpg.create_pool(**DB_CONFIG, min_size=2, max_size=5)
        
        async def fetch_all_users_pool():
            async with pool.acquire() as conn:
                results = await conn.fetch("SELECT * FROM user_data")
                print(f"Pool: async_fetch_users completed: Found {len(results)} users")
                return results
        
        async def fetch_older_users_pool():
            async with pool.acquire() as conn:
                results = await conn.fetch("SELECT * FROM user_data WHERE age > $1", 40)
                print(f"Pool: async_fetch_older_users completed: Found {len(results)} users older than 40")
                return results
        
        # Execute concurrently using the pool
        all_users, older_users = await asyncio.gather(
            fetch_all_users_pool(),
            fetch_older_users_pool()
        )
        
        # Close the pool
        await pool.close()
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\nPool-based execution completed in {execution_time:.2f} seconds")
        print(f"Total users: {len(all_users)}, Users older than 40: {len(older_users)}")
        
        return all_users, older_users
        
    except Exception as e:
        print(f"Error during pool-based execution: {e}")
        return [], []

# Main execution function
async def main():
    """Main function to demonstrate concurrent database operations."""
    
    # Setup sample data (uncomment if needed)
    # await setup_sample_data()
    
    print("DEMONSTRATION: Concurrent PostgreSQL Queries with asyncpg")
    print("=" * 70)
    
    # Method 1: Basic concurrent execution
    await fetch_concurrently()
    
    print("\n" + "=" * 70)
    
    # Method 2: Using connection pool (recommended for production)
    await fetch_concurrently_with_pool()

# Run the async program
if __name__ == "__main__":
    asyncio.run(main())