import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

cursor.execute("""
INSERT OR IGNORE INTO users (username, password_hash)
VALUES (?, ?)
""", ("admin", hash_password("admin123")))



conn.commit()
conn.close()
