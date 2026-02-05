# 🎯 What You See When You Use The System

## Login Screen
You'll see a clean login interface with:
- Email field
- Password field
- "Sign In" button
- Sign Up tab for new accounts
- Forgot Password option

**Login with:**
```
Email: admin@company.com
Password: admin123
```

---

## Dashboard - After Login

### For All Users:
You see the **Employees** table with columns:
```
ID | Name | Email | Department | Position | Salary | Actions (Edit/Delete)
```

### For Admins (automatically shows 5 tables):

#### 1️⃣ **Employees Table** (Top)
Shows all active employees. You can:
- ➕ Add new employee (button at top)
- Edit employee (click Edit button)
- Delete employee (click Delete button - moves to archive)

#### 2️⃣ **Users Table** (Middle)
Shows system user accounts. Admin-only. Columns:
```
ID | Name | Email | Role | Created | Actions
```

#### 3️⃣ **Password Change Log** (Middle)
Shows every password change that happened. Columns:
```
User ID | Action (Password changed/Created) | Changed By (Admin name) | Module (Where) | Timestamp (When)
```

Example rows:
```
1 | Password changed | Admin User | User Settings | 2026-02-05 14:30:00
2 | Created | Admin User | Admin Panel | 2026-02-03 10:15:00
```

Has a **🔄 Refresh** button to reload.

#### 4️⃣ **Login Attempts Log** (Bottom)
Shows failed login attempts and account locks. Columns:
```
Email | Attempts | Status | Last Attempt | IP Address
```

Status badges:
- ✓ OK (green) - No failed attempts
- ⚠️ WARNING (yellow) - 3+ attempts, cooldown soon
- 🔒 LOCKED (red) - Account is locked for 30 seconds

Example rows:
```
john.smith@company.com | 0 | ✓ OK | 2026-02-05 14:20:00 | 192.168.1.1
jane.doe@company.com | 3 | ⚠️ WARNING | 2026-02-05 14:25:00 | 192.168.1.2
```

Has a **🔄 Refresh** button.

#### 5️⃣ **Deleted Employees Archive** (Bottom)
Shows employees who were soft-deleted. Columns:
```
ID | Name | Email | Department | Position | Deleted By | Deleted At | Actions (Restore/View)
```

Example row:
```
7 | Robert Johnson | robert.johnson@company.com | Sales | Sales Manager | Admin User | 2026-02-05 14:30:00 | [↩️ Restore] [👁️ View]
```

You can:
- **↩️ Restore** - Brings employee back to main table
- **👁️ View** - See full details of deleted employee

---

## User Login Attempt Tracking

### What the User Sees:

#### **Attempt 1-2 (Failed):**
```
❌ Invalid credentials. Please try again.
```

#### **Attempt 3 (Warning):**
```
❌ Invalid credentials.
⚠️ WARNING: 2 attempts remaining before 30-second cooldown!
```

#### **Attempt 4 (Warning):**
```
❌ Invalid credentials.
⚠️ WARNING: 1 attempt remaining before 30-second cooldown!
```

#### **Attempt 5+ (Locked):**
```
🔒 Your account is locked due to multiple failed login attempts.
Please try again in 30 seconds.

[Form inputs are disabled]
[Countdown timer: 00:30]
```

**After 30 seconds:**
```
✓ Account unlocked. You can try again now.
```

---

## Employee Delete/Restore Example

### **Deleting an Employee:**
1. Find employee "John Smith" in Employees table
2. Click **Delete** button
3. **Pop-up confirms:** "Are you sure you want to delete this employee?"
4. Click **Yes**
5. John Smith disappears from Employees table
6. Success message: ✓ Employee deleted successfully

### **Finding in Archive:**
1. Scroll down to **"🗑️ Deleted Employees Archive"** table
2. Find "John Smith" in the list
3. See "Deleted by: Admin User" and "Deleted at: 2026-02-05 14:30:00"

### **Restoring an Employee:**
1. Click **↩️ Restore** button next to John Smith
2. **Pop-up confirms:** "Are you sure you want to restore this employee?"
3. Click **Yes**
4. Success message: ✓ Employee restored successfully
5. John Smith reappears in Employees table
6. John Smith disappears from Archive

---

## Real-World Usage Scenarios

### Scenario 1: Audit Trail
**Situation:** You need to know who changed a user's password and when.

**What you do:**
1. Login as admin
2. Scroll to **"🔑 Password Change Log"** table
3. Find the row for that user
4. See: "Changed By: Admin User" and exact timestamp
5. Know exactly what changed and when

### Scenario 2: Security Investigation
**Situation:** Multiple failed login attempts detected. Need to investigate.

**What you do:**
1. Login as admin
2. Scroll to **"📝 Login Attempts Log"** table
3. Find the user's email
4. See: attempt count, status (locked if > 5), last attempt time, IP address
5. Can identify suspicious activity

### Scenario 3: Employee Accidentally Deleted
**Situation:** You accidentally deleted an employee, need to restore them.

**What you do:**
1. Login as admin
2. Scroll to **"🗑️ Deleted Employees Archive"** table
3. Find the employee you deleted
4. Click **↩️ Restore**
5. Employee is back in the system with all data intact
6. Zero data loss

### Scenario 4: Monthly Audit Report
**Situation:** Need to show all password changes for compliance.

**What you do:**
1. Login as admin
2. Go to **"🔑 Password Change Log"** table
3. Click **🔄 Refresh** to get latest data
4. See all password changes with: who changed it, when, and what system part
5. Export/screenshot for audit purposes

---

## Mobile Responsive?
The system is fully responsive and works on:
- ✅ Desktop (1920x1080, 1440x900, etc.)
- ✅ Tablet (iPad, etc.)
- ✅ Mobile (when viewed on mobile browser)

---

## How the System Knows Your Role

When you login:
1. System checks if you're an admin or regular user
2. Admin tables (Password Log, Login Log, Archive) automatically **hide** for regular users
3. Only Employees table shows for regular users
4. Admin users see **all 5 tables**

No manual configuration needed - it's automatic!

---

## Summary

**The system provides:**
- 📋 Employee management with full CRUD operations
- 🗑️ Safe deletion with recovery (soft delete)
- 🔑 Complete password change audit trail
- 🔐 Failed login tracking and security lockout
- ⚠️ Automatic warnings at 3 attempts
- 🔒 30-second cooldown after 5 attempts
- ✓ One-click employee restore from archive

**All fully visual, user-friendly, and secure!** ✨
