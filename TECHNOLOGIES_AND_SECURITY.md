# Technologies and Tools

## Current Stack (Python/Flask)

### Backend
- **Python 3**: Server-side processing, form handling, and database query execution
- **Flask**: Lightweight, flexible web framework for building REST API endpoints
- **SQLite3**: Relational database management system for storing user and employee records
  - File-based, no server needed
  - Perfect for development and small-to-medium deployments
  - Located at: `backend_python/data/database.db`
- **Virtual Environment (venv)**: Isolated Python environment for dependency management

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Styling with CSS custom properties and responsive design patterns
- **JavaScript (ES6+)**: Client-side logic, API interactions, and dynamic UI updates

### Key Libraries
- **Flask-CORS**: Cross-Origin Resource Sharing support
- **PyJWT**: JWT token generation and verification
- **werkzeug.security**: Password hashing and verification

---

# Security Applied

## 1. Password Hashing ✅

**Implementation**: Using `werkzeug.security` module
```python
from werkzeug.security import generate_password_hash, check_password_hash

# During registration
hashed_password = generate_password_hash(password)  # PBKDF2 with salt

# During login
if check_password_hash(stored_hash, entered_password):
    # User authenticated
```

**Benefits**:
- User credentials are **never stored as plain text**
- Uses PBKDF2 algorithm with automatic salt generation
- One-way hashing ensures passwords cannot be reversed
- Even if database is compromised, passwords remain secure

---

## 2. Prepared Statements ✅

**Implementation**: SQL parameterized queries prevent SQL Injection

```python
# Safe - uses placeholders
cursor.execute('SELECT * FROM users WHERE email = ?', (email,))

# Safe - prevents SQL injection
cursor.execute('SELECT * FROM employees WHERE id = ?', (employee_id,))

# NEVER do this:
# cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')  # VULNERABLE!
```

**Benefits**:
- Separates SQL logic from user-supplied data
- Prevents SQL Injection attacks
- Database interprets user input as data, not code
- SQLite automatically escapes special characters

---

## 3. JWT Token-Based Authentication ✅

**Implementation**: JSON Web Token authentication

```python
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing!'}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user_id']
        except:
            return {'message': 'Token is invalid!'}, 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    # Only authenticated users reach here
    pass
```

**Benefits**:
- Tokens include expiration timestamps (1 hour default)
- Only authenticated users can access sensitive endpoints
- Stateless authentication (no session storage needed)
- Secure token validation on every request
- Clear separation between public and protected routes

---

## 4. CORS Protection ✅

**Implementation**: Restrict API access to authorized origins

```python
CORS(app, 
     origins=['http://localhost:8888', 'http://localhost:5001', 
              'http://127.0.0.1:8888', 'http://127.0.0.1:5001'],
     supports_credentials=True,
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
     allow_headers=['Content-Type', 'Authorization'])
```

**Benefits**:
- Prevents unauthorized cross-origin requests
- Only whitelisted domains can access the API
- Specifies allowed HTTP methods and headers
- Supports credentials in requests
- Protects against Cross-Site Request Forgery (CSRF)

---

## 5. Foreign Key Constraints ✅

**Implementation**: Referential integrity at database level

```python
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")  # Enable constraints
    return conn
```

**Benefits**:
- Enforces relationships between tables
- Prevents orphaned records (e.g., employees without valid user_id)
- Automatic cascade operations (delete related records)
- Data consistency and integrity

**Example Schema**:
```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
```

---

## 6. Additional Security Measures

### Input Validation
- Email format validation
- Password strength requirements
- Field length restrictions
- Type checking before database operations

### Error Handling
- Generic error messages (no sensitive data exposed)
- Proper HTTP status codes
- Server-side validation (never trust client input alone)

### Environment Variables
- Secret key stored separately (should be in `.env` file in production)
- Database path configurable
- Port configuration separate from code

---

## Summary

| Security Feature | Implementation | Status |
|---|---|---|
| Password Hashing | werkzeug.security | ✅ Active |
| SQL Injection Prevention | Prepared Statements | ✅ Active |
| Authentication | JWT Tokens | ✅ Active |
| Cross-Origin Protection | CORS Configuration | ✅ Active |
| Data Integrity | Foreign Key Constraints | ✅ Active |
| Input Validation | Server-side checks | ✅ Active |

All traditional PHP/MySQL security practices have been successfully migrated to the Python/Flask/SQLite3 stack with modern, production-ready implementations.
