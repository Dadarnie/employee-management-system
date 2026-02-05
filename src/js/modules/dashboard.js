/* ============================================
   DASHBOARD MODULE
   ============================================ */

class DashboardModule {
    constructor(db, employeeModule, userModule, logsModule) {
        this.db = db;
        this.employeeModule = employeeModule;
        this.userModule = userModule;
        this.logsModule = logsModule;
    }
    
    show() {
        const currentUser = this.db.getCurrentUser();
        
        if (!currentUser) {
            this.showAuth();
            return;
        }
        
        document.getElementById('auth-section').style.display = 'none';
        document.getElementById('dashboard-section').classList.add('active');
        
        document.getElementById('user-name').textContent = currentUser.name;
        
        this.employeeModule.loadEmployees();
        
        // Show admin-only tables
        if (currentUser.role === 'admin') {
            document.getElementById('users-table-container').classList.remove('hidden');
            document.getElementById('password-log-container').classList.remove('hidden');
            document.getElementById('login-log-container').classList.remove('hidden');
            document.getElementById('deleted-employees-container').classList.remove('hidden');
            
            this.userModule.loadUsers();
            this.logsModule.loadPasswordLogs();
            this.logsModule.loadLoginLogs();
            this.logsModule.loadDeletedEmployees();
        } else {
            document.getElementById('users-table-container').classList.add('hidden');
            document.getElementById('password-log-container').classList.add('hidden');
            document.getElementById('login-log-container').classList.add('hidden');
            document.getElementById('deleted-employees-container').classList.add('hidden');
        }
    }
    
    showAuth() {
        document.getElementById('auth-section').style.display = 'block';
        document.getElementById('dashboard-section').classList.remove('active');
        authModule.showSignIn();
    }
    
    logout() {
        if (confirm('Are you sure you want to logout?')) {
            this.db.clearCurrentUser();
            this.showAuth();
        }
    }
}
