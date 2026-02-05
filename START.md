# 🚀 HOW TO START

## Step 1: Start the Backend Server

Open a terminal and run:

```bash
cd /home/darnie/Downloads/ACT#1-LAIT
python backend_python/app.py
```

**Expected Output:**
```
🔧 Initializing database...
✓ Database ready
✓ Server running on http://localhost:5002
✓ CORS enabled for: http://localhost:8888
Press Ctrl+C to stop
```

⚠️ **IMPORTANT: Keep this terminal open!**

---

## Step 2: Open Frontend in Browser

Open a new browser tab and go to:

```
http://localhost:8888
```

---

## Step 3: Login

Use these credentials:

```
Email:    admin@company.com
Password: admin123
```

---

## ✅ You're In!

Once logged in, you'll see:

- **👥 Employees Table** - Manage employees
- **🔐 Users Table** - View users (admin only)
- **🔑 Password Change Log** - Track password changes (admin only)
- **📝 Login Attempts Log** - Monitor login attempts (admin only)
- **🗑️ Deleted Employees Archive** - Restore deleted employees (admin only)

---

## 🧪 Quick Test

Try these features:

1. **Test Login Lockout**: Logout and try logging in 5 times with wrong password
   - At 3 attempts: See ⚠️ warning
   - At 5 attempts: See 🔒 locked message for 30 seconds

2. **Test Soft Delete**: Delete an employee and restore it from archive

3. **Test Admin-Only Access**: Log out and create a regular user, then login as that user
   - You'll only see the Employees table
   - Other tables will be hidden

---

## ❌ If It Doesn't Work

### Backend won't start?
```bash
# Check if Python is installed
python --version

# Install dependencies
pip install flask flask-cors werkzeug pyjwt
```

### Port already in use?
```bash
# Try port 5002
python backend_python/app.py
```

### Still getting connection error?
- Make sure backend terminal is still running (don't close it)
- Try refreshing browser: Ctrl+F5 (hard refresh)
- Check browser console for errors: F12 → Console tab

---

## 📁 Important Files

- `backend_python/app.py` - Backend server (runs on port 5002)
- `index.html` - Frontend home (open in browser)
- `src/js/modules/logs.js` - Password/login logs module
- `backend_python/data/database.db` - SQLite database (auto-created)

---

**Status:** ✅ Ready to use
**Backend Port:** 5002
**Frontend Port:** 8888
**Admin Email:** admin@company.com
**Admin Password:** admin123

