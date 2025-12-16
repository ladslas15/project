import sqlite3
import hashlib

def get_connection():
    """Get database connection"""
    return sqlite3.connect("payroll.db")

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def get_payroll_report_data(date_filter=None):
    """
    Fetch payroll report data.
    
    Args:
        date_filter: Optional date to filter by (not used in current schema)
    
    Returns:
        List of tuples containing (emp_id, name, net_salary)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            SELECT 
                e.id,
                e.name,
                p.net_salary
            FROM employees e
            INNER JOIN payroll p ON e.id = p.emp_id
            ORDER BY e.name
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        conn.close()

def get_all_employees():
    """Get all employees"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, department, salary FROM employees ORDER BY name")
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def get_employee_by_id(emp_id):
    """Get employee by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id, name, department, salary FROM employees WHERE id = ?", (emp_id,))
        return cursor.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        conn.close()

def add_employee(name, department, salary):
    """Add new employee"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO employees (name, department, salary)
            VALUES (?, ?, ?)
        """, (name, department, salary))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def update_employee(emp_id, name, department, salary):
    """Update employee"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            UPDATE employees 
            SET name = ?, department = ?, salary = ?
            WHERE id = ?
        """, (name, department, salary, emp_id))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def delete_employee(emp_id):
    """Delete employee and related payroll records"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Delete related payroll records first
        cursor.execute("DELETE FROM payroll WHERE emp_id = ?", (emp_id,))
        # Delete employee
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def add_payroll(emp_id, net_salary):
    """Add payroll record"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO payroll (emp_id, net_salary)
            VALUES (?, ?)
        """, (emp_id, net_salary))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()

def get_payroll_by_employee(emp_id):
    """Get all payroll records for a specific employee"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, emp_id, net_salary
            FROM payroll
            WHERE emp_id = ?
            ORDER BY id DESC
        """, (emp_id,))
        return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        conn.close()

def verify_user(username, password):
    """Verify user credentials for login"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            SELECT id FROM users 
            WHERE username = ? AND password_hash = ?
        """, (username, password_hash))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        conn.close()

def add_user(username, password):
    """Add a new user"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        password_hash = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        return None
    finally:
        conn.close()