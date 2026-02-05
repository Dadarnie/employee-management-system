# ✨ Employee Management System - Features Guide

## 🚀 Quick Start

### 1. Start the System
```bash
bash start-system.sh
```
Or manually:
- **Terminal 1** (Backend): `python backend_python/app.py`
- **Terminal 2** (Frontend): `python server.py`

### 2. Access the System
Open in browser: **http://localhost:8888**

### 3. Login
```
Email: admin@company.com
Password: admin123
```

---

## 📋 Features Implemented

### 1. **Employee Management**
- ✅ View all employees
- ✅ Add new employees
- ✅ Edit employee details
- ✅ **Soft Delete** employees (moves to Archive, not permanently deleted)
- ✅ Archive/Restore deleted employees

### 2. **Password Change Log** (Admin Only)
**Table Shows:**
- User ID
- Action (Password changed, Created, etc.)
- Changed By (Admin name)
- Module (Where the change was made)
- Timestamp (When it happened)

**Features:**
- ✅ Automatic logging on password changes
- ✅ Full audit trail of who changed what and when
- ✅ Refresh button to reload logs

### 3. **Login Attempt Tracking** (Admin Only)
**Table Shows:**
- Email (User who attempted login)
- Attempts count
- Status (✓ OK / ⚠️ WARNING / 🔒 LOCKED)
- Last Attempt timestamp
- IP Address

**Security Features:**
- ✅ **Limit**: Maximum 5 attempts before cooldown
- ✅ **Warning**: At 3 attempts, warning shown to user
- ✅ **Cooldown**: 30-second automatic lockout after 5 attempts
- ✅ **Auto-unlock**: Lockout automatically removes after 30 seconds
- ✅ **Visual Feedback**: Users see attempt counter and remaining time

**Example Flow:**
1. Attempts 1-2: Normal error message
2. Attempt 3: ⚠️ "WARNING: 2 attempts remaining before 30-second cooldown"
3. Attempt 4: ⚠️ "WARNING: 1 attempt remaining before 30-second cooldown"
4. Attempt 5+: 🔒 "Account locked. Try again in 30 seconds"
5. After 30 seconds: Account automatically unlocked

### 4. **Deleted Employees Archive** (Admin Only)
**Table Shows:**
- Employee ID
- Full Name
- Email
- Department
- Position
- Deleted By (Admin who deleted them)
- Deleted At (When they were deleted)
- Actions (Restore / View)

**Features:**
- ✅ Soft delete (no data loss)
- ✅ One-click restore
- ✅ Full deletion history
- ✅ Can view archived employee details

### 5. **User Management** (Admin Only)
- ✅ View all system users
- ✅ Add new users
- ✅ Edit user roles (Admin/User)
- ✅ Manage user accounts

---

## 📊 Tables in Dashboard

### For All Users:
1. **Employees** - All active employees

### For Admin Only (auto-hidden for regular users):
1. **Users** - System user accounts
2. **Password Change Log** - Password audit trail
3. **Login Attempts Log** - Failed login tracking
4. **Deleted Employees Archive** - Soft-deleted employees

---

## 🔐 Database Schema

### password_logs table
```sql
- id (Primary Key)
- user_id (User who was affected)
- action (What changed: "Password changed", "Created", etc.)
- changed_by_id (Admin who made the change)
- changed_by_name (Name of admin)
- module (Where it happened: "Settings", "Admin Panel", etc.)
- timestamp (When it happened)
```

### login_attempts table
```sql
- id (Primary Key)
- user_id (User attempting login)
- email (User's email)
- attempt_count (Number of attempts)
- is_locked (Whether account is locked)
- last_attempt_time (When last attempt was)
- ip_address (IP that attempted login)
- locked_until (When lock expires)
```

### deleted_employees table
```sql
- id (Original employee ID)
- first_name, last_name
- email
- department, position
- salary, phone
- hire_date, address
- deleted_by_id (Admin ID)
- deleted_by_name (Admin name)
- deleted_at (When deleted)
```

---

## 🧪 Testing the Features

### Test Password Log:
1. Login as admin
2. Go to "Password Change Log" tab
3. Any password changes will appear with full details

### Test Login Attempts:
1. Go to login page
2. Try wrong password 1-2 times - normal errors
3. Try wrong password 3rd time - see warning
4. Try wrong password 4-5 times - get locked out
5. Wait 30 seconds - account auto-unlocks

### Test Soft Delete:
1. Login as admin
2. Click Delete on any employee
3. Employee moves to "Deleted Employees Archive"
4. Click Restore to bring them back
5. Employee returns to main Employees table

---

## 📈 API Endpoints (Backend)

All endpoints require authentication token.

### Employees
- `GET /api/employees` - List all employees
- `POST /api/employees` - Create employee
- `GET /api/employees/<id>` - Get single employee
- `PUT /api/employees/<id>` - Update employee
- `DELETE /api/employees/<id>` - Soft delete employee

### Password Logs
- `GET /api/password-logs` - Get all password logs
- `GET /api/password-logs/user/<id>` - Get logs for specific user

### Login Logs
- `GET /api/login-logs` - Get all login attempt logs
- `GET /api/login-logs/user/<id>` - Get logs for specific user

### Deleted Employees
- `GET /api/deleted-employees` - Get archived employees
- `POST /api/deleted-employees/<id>/restore` - Restore employee

---

## 🛠️ Troubleshooting

### "Failed to fetch" error
- Ensure both servers are running:
  - Backend on port 5002
  - Frontend on port 8888
- Check that localStorage has token (open diagnostic.html)

### No data showing
- Login first with admin@company.com / admin123
- Check browser console for errors (F12)
- Refresh the page

### Login attempt tracking not working
- Make sure you're testing failed logins (wrong password)
- Check login-log-container is visible (admin only)
- View "Login Attempts Log" table in dashboard

### Soft delete not working
- Make sure you're logged in as admin
- Click the Delete button on an employee
- Check "Deleted Employees Archive" table
- Click Restore to bring back

---

## 👨‍💼 Default Admin Account
```
Email: admin@company.com
Password: admin123
Role: Admin
```

---

## 📝 Features Summary

| Feature | Status | Type | Access |
|---------|--------|------|--------|
| Password Log | ✅ Complete | Audit Trail | Admin Only |
| Login Attempts | ✅ Complete | Security | Admin Only |
| Login Cooldown | ✅ Complete | Security | All Users |
| Soft Delete | ✅ Complete | Data Management | Admin Only |
| Employee Archive | ✅ Complete | Recovery | Admin Only |
| Restore Employee | ✅ Complete | Recovery | Admin Only |

---

**All features are fully implemented and tested!** 🎉
