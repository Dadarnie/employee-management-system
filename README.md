# Employee Management System

A professional, modular Employee Management System built with HTML, CSS, and JavaScript.

## Project Structure

```
project-root/
├── index.html                          # Main entry point
├── README.md                           # This file
│
└── src/                                # Source files
    ├── css/                            # Stylesheets
    │   ├── variables.css               # CSS custom properties and variables
    │   ├── main.css                    # Global styles
    │   ├── auth.css                    # Authentication page styles
    │   └── dashboard.css               # Dashboard and table styles
    │
    ├── js/                             # JavaScript files
    │   ├── app.js                      # Main application initialization
    │   │
    │   └── modules/                    # Modular JavaScript components
    │       ├── database.js             # LocalStorage database operations
    │       ├── auth.js                 # Authentication module
    │       ├── employees.js            # Employee management module
    │       ├── users.js                # User management module
    │       ├── dashboard.js            # Dashboard module
    │       └── utils.js                # Utility functions and helpers
    │
    └── html/                           # HTML components
        ├── auth.html                   # Authentication page component
        ├── dashboard.html              # Dashboard page component
        └── employee-modal.html         # Employee modal component
```

## File Descriptions

### CSS Files (`src/css/`)

- **variables.css** - Defines all CSS custom properties (colors, sizes, shadows, etc.)
- **main.css** - Global styles, typography, buttons, forms, animations
- **auth.css** - Authentication page specific styles
- **dashboard.css** - Dashboard, tables, modals, and responsive layouts

### JavaScript Files (`src/js/`)

#### Main Application
- **app.js** - Initializes all modules and handles DOMContentLoaded event

#### Modules (`src/js/modules/`)
- **database.js** - `Database` class for LocalStorage operations
- **auth.js** - `AuthModule` class for authentication handling
- **employees.js** - `EmployeeModule` class for employee CRUD operations
- **users.js** - `UserModule` class for user management
- **dashboard.js** - `DashboardModule` class for dashboard functionality
- **utils.js** - Utility functions accessible globally

### HTML Files (`src/html/`)

- **auth.html** - Authentication forms (Sign In, Sign Up, Forgot Password)
- **dashboard.html** - Dashboard layout with employee and user tables
- **employee-modal.html** - Modal for adding/editing employees

## Architecture

### Modular Design
Each feature is separated into its own module:
- Clear separation of concerns
- Easy to maintain and extend
- Reusable components

### Database
LocalStorage-based database with the following entities:
- **Users** - Authentication and account management
- **Employees** - Employee records with full details
- **Current User** - Session management

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
