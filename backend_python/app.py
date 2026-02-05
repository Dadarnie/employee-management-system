#!/usr/bin/env python3
"""
Employee Management System Backend
Python/Flask alternative to Node.js backend
Provides REST API for authentication and employee/user management
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import sqlite3
import os
import json
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-this'

# Enable CORS with proper configuration
CORS(app, 
     origins=['http://localhost:7777', 'http://localhost:8888', 'http://localhost:9000', 
              'http://127.0.0.1:7777', 'http://127.0.0.1:8888', 'http://127.0.0.1:9000'],
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'database.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT,
            position TEXT,
            salary REAL,
            phone TEXT,
            hire_date DATE,
            address TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create password log table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            changed_by_user_id INTEGER,
            changed_by_name TEXT,
            module TEXT,
            old_password_hash TEXT,
            new_password_hash TEXT,
            ip_address TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (changed_by_user_id) REFERENCES users(id)
        )
    ''')
    
    # Create login attempts table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS login_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            email TEXT NOT NULL,
            attempt_count INTEGER DEFAULT 1,
            last_attempt_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_locked INTEGER DEFAULT 0,
            cooldown_until TIMESTAMP,
            ip_address TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create deleted employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deleted_employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT,
            department TEXT,
            position TEXT,
            salary REAL,
            phone TEXT,
            hire_date DATE,
            address TEXT,
            deleted_by_user_id INTEGER,
            deleted_by_name TEXT,
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deletion_reason TEXT,
            FOREIGN KEY (deleted_by_user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    
    # Seed admin user if not exists
    cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@company.com',))
    if not cursor.fetchone():
        hashed_pw = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('Admin User', 'admin@company.com', hashed_pw, 'admin'))
        conn.commit()
        print('✓ Admin user created: admin@company.com / admin123')
    
    # Seed sample employees if not exists
    cursor.execute('SELECT COUNT(*) FROM employees')
    if cursor.fetchone()[0] == 0:
        employees = [
            ('John', 'Smith', 'john.smith@company.com', 'IT', 'Developer', 75000, '555-0101', '2022-01-15', '123 Main St'),
            ('Sarah', 'Johnson', 'sarah.j@company.com', 'HR', 'Manager', 85000, '555-0102', '2021-06-20', '456 Oak Ave'),
            ('Mike', 'Brown', 'mike.brown@company.com', 'Sales', 'Executive', 80000, '555-0103', '2022-03-10', '789 Pine Rd'),
        ]
        for emp in employees:
            cursor.execute('''
                INSERT INTO employees (first_name, last_name, email, department, position, salary, phone, hire_date, address)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', emp)
        conn.commit()
        print(f'✓ {len(employees)} sample employees created')
    
    conn.close()

def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(' ')[1]
            except:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    return decorated

def dict_from_row(row):
    """Convert sqlite3.Row to dict"""
    if row is None:
        return None
    return dict(row)

# ============ Authentication Routes ============

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if email exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create new user
    hashed_pw = generate_password_hash(data['password'])
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['email'], hashed_pw, 'user'))
        conn.commit()
        
        # Get created user
        cursor.execute('SELECT id, name, email, role FROM users WHERE email = ?', (data['email'],))
        user = dict_from_row(cursor.fetchone())
        
        # Generate token
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(days=7)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        conn.close()
        return jsonify({'user': user, 'token': token}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login with email and password with attempt tracking"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing email or password'}), 400
    
    email = data['email']
    password = data['password']
    ip_address = request.remote_addr
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check login attempts
    cursor.execute('SELECT * FROM login_attempts WHERE email = ?', (email,))
    login_attempt = cursor.fetchone()
    
    if login_attempt:
        if login_attempt['is_locked']:
            cooldown_time = datetime.fromisoformat(login_attempt['cooldown_until'])
            if datetime.utcnow() < cooldown_time:
                remaining = (cooldown_time - datetime.utcnow()).total_seconds()
                conn.close()
                return jsonify({
                    'error': f'Account locked. Try again in {int(remaining)} seconds',
                    'locked': True,
                    'remaining_cooldown': int(remaining)
                }), 429
            else:
                # Cooldown expired, unlock account
                cursor.execute('UPDATE login_attempts SET is_locked = 0, attempt_count = 0 WHERE email = ?', (email,))
                conn.commit()
    
    # Verify credentials
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_row = cursor.fetchone()
    
    if not user_row or not check_password_hash(user_row['password'], password):
        # Log failed attempt
        if login_attempt:
            new_count = login_attempt['attempt_count'] + 1
            cursor.execute('''
                UPDATE login_attempts 
                SET attempt_count = ?, last_attempt_time = CURRENT_TIMESTAMP
                WHERE email = ?
            ''', (new_count, email))
            
            # Check if reached limit
            if new_count >= 5:
                cooldown_until = datetime.utcnow() + timedelta(seconds=30)
                cursor.execute('''
                    UPDATE login_attempts 
                    SET is_locked = 1, cooldown_until = ?
                    WHERE email = ?
                ''', (cooldown_until.isoformat(), email))
                conn.commit()
                conn.close()
                return jsonify({
                    'error': 'Account locked due to too many failed attempts. Try again in 30 seconds',
                    'locked': True,
                    'remaining_cooldown': 30
                }), 429
            elif new_count == 3:
                conn.commit()
                conn.close()
                return jsonify({
                    'error': 'Invalid email or password. Warning: 2 more attempts before 30-second cooldown',
                    'attempts_remaining': 5 - new_count,
                    'warning': True
                }), 401
            else:
                conn.commit()
                conn.close()
                return jsonify({
                    'error': 'Invalid email or password',
                    'attempts_remaining': 5 - new_count
                }), 401
        else:
            # First failed attempt
            cursor.execute('''
                INSERT INTO login_attempts (email, user_id, attempt_count, ip_address)
                VALUES (?, ?, 1, ?)
            ''', (email, user_row['id'] if user_row else None, ip_address))
            conn.commit()
            conn.close()
            return jsonify({'error': 'Invalid email or password'}), 401
    
    # Successful login - reset attempts
    if login_attempt:
        cursor.execute('UPDATE login_attempts SET attempt_count = 0, is_locked = 0 WHERE email = ?', (email,))
    
    user = {
        'id': user_row['id'],
        'name': user_row['name'],
        'email': user_row['email'],
        'role': user_row['role']
    }
    
    # Log successful login attempt
    cursor.execute('''
        INSERT INTO login_attempts (user_id, email, attempt_count, ip_address)
        VALUES (?, ?, 0, ?)
    ''', (user['id'], email, ip_address))
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'exp': datetime.utcnow() + timedelta(days=7)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    conn.commit()
    conn.close()
    
    return jsonify({'user': user, 'token': token}), 200

@app.route('/api/auth/verify', methods=['GET'])
@token_required
def verify_token(current_user_id):
    """Verify JWT token"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, role FROM users WHERE id = ?', (current_user_id,))
    user = dict_from_row(cursor.fetchone())
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200

# ============ User Routes ============

@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user_id):
    """Get all users (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all users
    cursor.execute('SELECT id, name, email, role, created_at FROM users ORDER BY created_at DESC')
    users = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(users), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user_id, user_id):
    """Get specific user"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, email, role, created_at FROM users WHERE id = ?', (user_id,))
    user = dict_from_row(cursor.fetchone())
    conn.close()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user), 200

@app.route('/api/users', methods=['POST'])
@token_required
def create_user(current_user_id):
    """Create new user (admin only)"""
    data = request.get_json()
    
    # Check admin
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Validate
    if not data or not data.get('email') or not data.get('password') or not data.get('name'):
        conn.close()
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check email exists
    cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Email already exists'}), 409
    
    # Create user
    hashed_pw = generate_password_hash(data['password'])
    role = data.get('role', 'user')
    
    try:
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', (data['name'], data['email'], hashed_pw, role))
        conn.commit()
        
        cursor.execute('SELECT id, name, email, role FROM users WHERE email = ?', (data['email'],))
        new_user = dict_from_row(cursor.fetchone())
        conn.close()
        
        return jsonify(new_user), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user_id, user_id):
    """Delete user (admin only)"""
    # Check admin
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Prevent self-deletion
    if current_user_id == user_id:
        conn.close()
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    # Delete user
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============ Employee Routes ============

@app.route('/api/employees', methods=['GET'])
@token_required
def get_employees(current_user_id):
    """Get all employees with optional filters"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Build query
    query = 'SELECT * FROM employees WHERE 1=1'
    params = []
    
    # Filters
    search = request.args.get('search', '')
    if search:
        query += ' AND (name LIKE ? OR email LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    department = request.args.get('department', '')
    if department:
        query += ' AND department = ?'
        params.append(department)
    
    is_active = request.args.get('isActive', '')
    if is_active:
        query += ' AND is_active = ?'
        params.append(1 if is_active == 'true' else 0)
    
    # Sorting
    sort_by = request.args.get('sortBy', 'created_at')
    order = request.args.get('order', 'DESC')
    query += f' ORDER BY {sort_by} {order}'
    
    cursor.execute(query, params)
    employees = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(employees), 200

@app.route('/api/employees/<int:emp_id>', methods=['GET'])
@token_required
def get_employee(current_user_id, emp_id):
    """Get specific employee"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
    employee = dict_from_row(cursor.fetchone())
    conn.close()
    
    if not employee:
        return jsonify({'error': 'Employee not found'}), 404
    
    return jsonify(employee), 200

@app.route('/api/employees', methods=['POST'])
@token_required
def create_employee(current_user_id):
    """Create new employee"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('first_name'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (first_name, last_name, email, department, position, salary, phone, hire_date, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['first_name'],
            data.get('last_name', ''),
            data['email'],
            data.get('department', ''),
            data.get('position', ''),
            data.get('salary', 0),
            data.get('phone', ''),
            data.get('hire_date', datetime.now().date()),
            data.get('address', '')
        ))
        conn.commit()
        
        emp_id = cursor.lastrowid
        cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
        employee = dict_from_row(cursor.fetchone())
        conn.close()
        
        return jsonify(employee), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:emp_id>', methods=['PUT'])
@token_required
def update_employee(current_user_id, emp_id):
    """Update employee"""
    data = request.get_json()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check exists
    cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Employee not found'}), 404
    
    # Update
    update_fields = []
    params = []
    
    for field in ['first_name', 'last_name', 'email', 'department', 'position', 'salary', 'phone', 'hire_date', 'address', 'is_active']:
        if field in data:
            update_fields.append(f'{field} = ?')
            params.append(data[field])
    
    if not update_fields:
        conn.close()
        return jsonify({'error': 'No fields to update'}), 400
    
    update_fields.append('updated_at = CURRENT_TIMESTAMP')
    params.append(emp_id)
    
    query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = ?"
    
    try:
        cursor.execute(query, params)
        conn.commit()
        
        cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
        employee = dict_from_row(cursor.fetchone())
        conn.close()
        
        return jsonify(employee), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:emp_id>', methods=['DELETE'])
@token_required
def delete_employee(current_user_id, emp_id):
    """Soft delete employee (move to deleted_employees table)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check exists
    cursor.execute('SELECT * FROM employees WHERE id = ?', (emp_id,))
    employee = cursor.fetchone()
    if not employee:
        conn.close()
        return jsonify({'error': 'Employee not found'}), 404
    
    # Get current user info
    cursor.execute('SELECT name FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    
    try:
        # Move to deleted_employees table
        cursor.execute('''
            INSERT INTO deleted_employees 
            (employee_id, first_name, last_name, email, department, position, 
             salary, phone, hire_date, address, deleted_by_user_id, deleted_by_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            emp_id,
            employee['first_name'],
            employee['last_name'],
            employee['email'],
            employee['department'],
            employee['position'],
            employee['salary'],
            employee['phone'],
            employee['hire_date'],
            employee['address'],
            current_user_id,
            user['name'] if user else 'Unknown'
        ))
        
        # Delete from active employees
        cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Employee deleted and moved to archive'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# ============ Password & Login Log Routes ============

@app.route('/api/password-logs', methods=['GET'])
@token_required
def get_password_logs(current_user_id):
    """Get password change logs (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    cursor.execute('''
        SELECT id, user_id, action, changed_by_name, module, timestamp
        FROM password_logs
        ORDER BY timestamp DESC
        LIMIT 100
    ''')
    logs = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs), 200

@app.route('/api/password-logs/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_password_logs(current_user_id, user_id):
    """Get password logs for specific user"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin or same user
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or (user['role'] != 'admin' and current_user_id != user_id):
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    cursor.execute('''
        SELECT id, action, changed_by_name, module, timestamp
        FROM password_logs
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 50
    ''', (user_id,))
    logs = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs), 200

@app.route('/api/login-logs', methods=['GET'])
@token_required
def get_login_logs(current_user_id):
    """Get login attempt logs (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    cursor.execute('''
        SELECT id, user_id, email, attempt_count, last_attempt_time, 
               is_locked, ip_address
        FROM login_attempts
        ORDER BY last_attempt_time DESC
        LIMIT 200
    ''')
    logs = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs), 200

@app.route('/api/login-logs/user/<int:user_id>', methods=['GET'])
@token_required
def get_user_login_logs(current_user_id, user_id):
    """Get login logs for specific user"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin or same user
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or (user['role'] != 'admin' and current_user_id != user_id):
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    cursor.execute('''
        SELECT id, attempt_count, last_attempt_time, is_locked, ip_address
        FROM login_attempts
        WHERE user_id = ?
        ORDER BY last_attempt_time DESC
        LIMIT 50
    ''', (user_id,))
    logs = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(logs), 200

@app.route('/api/deleted-employees', methods=['GET'])
@token_required
def get_deleted_employees(current_user_id):
    """Get deleted employees (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    cursor.execute('''
        SELECT id, employee_id, first_name, last_name, email, department, position,
               salary, phone, hire_date, deleted_by_name, deleted_at
        FROM deleted_employees
        ORDER BY deleted_at DESC
    ''')
    employees = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify(employees), 200

@app.route('/api/deleted-employees/<int:emp_id>/restore', methods=['POST'])
@token_required
def restore_employee(current_user_id, emp_id):
    """Restore deleted employee"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if admin
    cursor.execute('SELECT role FROM users WHERE id = ?', (current_user_id,))
    user = cursor.fetchone()
    if not user or user['role'] != 'admin':
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get deleted employee
    cursor.execute('SELECT * FROM deleted_employees WHERE id = ?', (emp_id,))
    deleted_emp = cursor.fetchone()
    if not deleted_emp:
        conn.close()
        return jsonify({'error': 'Deleted employee not found'}), 404
    
    try:
        # Restore to employees table
        cursor.execute('''
            INSERT INTO employees 
            (first_name, last_name, email, department, position, 
             salary, phone, hire_date, address, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            deleted_emp['first_name'],
            deleted_emp['last_name'],
            deleted_emp['email'],
            deleted_emp['department'],
            deleted_emp['position'],
            deleted_emp['salary'],
            deleted_emp['phone'],
            deleted_emp['hire_date'],
            deleted_emp['address']
        ))
        
        # Delete from deleted_employees table
        cursor.execute('DELETE FROM deleted_employees WHERE id = ?', (emp_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Employee restored'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/statistics', methods=['GET'])
@token_required
def get_statistics(current_user_id):
    """Get employee statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    stats = {}
    
    # Total employees
    cursor.execute('SELECT COUNT(*) as count FROM employees')
    stats['total'] = cursor.fetchone()['count']
    
    # By department
    cursor.execute('SELECT department, COUNT(*) as count FROM employees GROUP BY department')
    stats['by_department'] = {row['department']: row['count'] for row in cursor.fetchall()}
    
    # Average salary
    cursor.execute('SELECT AVG(salary) as avg_salary FROM employees')
    result = cursor.fetchone()
    stats['average_salary'] = result['avg_salary'] or 0
    
    # Active employees
    cursor.execute('SELECT COUNT(*) as count FROM employees WHERE is_active = 1')
    stats['active'] = cursor.fetchone()['count']
    
    conn.close()
    return jsonify(stats), 200

@app.route('/api/employees/departments', methods=['GET'])
@token_required
def get_departments(current_user_id):
    """Get list of departments"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT department FROM employees ORDER BY department')
    departments = [row['department'] for row in cursor.fetchall() if row['department']]
    conn.close()
    
    return jsonify(departments), 200

# ============ Health Check ============

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Employee Management System API',
        'version': '1.0.0',
        'docs': '/api/docs'
    }), 200

# ============ Error Handlers ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print('🔧 Initializing database...')
    init_db()
    print('✓ Database ready')
    print('\n✓ Server running on http://localhost:5002')
    print('✓ CORS enabled for: http://localhost:8888')
    print('Press Ctrl+C to stop\n')
    app.run(host='127.0.0.1', port=5002, debug=False, use_reloader=False)
