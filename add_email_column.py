import pyodbc
from urllib.parse import quote_plus

# Database connection
db_config = {
    'server': '111.93.26.122',
    'database': 'Delhi',
    'username': 'sa',
    'password': 'Oliva@9876'
}

connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"UID={db_config['username']};"
    f"PWD={db_config['password']};"
    "ConnectRetryCount=3;"
    "ConnectRetryInterval=10;"
)

def add_email_column():
    """Add email_id column to credit_balances table."""
    try:
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'credit_balances' 
            AND COLUMN_NAME = 'email_id'
        """)
        
        if cursor.fetchone():
            print("Column 'email_id' already exists.")
        else:
            # Add the email_id column
            cursor.execute("""
                ALTER TABLE credit_balances 
                ADD email_id VARCHAR(255) NULL
            """)
            print("Column 'email_id' added successfully.")
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding email_id column: {e}")
        return False

if __name__ == "__main__":
    add_email_column()
