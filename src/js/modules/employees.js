/* ============================================
   EMPLOYEE MANAGEMENT MODULE
   ============================================ */

class EmployeeModule {
    constructor(db) {
        this.db = db;
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        const employeeForm = document.getElementById('employee-form');
        if (employeeForm) {
            employeeForm.addEventListener('submit', (e) => this.handleFormSubmit(e));
        }
    }
    
    loadEmployees() {
        this.db.getEmployees()
            .then(employees => {
                const tbody = document.getElementById('employees-tbody');
                tbody.innerHTML = '';
                
                if (!Array.isArray(employees)) {
                    console.error('Expected array but got:', employees);
                    return;
                }
                
                employees.forEach(emp => {
                    const tr = document.createElement('tr');
                    tr.innerHTML = `
                        <td>${emp.id}</td>
                        <td>${emp.first_name} ${emp.last_name}</td>
                        <td>${emp.email}</td>
                        <td>${emp.department || 'N/A'}</td>
                        <td>${emp.position || 'N/A'}</td>
                        <td>$${Number(emp.salary || 0).toLocaleString()}</td>
                        <td class="action-buttons">
                            <button class="btn-edit" onclick="employeeModule.editEmployee(${emp.id})">Edit</button>
                            <button class="btn-delete" onclick="employeeModule.deleteEmployee(${emp.id})">Delete</button>
                        </td>
                    `;
                    tbody.appendChild(tr);
                });
            })
            .catch(error => {
                console.error('Error loading employees:', error);
                showAlert('error', 'Failed to load employees');
            });
    }
    
    openModal(employeeId = null) {
        const modal = document.getElementById('employee-modal');
        const form = document.getElementById('employee-form');
        const title = document.getElementById('employee-modal-title');
        
        form.reset();
        document.getElementById('employee-id').value = '';
        this.clearModalAlerts();
        
        if (employeeId) {
            // Fetch employees asynchronously
            this.db.getEmployees()
                .then(employees => {
                    const emp = employees.find(e => e.id === employeeId);
                    
                    if (emp) {
                        title.textContent = 'Edit Employee';
                        document.getElementById('employee-id').value = emp.id;
                        document.getElementById('emp-firstname').value = emp.first_name || '';
                        document.getElementById('emp-lastname').value = emp.last_name || '';
                        document.getElementById('emp-email').value = emp.email;
                        document.getElementById('emp-phone').value = emp.phone || '';
                        document.getElementById('emp-department').value = emp.department || '';
                        document.getElementById('emp-position').value = emp.position || '';
                        document.getElementById('emp-hiredate').value = emp.hire_date || '';
                        document.getElementById('emp-salary').value = emp.salary || '';
                        document.getElementById('emp-address').value = emp.address || '';
                    }
                })
                .catch(error => {
                    console.error('Error loading employee:', error);
                    showAlert('error', 'Failed to load employee');
                });
        } else {
            title.textContent = 'Add Employee';
        }
        
        modal.classList.add('active');
    }
    
    closeModal() {
        document.getElementById('employee-modal').classList.remove('active');
        document.getElementById('employee-form').reset();
        this.clearModalAlerts();
    }
    
    editEmployee(id) {
        this.openModal(id);
    }
    
    deleteEmployee(id) {
        if (confirm('Are you sure you want to delete this employee?')) {
            this.db.deleteEmployee(id)
                .then(() => {
                    this.loadEmployees();
                    showAlert('success', 'Employee deleted successfully!');
                })
                .catch(error => {
                    console.error('Error deleting employee:', error);
                    showAlert('error', 'Failed to delete employee');
                });
        }
    }
    
    handleFormSubmit(e) {
        e.preventDefault();
        
        const employeeData = {
            first_name: document.getElementById('emp-firstname').value,
            last_name: document.getElementById('emp-lastname').value,
            email: document.getElementById('emp-email').value,
            phone: document.getElementById('emp-phone').value,
            department: document.getElementById('emp-department').value,
            position: document.getElementById('emp-position').value,
            hire_date: document.getElementById('emp-hiredate').value,
            salary: parseFloat(document.getElementById('emp-salary').value) || 0,
            address: document.getElementById('emp-address').value
        };
        
        const employeeId = document.getElementById('employee-id').value;
        
        if (employeeId) {
            // Update employee
            this.db.updateEmployee(parseInt(employeeId), employeeData)
                .then(() => {
                    showModalAlert('success', 'Employee updated successfully!');
                    this.loadEmployees();
                    setTimeout(() => {
                        this.closeModal();
                    }, 1500);
                })
                .catch(error => {
                    showModalAlert('error', error.message || 'Failed to update employee');
                });
        } else {
            // Create new employee
            this.db.createEmployee(employeeData)
                .then(() => {
                    showModalAlert('success', 'Employee added successfully!');
                    this.loadEmployees();
                    setTimeout(() => {
                        this.closeModal();
                    }, 1500);
                })
                .catch(error => {
                    showModalAlert('error', error.message || 'Failed to create employee');
                });
        }
    }
    
    clearModalAlerts() {
        document.getElementById('modal-alert-container').innerHTML = '';
    }
}
