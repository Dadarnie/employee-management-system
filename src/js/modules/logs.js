/* ============================================
   LOGS MODULE
   Handles password logs, login logs, and deleted employees
   ============================================ */

class LogsModule {
    constructor(db) {
        this.db = db;
    }
    
    /**
     * Load password change logs
     */
    async loadPasswordLogs() {
        try {
            const logs = await this.db.getPasswordLogs();
            this.displayPasswordLogs(logs);
        } catch (error) {
            console.error('Error loading password logs:', error);
            showAlert('error', 'Failed to load password logs');
        }
    }
    
    /**
     * Display password logs in table
     */
    displayPasswordLogs(logs) {
        const tbody = document.getElementById('password-log-tbody');
        tbody.innerHTML = '';
        
        if (!logs || logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No password logs found</td></tr>';
            return;
        }
        
        logs.forEach(log => {
            const timestamp = new Date(log.timestamp).toLocaleString();
            const row = `
                <tr>
                    <td>${log.user_id}</td>
                    <td><span class="badge badge-info">${log.action}</span></td>
                    <td>${log.changed_by_name || 'System'}</td>
                    <td>${log.module || 'N/A'}</td>
                    <td>${timestamp}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }
    
    /**
     * Load login attempt logs
     */
    async loadLoginLogs() {
        try {
            const logs = await this.db.getLoginLogs();
            this.displayLoginLogs(logs);
        } catch (error) {
            console.error('Error loading login logs:', error);
            showAlert('error', 'Failed to load login logs');
        }
    }
    
    /**
     * Display login logs in table
     */
    displayLoginLogs(logs) {
        const tbody = document.getElementById('login-log-tbody');
        tbody.innerHTML = '';
        
        if (!logs || logs.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center">No login attempts found</td></tr>';
            return;
        }
        
        logs.forEach(log => {
            const lastAttempt = new Date(log.last_attempt_time).toLocaleString();
            
            let statusBadge = '';
            if (log.is_locked) {
                statusBadge = '<span class="badge badge-danger">🔒 LOCKED</span>';
            } else if (log.attempt_count >= 3) {
                statusBadge = '<span class="badge badge-warning">⚠️ WARNING</span>';
            } else if (log.attempt_count === 0) {
                statusBadge = '<span class="badge badge-success">✓ OK</span>';
            } else {
                statusBadge = '<span class="badge badge-warning">⚠️ FAILED</span>';
            }
            
            const row = `
                <tr>
                    <td>${log.email}</td>
                    <td>${log.attempt_count}</td>
                    <td>${statusBadge}</td>
                    <td>${lastAttempt}</td>
                    <td>${log.ip_address || 'N/A'}</td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }
    
    /**
     * Load deleted employees
     */
    async loadDeletedEmployees() {
        try {
            const employees = await this.db.getDeletedEmployees();
            this.displayDeletedEmployees(employees);
        } catch (error) {
            console.error('Error loading deleted employees:', error);
            showAlert('error', 'Failed to load deleted employees');
        }
    }
    
    /**
     * Display deleted employees in table
     */
    displayDeletedEmployees(employees) {
        const tbody = document.getElementById('deleted-employees-tbody');
        tbody.innerHTML = '';
        
        if (!employees || employees.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center">No deleted employees</td></tr>';
            return;
        }
        
        employees.forEach(emp => {
            const deletedDate = new Date(emp.deleted_at).toLocaleString();
            const row = `
                <tr>
                    <td>${emp.id}</td>
                    <td>${emp.first_name} ${emp.last_name}</td>
                    <td>${emp.email}</td>
                    <td>${emp.department || 'N/A'}</td>
                    <td>${emp.position || 'N/A'}</td>
                    <td>${emp.deleted_by_name}</td>
                    <td>${deletedDate}</td>
                    <td>
                        <button class="btn btn-small btn-success" onclick="restoreEmployee(${emp.id})">
                            ↩️ Restore
                        </button>
                        <button class="btn btn-small btn-info" onclick="viewDeletedEmployee(${emp.id})">
                            👁️ View
                        </button>
                    </td>
                </tr>
            `;
            tbody.innerHTML += row;
        });
    }
}

/**
 * Refresh password logs
 */
async function refreshPasswordLogs() {
    if (logsModule) {
        await logsModule.loadPasswordLogs();
        showAlert('success', 'Password logs refreshed');
    }
}

/**
 * Refresh login logs
 */
async function refreshLoginLogs() {
    if (logsModule) {
        await logsModule.loadLoginLogs();
        showAlert('success', 'Login logs refreshed');
    }
}

/**
 * Refresh deleted employees
 */
async function refreshDeletedEmployees() {
    if (logsModule) {
        await logsModule.loadDeletedEmployees();
        showAlert('success', 'Deleted employees list refreshed');
    }
}

/**
 * Restore deleted employee
 */
async function restoreEmployee(empId) {
    if (!confirm('Are you sure you want to restore this employee?')) {
        return;
    }
    
    try {
        await db.restoreEmployee(empId);
        showAlert('success', 'Employee restored successfully');
        logsModule.loadDeletedEmployees();
        employeeModule.loadEmployees();
    } catch (error) {
        showAlert('error', error.message || 'Failed to restore employee');
    }
}

/**
 * View deleted employee details
 */
function viewDeletedEmployee(empId) {
    // This would open a modal with the deleted employee's details
    // For now, we'll show an alert with basic info
    alert('View deleted employee details - Feature to be implemented');
}
