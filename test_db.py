# test_db.py
import sqlite3
import os

def check_database():
    db_path = 'weak_passwords.db'
    if not os.path.exists(db_path):
        print(f"Database file {db_path} does not exist.")
        return
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='weak_passwords'")
        if cursor.fetchone():
            print("Table 'weak_passwords' exists.")
            cursor.execute("SELECT COUNT(*) FROM weak_passwords")
            count = cursor.fetchone()[0]
            print(f"Table contains {count} passwords.")
        else:
            print("Table 'weak_passwords' does not exist.")
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    check_database()