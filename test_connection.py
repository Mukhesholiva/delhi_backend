import pyodbc

def test_connection():
    db_config = {
        'server': '111.93.26.122',
        'database': 'Delhi',
        'username': 'sa',
        'password': 'Oliva@9876'
    }
    
    try:
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={db_config['server']};"
            f"DATABASE={db_config['database']};"
            f"UID={db_config['username']};"
            f"PWD={db_config['password']};"
            "ConnectRetryCount=3;"
            "ConnectRetryInterval=10;"
        )
        
        print("Testing connection with string:")
        print(connection_string)
        print("\nAttempting to connect...")
        
        conn = pyodbc.connect(connection_string)
        print("✅ Connection successful!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT @@VERSION")
        version = cursor.fetchone()[0]
        print(f"SQL Server Version: {version}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()



