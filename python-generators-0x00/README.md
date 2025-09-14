# PostgreSQL Database Seeder

A Python script to set up and populate a PostgreSQL database with user data from CSV files.

## Overview

This project contains a database seeder script that creates and populates the `ALX_prodev` database with user information. The script handles database connection, table creation, and data insertion with duplicate prevention.

## Features

- **Database Management**: Creates the `ALX_prodev` database if it doesn't exist
- **Table Creation**: Sets up the `user_data` table with proper schema
- **UUID Generation**: Automatically generates unique UUIDs for each user
- **Duplicate Prevention**: Checks for existing emails before inserting new records
- **CSV Import**: Reads user data from CSV files and imports into the database
- **Error Handling**: Comprehensive error handling for database operations

## Database Schema

The `user_data` table contains the following fields:

- `user_id` (UUID, Primary Key, Indexed)
- `name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, NOT NULL)
- `age` (DECIMAL, NOT NULL)

## Prerequisites

- Python 3.6+
- PostgreSQL database server
- Required Python packages:
  ```bash
  pip install psycopg2-binary
  ```

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies**:
   ```bash
   pip install psycopg2-binary
   ```

3. **Configure database credentials**:
   Edit the `seed.py` file and update the following variables with your PostgreSQL credentials:
   ```python
   user='postgres'  # Your PostgreSQL username
   password='your_actual_password'  # Your PostgreSQL password
   ```

4. **Prepare your CSV file**:
   Create a `user_data.csv` file in the same directory as `seed.py` with the following format:
   ```csv
   name,email,age
   John Doe,john@example.com,25
   Jane Smith,jane@example.com,30
   Bob Johnson,bob@example.com,35
   ```

## Usage

Run the seeder script:

```bash
python seed.py
```

The script will:
1. Connect to your PostgreSQL server
2. Create the `alx_prodev` database (if it doesn't exist)
3. Create the `user_data` table (if it doesn't exist)
4. Read data from `user_data.csv`
5. Insert new records (skipping duplicates based on email)
6. Generate UUIDs for each new user

## Functions

### Core Functions

- `connect_db()`: Connects to the PostgreSQL database server
- `create_database(connection)`: Creates the `alx_prodev` database if it doesn't exist
- `connect_to_prodev()`: Connects to the `alx_prodev` database
- `create_table(connection)`: Creates the `user_data` table with required fields
- `insert_data(connection, data)`: Inserts data into the database, preventing duplicates

## Error Handling

The script includes comprehensive error handling for:
- Database connection failures
- Missing CSV files
- Invalid data formats
- Duplicate email entries
- SQL execution errors

## Example Output

```
Connected to alx_prodev database successfully
Looking for CSV at: /path/to/your/project/user_data.csv
Data inserted successfully
```

## Troubleshooting

### Common Issues

1. **"psql is not recognized"**:
   - Add PostgreSQL to your system PATH
   - Or use the full path to PostgreSQL binaries

2. **"user_data.csv file not found"**:
   - Ensure the CSV file is in the same directory as `seed.py`
   - Check that the filename is exactly `user_data.csv`

3. **"connection failed"**:
   - Verify PostgreSQL service is running
   - Check your username and password in the script
   - Ensure PostgreSQL is listening on localhost:5432

4. **"can't adapt type 'UUID'"**:
   - This has been fixed in the current version by converting UUID to string

## CSV File Format

Your CSV file should have the following headers:
- `name`: User's full name
- `email`: User's email address (used for duplicate checking)
- `age`: User's age (numeric value)

Example:
```csv
name,email,age
Alice Johnson,alice@example.com,28
Bob Wilson,bob@example.com,34
Carol Davis,carol@example.com,22
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Created as part of the ALX Software Engineering program.