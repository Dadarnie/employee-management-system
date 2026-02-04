/* ============================================
   MAIN APPLICATION FILE
   ============================================ */

// Initialize modules
let db;
let authModule;
let employeeModule;
let userModule;
let dashboardModule;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize database
    db = new Database();
    
    // Initialize modules
    authModule = new AuthModule(db);
    employeeModule = new EmployeeModule(db);
    userModule = new UserModule(db);
    dashboardModule = new DashboardModule(db, employeeModule, userModule);
    
    // Check if user is logged in
    const currentUser = db.getCurrentUser();
    
    if (currentUser) {
        dashboardModule.show();
    } else {
        dashboardModule.showAuth();
    }
});
