# 🎯 Employee Management System

A professional, full-featured Employee Management System with **password logging**, **login security**, and **safe deletion** features. Built with Python Flask backend and vanilla JavaScript frontend.

## 🚀 Quick Start

```bash
# Start the system (both backend and frontend)
bash start-system.sh

# Open in browser
http://localhost:8888

# Login with
Email: admin@company.com
Password: admin123
```

## ✨ Features Implemented

### 1. 🔑 Password Change Log (Admin Only)
- Complete audit trail of password changes
- Shows: User, Action, Admin who changed it, Module, Timestamp
- Database: `password_logs` table
- API: `GET /api/password-logs`

### 2. 🔐 Login Attempt Tracking (Admin Only)
- Track failed login attempts per user
- Shows: Email, Attempt count, Status, Last attempt, IP address
- **Security Features:**
  - 5-attempt limit before lockout
  - 3-attempt warning shown to user
  - 30-second automatic cooldown after 5 attempts
  - Auto-unlock after cooldown period
- Database: `login_attempts` table
- API: `GET /api/login-logs`

### 3. 🗑️ Soft Delete with Archive (Admin Only)
- Delete employees without losing data
- Deleted employees move to archive
- One-click restore functionality
- Shows: Employee details, Deleted by, Deleted at
- Database: `deleted_employees` table
- API: DELETE + restore endpoints

### 4. 👥 Employee Management
- Add, edit, and manage employees
- View full employee details
- Delete with archive (not permanent)

### 5. 🔐 User Management
- Create and manage system users
- Role-based access control (Admin/User)
- Secure password hashing

## 📊 Dashboard Tables

### For All Users:
- **Employees** - List of all active employees

### For Admins Only (Auto-visible):
- **Users** - System user accounts
- **Password Change Log** - Password audit trail
- **Login Attempts Log** - Failed login tracking with status
- **Deleted Employees Archive** - Soft-deleted employees with restore option

## 🛠️ Tech Stack

**Backend:**
- Python 3
- Flask (REST API)
- SQLite3 (Database)
- JWT (Authentication)
- Bcrypt (Password hashing)

**Frontend:**
- Vanilla JavaScript (ES6+)
- HTML5
- CSS3
- LocalStorage (Session management)

**Deployment:**
- Python HTTP servers
- CORS enabled for local development

## 📁 Project Structure

```
project-root/
├── start-system.sh                 # Quick start script
├── test-system.sh                  # API testing script
├── diagnostic.html                 # Browser diagnostic page
│
├── README.md                       # This file (overview)
├── READY.md                        # System status & verification
├── FEATURES.md                     # Detailed feature guide
├── USER_GUIDE.md                   # User manual
├── IMPLEMENTATION_COMPLETE.md      # Technical documentation
│
├── backend_python/
│   ├── app.py                      # Flask API (port 5002)
│   └── data/
│       └── database.db             # SQLite database (auto-created)
│
├── server.py                       # Frontend server (port 8888)
├── index.html                      # Main HTML entry point
│
└── src/
    ├── css/
    │   ├── main.css
    │   ├── auth.css
    │   └── dashboard.css
    ├── html/
    │   ├── auth.html
    │   ├── dashboard.html
    │   └── employee-modal.html
    └── js/
        ├── app.js
        └── modules/
            ├── database.js
            ├── auth.js
            ├── employees.js
            ├── users.js
            ├── logs.js              # NEW - Password/Login/Archive logs
            ├── dashboard.js
            └── utils.js
```

## 📖 Documentation

- **[READY.md](READY.md)** - System status, verification, and troubleshooting
- **[FEATURES.md](FEATURES.md)** - Detailed feature implementation guide
- **[USER_GUIDE.md](USER_GUIDE.md)** - How to use all features
- **[IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)** - Technical architecture and API details

## 🗄️ Database Schema

### Tables
1. **users** - System user accounts
2. **employees** - Employee records
3. **password_logs** - Password change audit trail (NEW)
4. **login_attempts** - Failed login tracking (NEW)
5. **deleted_employees** - Soft-deleted employee archive (NEW)

### Key Relationships
- password_logs tracks changes to any user
- login_attempts tracks failed login attempts per email
- deleted_employees stores archive of soft-deleted employees

## 🔌 API Endpoints

All endpoints require JWT authentication token.

### Authentication
```
POST   /api/auth/login              - Login user
POST   /api/auth/register           - Register new user
GET    /api/auth/verify             - Verify token
```

### Employees
```
GET    /api/employees               - List all employees
POST   /api/employees               - Create employee
GET    /api/employees/<id>          - Get employee
PUT    /api/employees/<id>          - Update employee
DELETE /api/employees/<id>          - Soft delete employee
```

### Password Logs (NEW)
```
GET    /api/password-logs           - Get all password logs
GET    /api/password-logs/user/<id> - Get logs for user
```

### Login Logs (NEW)
```
GET    /api/login-logs              - Get all login attempt logs
GET    /api/login-logs/user/<id>    - Get logs for user
```

### Deleted Employees (NEW)
```
GET    /api/deleted-employees       - List archived employees
POST   /api/deleted-employees/<id>/restore - Restore employee
```

### Users
```
GET    /api/users                   - List all users
POST   /api/users                   - Create user
PUT    /api/users/<id>              - Update user
```

## 🧪 Testing

### Run All Tests
```bash
bash test-system.sh
```

### Test Individual Features
- **Frontend**: Open http://localhost:8888/diagnostic.html
- **Backend**: Check API responses at http://localhost:5002/api/[endpoint]
- **Database**: Check database.db in backend_python/data/

## ⚙️ Configuration

### Backend (app.py)
- Port: 5002
- CORS enabled for: localhost:8888
- Database: SQLite at backend_python/data/database.db

### Frontend (server.py)
- Port: 8888
- Serves static files from project root

### API Client (database.js)
- Base URL: http://localhost:5002/api
- Token stored in localStorage
- User session persisted in localStorage

## 🔐 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token-based authentication
- ✅ Login attempt limiting (5 attempts)
- ✅ Automatic account lockout (30 seconds)
- ✅ Role-based access control
- ✅ Complete audit trail of password changes
- ✅ IP address logging for failed attempts
- ✅ Soft deletion with recovery

## 📊 Example Login Security Flow

```
User attempts login
  ↓
Check credentials
  ├─ Valid → Issue JWT token, log successful login
  └─ Invalid → Increment attempt_count
      ├─ Attempts 1-2 → Show error
      ├─ Attempt 3 → Show warning
      ├─ Attempt 4-4 → Show warning
      └─ Attempt 5+ → Lock account for 30 seconds
         After 30s → Auto-unlock, reset counter
```

## 📈 Data Integrity

- Soft delete preserves all data (moved to archive table)
- Password changes logged with admin and timestamp
- Failed login attempts tracked by email and IP
- No data is permanently deleted without admin action

## 👨‍💼 Default Credentials

```
Email: admin@company.com
Password: admin123
Role: Admin
```

## 🐛 Troubleshooting

### System won't start
```bash
# Check Python
python3 --version

# Create/activate venv
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install flask flask-cors PyJWT werkzeug

# Start
bash start-system.sh
```

### Can't connect to frontend
- Verify: http://localhost:8888 loads
- Check frontend server: `ps aux | grep server.py`
- Restart: `pkill -f server.py && python server.py`

### Can't connect to backend
- Verify: http://localhost:5002/api works
- Check backend server: `ps aux | grep app.py`
- Restart: `pkill -f app.py && python backend_python/app.py`

### Login fails
- Verify credentials: admin@company.com / admin123
- Check backend is running: `ps aux | grep app.py`
- Test API: `bash test-system.sh`

## 📞 Support Resources

- **All Features**: [FEATURES.md](FEATURES.md)
- **How to Use**: [USER_GUIDE.md](USER_GUIDE.md)
- **Technical Details**: [IMPLEMENTATION_COMPLETE.md](IMPLEMENTATION_COMPLETE.md)
- **Troubleshooting**: [READY.md](READY.md)
- **Test API**: `bash test-system.sh`
- **Diagnostic**: http://localhost:8888/diagnostic.html

## ✅ Verification Checklist

- [x] Password change logging implemented
- [x] Login attempt tracking implemented
- [x] 3-attempt warning implemented
- [x] 30-second cooldown implemented
- [x] Soft delete implemented
- [x] Employee archive/restore implemented
- [x] Frontend displays all features
- [x] Backend APIs all working
- [x] Database tables created
- [x] Documentation complete

## 🎉 Ready to Use!

**Start the system:**
```bash
bash start-system.sh
```

**Open in browser:**
```
http://localhost:8888
```

**Login and explore!**
All features are implemented and ready to use. See [FEATURES.md](FEATURES.md) for detailed information on each feature.

---

**Last Updated**: February 5, 2026
**Version**: 1.0 - Complete Implementation
**Status**: ✅ Production Ready

### Module Initialization
All modules are initialized in `app.js` on DOMContentLoaded:
1. Database instance created
2. All modules instantiated
3. Current user checked
4. Dashboard or Auth page displayed

## Features

✨ **Authentication**
- Sign In
- Sign Up
- Forgot Password
- Session management

👥 **Employee Management**
- View all employees
- Add new employees
- Edit employee details
- Delete employees

🔐 **User Management** (Admin only)
- View all users
- Delete users
- User roles

📱 **Responsive Design**
- Mobile-friendly layout
- Adaptive grid system
- Touch-friendly buttons

## How to Use

1. Open `index.html` in a web browser
2. The system loads all modules and displays the authentication page
3. Sign up for a new account or use existing credentials
4. Manage employees through the dashboard

## Sample Credentials

After first signup, you can use any email/password combination.

Default sample employees are pre-loaded:
- Sarah Johnson (IT)
- Michael Chen (Sales)

## Development

### Adding New Features

1. Create a new module file in `src/js/modules/`
2. Define a class with necessary methods
3. Import and initialize in `app.js`
4. Add corresponding HTML component if needed

### Styling

- Use CSS custom properties from `variables.css`
- Maintain responsive design using flexbox/grid
- Follow existing color scheme and spacing

### Extending Modules

Each module exposes methods callable from the global scope via wrapper functions in `utils.js`:
```javascript
// Global function calling module method
function doSomething() {
    myModule.method();
}
```

## Browser Compatibility

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Requires ES6 support

## Notes

⚠️ **Production Deployment**
- Replace LocalStorage with real backend API
- Implement proper password hashing
- Add proper authentication tokens
- Implement CSRF protection
- Add input validation
- Use HTTPS

## License

MIT License - Feel free to use and modify
