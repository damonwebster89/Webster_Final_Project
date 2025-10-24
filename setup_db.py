# setup_db.py
import sqlite3

def create_database():
    try:
        conn = sqlite3.connect('weak_passwords.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS weak_passwords (password TEXT PRIMARY KEY)''')
        common_passwords = ['123456', 'password', 'qwerty', 'admin123', 'letmein']  # Example list
        cursor.executemany('INSERT OR IGNORE INTO weak_passwords VALUES (?)', [(pwd,) for pwd in common_passwords])
        conn.commit()
        print("Database and table created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_database()