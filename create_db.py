import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

# Drop the existing employees table if it exists
cursor.execute("DROP TABLE IF EXISTS employees")

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

# Create employees table with correct columns
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

# Insert default admin user
cursor.execute("""
INSERT OR IGNORE INTO users (username, password_hash)
VALUES (?, ?)
""", ("admin", hash_password("admin123")))

conn.commit()
conn.close()

print("Database and tables created successfully!")