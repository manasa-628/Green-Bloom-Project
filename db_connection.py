import mysql.connector


def get_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="manasa28",
        database="green_bloom_db"
    )

    return conn

if __name__ == "__main__":
    conn = get_connection()

    if conn.is_connected():
        print("Database connected successfully!")

    conn.close()