# Project Structure Overview

## How Everything is Connected

### 1. **Entry Point: index.html**
   - Loads all CSS files with consistent styling
   - Loads all JavaScript modules in order
   - Contains all HTML sections inline (no fetch needed)

### 2. **CSS Files (Unified Styling)**
   ```
   main.css
   ├── All CSS variables (colors, sizes, shadows)
   ├── Global styles (body, animations, containers)
   ├── Form elements (inputs, labels, selects)
   ├── Buttons (all button styles)
   └── Utilities (alerts, spinners, responsive)
   
   auth.css
   ├── Authentication container
   ├── Auth tabs
   ├── Auth forms
   └── Auth-specific animations
   
   dashboard.css
   ├── Dashboard layout
   ├── Table styles
   ├── Modal styles
   └── Responsive design
   ```

### 3. **JavaScript Module Flow**

```
app.js (Main Entry)
    ↓
DOMContentLoaded Event
    ↓
├── database.js (Database class)
│   └── Manages all data operations
│
├── auth.js (AuthModule class)
│   ├── Handles sign in/sign up
│   ├── Manages authentication forms
│   └── Uses global functions from utils.js
│
├── employees.js (EmployeeModule class)
│   ├── Loads employees
│   ├── Opens/closes modal
│   ├── Edit/delete employees
│   └── Handles form submission
│
├── users.js (UserModule class)
│   ├── Loads users
│   └── Delete users
│
├── dashboard.js (DashboardModule class)
│   ├── Shows/hides sections
│   ├── Manages logout
│   └── Coordinates other modules
│
└── utils.js (Global Functions)
    ├── showAlert()
    ├── showModalAlert()
    ├── switchAuthTab()
    ├── showForgotPassword()
    ├── showSignIn()
    ├── showDashboard()
    ├── logout()
    ├── openEmployeeModal()
    ├── closeEmployeeModal()
    └── Modal click handlers
```

### 4. **Data Flow**

```
User Action (Click/Submit)
    ↓
Global Function (from utils.js / HTML onclick)
    ↓
Module Method
    ↓
Database Method
    ↓
LocalStorage
    ↓
Update UI
```

### 5. **CSS Cascade**

All elements inherit from the unified CSS variable system:

```
CSS Variables (main.css)
├── Colors: --primary-pink, --primary-lavender, etc.
├── Sizes: --radius-soft, --radius-medium, etc.
├── Shadows: --card-shadow
├── Gradients: --bg-gradient
└── Text colors: --text-primary, --text-secondary

Applied to:
├── auth.css - Auth page styling
├── dashboard.css - Dashboard styling
└── All HTML elements
```

### 6. **Key Connection Points**

**HTML → JavaScript:**
```html
<!-- From index.html -->
<button onclick="switchAuthTab('signin')">Sign In</button>
↓
<!-- Global function in utils.js -->
function switchAuthTab(tab) {
    authModule.switchAuthTab(tab);
}
```

**Module to Module:**
```javascript
// In app.js
dashboardModule = new DashboardModule(db, employeeModule, userModule);

// In dashboard.js
constructor(db, employeeModule, userModule) {
    this.employeeModule = employeeModule;
    this.userModule = userModule;
}
```

**Database Singleton:**
```javascript
// Created once in app.js
db = new Database();

// Shared across all modules
authModule = new AuthModule(db);
employeeModule = new EmployeeModule(db);
userModule = new UserModule(db);
dashboardModule = new DashboardModule(db, employeeModule, userModule);
```

## Testing the Connection

1. Open `index.html` in browser
2. All CSS should load and apply consistently
3. All JavaScript modules should initialize
4. Try signing up → dashboard should appear
5. Try adding an employee → modal should open with proper styling
6. All colors and animations should be consistent throughout

## Advantages of This Setup

✅ **Single Page Application** - No page reloads needed
✅ **Modular Code** - Each feature is independent
✅ **Consistent Styling** - All CSS uses same variables
✅ **Easy Maintenance** - Change variables in main.css to update entire app
✅ **Responsive** - Mobile-friendly design across all sections
✅ **No Build Required** - Works in any browser immediately
