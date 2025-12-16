import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

conn = sqlite3.connect("payroll.db")
cursor = conn.cursor()

# -----------------------------
# Drop tables (development only)
# -----------------------------
cursor.execute("DROP TABLE IF EXISTS payroll")
cursor.execute("DROP TABLE IF EXISTS employees")
cursor.execute("DROP TABLE IF EXISTS users")

# -----------------------------
# Users table (Login)
# -----------------------------
cursor.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)
""")

# -----------------------------
# Employees table
# -----------------------------
cursor.execute("""
CREATE TABLE employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    salary REAL NOT NULL
)
""")

# -----------------------------
# Payroll table (IMPORTANT)
# -----------------------------
cursor.execute("""
CREATE TABLE payroll (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id INTEGER NOT NULL,
    net_salary REAL NOT NULL,
    FOREIGN KEY (emp_id) REFERENCES employees(id)
)
""")

# -----------------------------
# Insert default admin
# -----------------------------
cursor.execute("""
INSERT INTO users (username, password_hash)
VALUES (?, ?)
""", ("admin", hash_password("admin123")))

# -----------------------------
# Sample employees
# -----------------------------
cursor.executemany("""
INSERT INTO employees (name, department, salary)
VALUES (?, ?, ?)
""", [
    ("Batimbo Ladslas", "Finance", 1200000),
    ("Kayanja Samuel", "IT", 950000)
])

# -----------------------------
# Sample payroll data
# -----------------------------
cursor.executemany("""
INSERT INTO payroll (emp_id, net_salary)
VALUES (?, ?)
""", [
    (1, 1200000),
    (2, 950000)
])

conn.commit()
conn.close()

print("Database created successfully!")
