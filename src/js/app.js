/* ============================================
   MAIN APPLICATION FILE
   ============================================ */

// Initialize modules
let db;
let authModule;
let employeeModule;
let userModule;
let logsModule;
let dashboardModule;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize database
    db = new Database();
    
    // Initialize modules
    authModule = new AuthModule(db);
    employeeModule = new EmployeeModule(db);
    userModule = new UserModule(db);
    logsModule = new LogsModule(db);
    dashboardModule = new DashboardModule(db, employeeModule, userModule, logsModule);
    
    // Check if user is logged in
    const currentUser = db.getCurrentUser();
    
    if (currentUser) {
        dashboardModule.show();
    } else {
        dashboardModule.showAuth();
    }
});
