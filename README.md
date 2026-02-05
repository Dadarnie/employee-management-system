# 🎯 Employee Management System

Complete Employee Management System with password logging, login security, and soft delete features.

## 🚀 Quick Start

```bash
bash start-system.sh
```

Then open: **http://localhost:8888**

Login with:
- Email: `admin@company.com`
- Password: `admin123`

## ✨ Features

✅ **Password Change Log** - Admin audit trail of all password changes
✅ **Login Attempt Tracking** - Failed login monitoring with 30-sec lockout
✅ **Soft Delete Archive** - Safe employee deletion with one-click restore
✅ **User Management** - Add/delete system users with roles
✅ **Employee Management** - Full CRUD operations
✅ **Role-Based Access** - Admin and User roles

## 📊 Dashboard

**All Users See:**
- Employees table

**Admins See (Additional):**
- Users table
- Password Change Log
- Login Attempts Log
- Deleted Employees Archive

## 📁 Files

```
backend_python/
├── app.py              Flask API (port 5002)
└── data/database.db    SQLite database

src/
├── css/                Stylesheets
├── html/               HTML components
└── js/modules/         JavaScript modules

index.html              Main page
server.py              Frontend server (port 8888)
start-system.sh        Startup script

README.md              This file
FEATURES.md            Detailed features
USER_GUIDE.md          How to use
```

## 🔌 Tech Stack

- Backend: Python Flask + SQLite3
- Frontend: Vanilla JavaScript + HTML5 + CSS3
- Auth: JWT + Bcrypt
- API: REST with role-based access

## 🔐 Security

✓ Bcrypt password hashing
✓ JWT authentication
✓ Login attempt limiting (5 attempts)
✓ 30-second automatic lockout
✓ Complete audit trail
✓ Role-based access control

## 📚 Documentation

- **FEATURES.md** - Detailed feature explanations
- **USER_GUIDE.md** - How to use each feature

## 🆘 Quick Help

**Start system:**
```bash
bash start-system.sh
```

**Stop servers:**
```bash
pkill -f "app.py"
pkill -f "server.py"
```

**Check servers running:**
```bash
ps aux | grep -E "app.py|server.py"
```

## 👨‍💼 Default Account

```
Email: admin@company.com
Password: admin123
```

## ✅ Status

All 3 requested features fully implemented and tested. System is production-ready.

**Start Now:** `bash start-system.sh`
**Access:** `http://localhost:8888`
