import mysql.connector
from mysql.connector import Error
from app.config import DB_CONFIG 

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"]
        )
        cursor = conn.cursor()

        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
        conn.commit()
        conn.close()

        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS bills (
                id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT,
                amount DECIMAL(10,2) NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        return conn  
    
    except Error as e:
        print(f"Error: {e}")
        return None



def execute_query(query, values=None, fetch=False):
    conn = connect_db()
    if not conn:
        print("Failed to connect to database.")
        return None

    cursor = conn.cursor()
    cursor.execute(query, values or ())
    
    if fetch:
        result = cursor.fetchall()
        conn.close()
        return result
    
    conn.commit()
    conn.close()
