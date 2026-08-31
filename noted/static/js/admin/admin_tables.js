/* ======================= */
/* REUSABLE ADMIN TABLE JS */
/* ======================= */

class AdminTable {
    constructor(tableId, config) {
        this.tableId = tableId;
        this.config = config;
        this.currentPage = 1;
        this.currentPerPage = 25;
        this.currentSearch = '';
        this.currentFilter = 'all';
        this.currentSort = { column: null, direction: 'asc' };
        this.data = [];
        this.totalCount = 0;
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.loadData();
    }
    
    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById(`${this.tableId}-search`);
        if (searchInput) {
            let searchTimeout;
            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.currentSearch = e.target.value;
                    this.currentPage = 1;
                    this.loadData();
                }, 300);
            });
        }
        
        // Filter functionality
        const filterSelect = document.getElementById(`${this.tableId}-filter`);
        if (filterSelect) {
            filterSelect.addEventListener('change', (e) => {
                this.currentFilter = e.target.value;
                this.currentPage = 1;
                this.loadData();
            });
        }
        
        // Entries per page
        const entriesSelect = document.getElementById(`${this.tableId}-entries`);
        if (entriesSelect) {
            entriesSelect.addEventListener('change', (e) => {
                this.currentPerPage = parseInt(e.target.value);
                this.currentPage = 1;
                this.loadData();
            });
        }
        
        // Column sorting
        const headers = document.querySelectorAll(`#${this.tableId} th.sortable`);
        headers.forEach(header => {
            header.addEventListener('click', () => {
                const column = header.dataset.column;
                if (this.currentSort.column === column) {
                    this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
                } else {
                    this.currentSort.column = column;
                    this.currentSort.direction = 'asc';
                }
                this.updateSortIndicators();
                this.loadData();
            });
        });
    }
    
    updateSortIndicators() {
        // Remove all sort classes
        const headers = document.querySelectorAll(`#${this.tableId} th`);
        headers.forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });
        
        // Add sort class to current column
        if (this.currentSort.column) {
            const currentHeader = document.querySelector(`#${this.tableId} th[data-column="${this.currentSort.column}"]`);
            if (currentHeader) {
                currentHeader.classList.add(`sort-${this.currentSort.direction}`);
            }
        }
    }
    
    async loadData() {
        this.showLoading();
        
        try {
            const params = new URLSearchParams({
                page: this.currentPage,
                per_page: this.currentPerPage,
                search: this.currentSearch,
                filter: this.currentFilter,
                sort_column: this.currentSort.column || '',
                sort_direction: this.currentSort.direction
            });
            
            const response = await fetch(`${this.config.apiEndpoint}?${params}`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                this.data = result.data;
                this.totalCount = result.total;
                this.renderTable();
                this.updatePagination();
                this.updateInfo();
            } else {
                throw new Error(result.message || 'Failed to load data');
            }
        } catch (error) {
            console.error('Error loading table data:', error);
            this.showError(error.message);
        } finally {
            this.hideLoading();
        }
    }
    
    showLoading() {
        const loading = document.getElementById(`${this.tableId}-loading`);
        const table = document.querySelector(`#${this.tableId} .table-wrapper`);
        if (loading) loading.style.display = 'block';
        if (table) table.style.opacity = '0.5';
    }
    
    hideLoading() {
        const loading = document.getElementById(`${this.tableId}-loading`);
        const table = document.querySelector(`#${this.tableId} .table-wrapper`);
        if (loading) loading.style.display = 'none';
        if (table) table.style.opacity = '1';
    }
    
    showError(message) {
        const tbody = document.getElementById(`${this.tableId}-tbody`);
        if (tbody) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="${this.config.columns.length + (this.config.actions ? 1 : 0)}" class="text-center" style="padding: 3rem; color: #dc3545;">
                        <strong>Error:</strong> ${message}
                    </td>
                </tr>
            `;
        }
    }
    
    renderTable() {
        const tbody = document.getElementById(`${this.tableId}-tbody`);
        if (!tbody) return;
        
        if (this.data.length === 0) {
            const noData = tbody.querySelector('.no-data');
            if (noData) {
                noData.style.display = 'table-row';
            }
            tbody.innerHTML = tbody.querySelector('.no-data')?.outerHTML || '';
            return;
        }
        
        const rows = this.data.map(row => this.renderRow(row)).join('');
        tbody.innerHTML = rows;
    }
    
    renderRow(row) {
        const cells = this.config.columns.map(column => {
            let value = this.getNestedValue(row, column.key);
            
            // Apply formatting if specified
            if (column.format) {
                value = this.formatValue(value, column.format, row);
            }
            
            return `<td${column.class ? ` class="${column.class}"` : ''}>${value}</td>`;
        }).join('');
        
        let actionCell = '';
        if (this.config.actions) {
            actionCell = `<td class="actions-column">${this.renderActions(row)}</td>`;
        }
        
        return `<tr data-id="${row.id || row[this.config.primaryKey || 'id']}">${cells}${actionCell}</tr>`;
    }
    
    renderActions(row) {
        if (!this.config.actions) return '';
        
        const actions = this.config.actions.map(action => {
            const id = row.id || row[this.config.primaryKey || 'id'];
            
            if (action.type === 'link') {
                return `<a href="${action.url.replace(':id', id)}" class="action-btn ${action.class || ''}" title="${action.label}">
                    ${action.label}
                </a>`;
            } else {
                return `<button onclick="handleTableAction('${this.tableId}', '${action.key}', '${id}')" 
                               class="action-btn ${action.class || ''}" 
                               title="${action.label}">
                    ${action.label}
                </button>`;
            }
        });
        
        return `<div class="table-actions">${actions.join('')}</div>`;
    }
    
    getNestedValue(obj, path) {
        return path.split('.').reduce((current, key) => current && current[key], obj) || '';
    }
    
    formatValue(value, format, row) {
        switch (format) {
            case 'date':
                return value ? new Date(value).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric'
                }) : '';
            
            case 'datetime':
                return value ? new Date(value).toLocaleString('en-US', {
                    year: 'numeric',
                    month: 'short',
                    day: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                }) : '';
            
            case 'currency':
                return value ? `$${parseFloat(value).toFixed(2)}` : '$0.00';
            
            case 'status':
                return value ? `<span class="status-badge status-${value.toLowerCase()}">${value}</span>` : '';
            
            case 'boolean':
                return value ? 
                    '<span class="status-badge status-active">Yes</span>' : 
                    '<span class="status-badge status-inactive">No</span>';
            
            case 'role':
                if (value == 1) {
                    return '<span class="status-badge status-active">Admin</span>';
                } else {
                    return '<span class="status-badge status-pending">Customer</span>';
                }
            
            case 'stock':
                const quantity = parseInt(value) || 0;
                let stockClass = 'status-good';
                let stockText = 'In Stock';
                
                if (quantity === 0) {
                    stockClass = 'status-out';
                    stockText = 'Out of Stock';
                } else if (quantity <= 10) {
                    stockClass = 'status-low';
                    stockText = 'Low Stock';
                }
                
                return `<span class="stock-badge ${stockClass}" title="${stockText}">${quantity}</span>`;
            
            case 'custom':
                // Custom formatting function should be provided in column config
                return typeof this.config.customFormatters?.[format] === 'function' 
                    ? this.config.customFormatters[format](value, row) 
                    : value;
            
            default:
                return value;
        }
    }
    
    updatePagination() {
        const totalPages = Math.ceil(this.totalCount / this.currentPerPage);
        
        // Update previous/next buttons
        const prevBtn = document.getElementById(`${this.tableId}-prev`);
        const nextBtn = document.getElementById(`${this.tableId}-next`);
        
        if (prevBtn) {
            prevBtn.disabled = this.currentPage <= 1;
        }
        
        if (nextBtn) {
            nextBtn.disabled = this.currentPage >= totalPages;
        }
        
        // Update page numbers
        const paginationNumbers = document.getElementById(`${this.tableId}-pagination-numbers`);
        if (paginationNumbers) {
            paginationNumbers.innerHTML = this.generatePageNumbers(totalPages);
        }
    }
    
    generatePageNumbers(totalPages) {
        if (totalPages <= 1) return '';
        
        const pages = [];
        const currentPage = this.currentPage;
        
        // Always show first page
        pages.push(1);
        
        // Calculate range around current page
        const rangeStart = Math.max(2, currentPage - 2);
        const rangeEnd = Math.min(totalPages - 1, currentPage + 2);
        
        // Add ellipsis if there's a gap
        if (rangeStart > 2) {
            pages.push('...');
        }
        
        // Add pages around current page
        for (let i = rangeStart; i <= rangeEnd; i++) {
            if (i !== 1 && i !== totalPages) {
                pages.push(i);
            }
        }
        
        // Add ellipsis if there's a gap
        if (rangeEnd < totalPages - 1) {
            pages.push('...');
        }
        
        // Always show last page
        if (totalPages > 1) {
            pages.push(totalPages);
        }
        
        return pages.map(page => {
            if (page === '...') {
                return '<span class="pagination-ellipsis">...</span>';
            }
            
            const isActive = page === currentPage ? 'active' : '';
            return `<button class="pagination-number ${isActive}" onclick="goToPage('${this.tableId}', ${page})">${page}</button>`;
        }).join('');
    }
    
    updateInfo() {
        const info = document.getElementById(`${this.tableId}-info`);
        if (info) {
            const start = (this.currentPage - 1) * this.currentPerPage + 1;
            const end = Math.min(this.currentPage * this.currentPerPage, this.totalCount);
            info.textContent = `Showing ${start} to ${end} of ${this.totalCount} entries`;
        }
    }
    
    refresh() {
        this.loadData();
    }
    
    goToPage(page) {
        this.currentPage = page;
        this.loadData();
    }
    
    changePage(direction) {
        if (direction === 'prev' && this.currentPage > 1) {
            this.currentPage--;
        } else if (direction === 'next') {
            const totalPages = Math.ceil(this.totalCount / this.currentPerPage);
            if (this.currentPage < totalPages) {
                this.currentPage++;
            }
        }
        this.loadData();
    }
}

// Global table instances
const adminTables = {};

// Initialize table
function initializeTable(tableId, config) {
    adminTables[tableId] = new AdminTable(tableId, config);
}

// Global functions for table interactions
function refreshTable(tableId) {
    if (adminTables[tableId]) {
        adminTables[tableId].refresh();
    }
}

function goToPage(tableId, page) {
    if (adminTables[tableId]) {
        adminTables[tableId].goToPage(page);
    }
}

function changePage(tableId, direction) {
    if (adminTables[tableId]) {
        adminTables[tableId].changePage(direction);
    }
}

// Handle table actions (edit, delete, etc.)
function handleTableAction(tableId, action, itemId) {
    const table = adminTables[tableId];
    if (!table) return;
    
    const config = table.config;
    const actionConfig = config.actions?.find(a => a.key === action);
    
    if (!actionConfig) return;
    
    switch (action) {
        case 'edit':
            if (actionConfig.handler) {
                actionConfig.handler(itemId);
            } else {
                openEditModal(tableId, itemId);
            }
            break;
            
        case 'view':
            if (actionConfig.handler) {
                actionConfig.handler(itemId);
            } else {
                openViewModal(tableId, itemId);
            }
            break;
            
        case 'delete':
            if (actionConfig.handler) {
                actionConfig.handler(itemId);
            } else {
                openDeleteModal(tableId, itemId);
            }
            break;
            
        case 'stock':
            if (actionConfig.handler) {
                actionConfig.handler(itemId);
            } else {
                openProductStockModal(itemId);
            }
            break;
            
        default:
            if (actionConfig.handler) {
                actionConfig.handler(itemId);
            }
    }
}

// Enhanced modal functions
function openEditModal(tableId, itemId) {
    const table = adminTables[tableId];
    if (!table) return;
    
    const modal = document.getElementById(`${tableId}-edit-modal`);
    const loadingEl = modal.querySelector('.form-loading');
    const contentEl = modal.querySelector('.form-content');
    const saveBtn = document.getElementById(`${tableId}-edit-save`);
    
    if (!modal) return;
    
    // Show modal and loading state
    modal.style.display = 'flex';
    loadingEl.style.display = 'block';
    contentEl.innerHTML = '';
    
    // Fetch item data
    fetch(`${table.config.apiEndpoint.replace('/table/', '/')}/${itemId}`)
        .then(response => response.json())
        .then(result => {
            loadingEl.style.display = 'none';
            
            if (result.success || result.data) {
                const data = result.data || result;
                contentEl.innerHTML = generateEditForm(tableId, data);
                
                // Setup save handler
                saveBtn.onclick = () => saveItem(tableId, itemId);
            } else {
                contentEl.innerHTML = '<p class="text-danger">Failed to load data</p>';
            }
        })
        .catch(error => {
            console.error('Error loading item:', error);
            loadingEl.style.display = 'none';
            contentEl.innerHTML = '<p class="text-danger">Error loading data</p>';
        });
}

function openViewModal(tableId, itemId) {
    const table = adminTables[tableId];
    if (!table) return;
    
    const modal = document.getElementById(`${tableId}-view-modal`);
    const loadingEl = modal.querySelector('.view-loading');
    const contentEl = modal.querySelector('.view-content');
    
    if (!modal) return;
    
    // Show modal and loading state
    modal.style.display = 'flex';
    loadingEl.style.display = 'block';
    contentEl.innerHTML = '';
    
    // Fetch item data
    fetch(`${table.config.apiEndpoint.replace('/table/', '/')}/${itemId}`)
        .then(response => response.json())
        .then(result => {
            loadingEl.style.display = 'none';
            
            if (result.success || result.data) {
                const data = result.data || result;
                contentEl.innerHTML = generateViewContent(tableId, data);
            } else {
                contentEl.innerHTML = '<p class="text-danger">Failed to load data</p>';
            }
        })
        .catch(error => {
            console.error('Error loading item:', error);
            loadingEl.style.display = 'none';
            contentEl.innerHTML = '<p class="text-danger">Error loading data</p>';
        });
}

function openDeleteModal(tableId, itemId) {
    const modal = document.getElementById(`${tableId}-delete-modal`);
    const confirmBtn = document.getElementById(`${tableId}-delete-confirm`);
    
    if (!modal) return;
    
    modal.style.display = 'flex';
    
    // Setup delete handler
    confirmBtn.onclick = () => {
        confirmBtn.disabled = true;
        confirmBtn.textContent = 'Deleting...';
        
        deleteTableItem(tableId, itemId)
            .then(() => {
                closeModal(`${tableId}-delete`);
            })
            .finally(() => {
                confirmBtn.disabled = false;
                confirmBtn.textContent = 'Delete';
            });
    };
}

// Generate edit form based on table columns
function generateEditForm(tableId, data) {
    const table = adminTables[tableId];
    const columns = table.config.columns;
    
    let html = '';
    
    columns.forEach(column => {
        if (column.key === 'id') return; // Skip ID field
        
        const value = data[column.key] || '';
        const fieldId = `${tableId}-${column.key}`;
        
        html += `<div class="form-group">`;
        html += `<label for="${fieldId}">${column.label}</label>`;
        
        if (column.key.includes('description') || column.key.includes('content')) {
            html += `<textarea id="${fieldId}" name="${column.key}">${value}</textarea>`;
        } else if (column.key === 'category_id') {
            html += generateCategorySelect(fieldId, column.key, value);
        } else if (column.key === 'role') {
            html += generateRoleSelect(fieldId, column.key, value);
        } else if (column.format === 'currency') {
            html += `<input type="number" step="0.01" id="${fieldId}" name="${column.key}" value="${value}">`;
        } else if (column.format === 'date') {
            const dateValue = value ? new Date(value).toISOString().split('T')[0] : '';
            html += `<input type="date" id="${fieldId}" name="${column.key}" value="${dateValue}">`;
        } else {
            html += `<input type="text" id="${fieldId}" name="${column.key}" value="${value}">`;
        }
        
        html += `</div>`;
    });
    
    return html;
}

// Generate view content
function generateViewContent(tableId, data) {
    const table = adminTables[tableId];
    const columns = table.config.columns;
    
    let html = '';
    
    columns.forEach(column => {
        let value = data[column.key] || '';
        
        // Format value based on column format
        if (column.format) {
            const adminTable = new AdminTable(tableId, table.config);
            value = adminTable.formatValue(value, column.format, data);
        }
        
        html += `<div class="view-item">`;
        html += `<div class="view-label">${column.label}:</div>`;
        html += `<div class="view-value">${value}</div>`;
        html += `</div>`;
    });
    
    return html;
}

// Generate category select dropdown
function generateCategorySelect(fieldId, fieldName, currentValue) {
    // This should be populated with actual categories from the API
    return `
        <select id="${fieldId}" name="${fieldName}">
            <option value="">Select Category</option>
            <option value="1" ${currentValue == 1 ? 'selected' : ''}>Note</option>
            <option value="2" ${currentValue == 2 ? 'selected' : ''}>Write</option>
            <option value="3" ${currentValue == 3 ? 'selected' : ''}>Type</option>
            <option value="4" ${currentValue == 4 ? 'selected' : ''}>Essentials</option>
        </select>
    `;
}

// Generate role select dropdown
function generateRoleSelect(fieldId, fieldName, currentValue) {
    return `
        <select id="${fieldId}" name="${fieldName}">
            <option value="2" ${currentValue == 2 ? 'selected' : ''}>Customer</option>
            <option value="1" ${currentValue == 1 ? 'selected' : ''}>Admin</option>
        </select>
    `;
}

// Save item function
async function saveItem(tableId, itemId) {
    const table = adminTables[tableId];
    if (!table) return;
    
    const form = document.getElementById(`${tableId}-edit-form`);
    const formData = new FormData(form);
    
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    
    try {
        const response = await fetch(`${table.config.apiEndpoint.replace('/table/', '/')}/${itemId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success || response.ok) {
            showNotification('item updated successfully', 'success');
            closeModal(`${tableId}-edit`);
            table.refresh();
        } else {
            showNotification(result.message || 'failed to update item', 'error');
        }
    } catch (error) {
        console.error('Error saving item:', error);
        showNotification('error saving item', 'error');
    }
}

// Enhanced modal close function
function closeModal(modalId) {
    if (modalId.includes('-')) {
        const modal = document.getElementById(`${modalId}-modal`);
        if (modal) {
            modal.style.display = 'none';
        }
    } else {
        const modal = document.getElementById(`${modalId}-modal`);
        if (modal) {
            modal.style.display = 'none';
        }
    }
}

// Delete item from table
async function deleteTableItem(tableId, itemId) {
    const table = adminTables[tableId];
    if (!table) return;
    
    try {
        const response = await fetch(`${table.config.deleteEndpoint}/${itemId}`, {
            method: 'DELETE'
        });
        
        const result = await response.json();
        
        if (result.success) {
            table.refresh();
            showNotification('item deleted successfully', 'success');
            return Promise.resolve();
        } else {
            throw new Error(result.message || 'Failed to delete item');
        }
    } catch (error) {
        console.error('Error deleting item:', error);
        showNotification(error.message, 'error');
        return Promise.reject(error);
    }
}

// Modal functions
function openModal(tableId, title, content) {
    const modal = document.getElementById(`${tableId}-modal`);
    const titleEl = document.getElementById(`${tableId}-modal-title`);
    const bodyEl = document.getElementById(`${tableId}-modal-body`);
    
    if (modal && titleEl && bodyEl) {
        titleEl.textContent = title;
        bodyEl.innerHTML = content;
        modal.style.display = 'flex';
        
        // Focus trap
        const firstInput = modal.querySelector('input, select, textarea, button');
        if (firstInput) firstInput.focus();
    }
}

function closeModal(tableId) {
    // Handle both old and new modal naming conventions
    let modal = document.getElementById(`${tableId}-modal`);
    if (!modal) {
        modal = document.getElementById(`${tableId}`);
    }
    if (modal) {
        modal.style.display = 'none';
    }
}

// We're using the shared notification system from notifications.js

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Product Stock Modal Function
function openProductStockModal(itemId) {
    const modal = document.getElementById('products-table-edit-modal');
    const titleEl = modal.querySelector('.modal-header h3');
    const contentEl = modal.querySelector('.form-content');
    const saveBtn = document.getElementById('products-table-edit-save');
    
    if (!modal) return;
    
    // Update modal for stock management
    titleEl.textContent = 'Manage Product Stock';
    contentEl.innerHTML = '<div class="loading-spinner"></div><p>Loading product stock data...</p>';
    
    modal.style.display = 'flex';
    
    // Fetch product data including stock
    fetch(`/api/admin/products/${itemId}?include_stock=true`)
        .then(response => response.json())
        .then(result => {
            const data = result.data || result;
            contentEl.innerHTML = `
                <div class="stock-management-form">
                    <div class="form-group">
                        <label>Product Name</label>
                        <input type="text" value="${data.name || ''}" readonly class="readonly">
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Current Stock</label>
                            <input type="text" value="${data.stock_quantity || 0}" readonly class="readonly">
                        </div>
                        <div class="form-group">
                            <label for="stock-action">Action</label>
                            <select id="stock-action" name="action">
                                <option value="set">Set to</option>
                                <option value="add">Add</option>
                                <option value="subtract">Subtract</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="stock-quantity">Quantity</label>
                        <input type="number" id="stock-quantity" name="quantity" min="0" value="0" required>
                    </div>
                    <div class="form-group">
                        <label for="stock-reason">Reason (Optional)</label>
                        <textarea id="stock-reason" name="reason" placeholder="Reason for stock change..." rows="3"></textarea>
                    </div>
                </div>
            `;
            
            // Setup save handler for stock update
            saveBtn.onclick = () => saveStockUpdate(itemId);
            
            // Focus on quantity input
            document.getElementById('stock-quantity').focus();
        })
        .catch(error => {
            console.error('Error loading product stock:', error);
            contentEl.innerHTML = '<p class="text-danger">Error loading product stock data</p>';
        });
}

// Save stock update function
async function saveStockUpdate(itemId) {
    const action = document.getElementById('stock-action').value;
    const quantity = parseInt(document.getElementById('stock-quantity').value);
    const reason = document.getElementById('stock-reason').value.trim();
    
    if (isNaN(quantity) || quantity < 0) {
        showNotification('please enter a valid quantity', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/api/admin/products/${itemId}/stock`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                action: action,
                quantity: quantity,
                reason: reason
            })
        });
        
        const result = await response.json();
        
        if (result.success || response.ok) {
            showNotification('stock updated successfully', 'success');
            closeModal('products-table-edit');
            refreshTable('products-table');
        } else {
            showNotification(result.message || 'failed to update stock', 'error');
        }
    } catch (error) {
        console.error('Error updating stock:', error);
        showNotification('error updating stock', 'error');
    }
}

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        AdminTable,
        initializeTable,
        refreshTable,
        goToPage,
        changePage,
        handleTableAction,
        openProductStockModal
    };
}