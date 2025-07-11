/* ======================= */
/* TABLE CONFIGURATION HELPERS */
/* ======================= */

// Common column configurations for different data types
const TableColumns = {
    // Standard ID column
    id: {
        key: 'id',
        label: 'ID',
        width: '80px',
        sortable: true
    },

    // Name/title column
    name: {
        key: 'name',
        label: 'Name',
        sortable: true
    },

    // Email column
    email: {
        key: 'email',
        label: 'Email',
        sortable: true
    },

    // Price column
    price: {
        key: 'price',
        label: 'Price',
        width: '100px',
        format: 'currency',
        class: 'text-right',
        sortable: true
    },

    // Date columns
    created_at: {
        key: 'created_at',
        label: 'Created',
        width: '120px',
        format: 'date',
        sortable: true
    },

    updated_at: {
        key: 'updated_at',
        label: 'Updated',
        width: '120px',
        format: 'date',
        sortable: true
    },

    // Status column
    status: {
        key: 'status',
        label: 'Status',
        width: '100px',
        format: 'status',
        sortable: true
    },

    // Role column
    role: {
        key: 'role',
        label: 'Role',
        width: '100px',
        format: 'role',
        sortable: true
    },

    // Counter columns
    count: function(key, label) {
        return {
            key: key,
            label: label,
            width: '100px',
            class: 'text-center',
            sortable: true
        };
    }
};

// Common action configurations
const TableActions = {
    view: {
        key: 'view',
        label: 'View',
        icon: 'VIEW',
        class: 'btn-view'
    },

    edit: {
        key: 'edit',
        label: 'Edit',
        icon: 'EDIT',
        class: 'btn-edit'
    },

    delete: {
        key: 'delete',
        label: 'Delete',
        icon: 'DELETE',
        class: 'btn-delete'
    },

    // Custom action creator
    custom: function(key, label, icon, className) {
        return {
            key: key,
            label: label,
            icon: icon || '',
            class: className || 'btn-secondary'
        };
    }
};

// Common filter configurations
const TableFilters = {
    // Status filters
    status: {
        active: { value: 'active', label: 'Active' },
        inactive: { value: 'inactive', label: 'Inactive' },
        pending: { value: 'pending', label: 'Pending' }
    },

    // Role filters
    roles: {
        admin: { value: 'admin', label: 'Admin Users' },
        customer: { value: 'customer', label: 'Customer Users' }
    },

    // Category filters (you'll need to populate this dynamically)
    categories: function(categories) {
        return categories.map(cat => ({
            value: cat.id,
            label: `Category: ${cat.name}`
        }));
    }
};

// Quick table configuration builder
function buildTableConfig(tableName, columns, options = {}) {
    return {
        table_id: options.tableId || `${tableName.toLowerCase()}-table`,
        table_name: tableName,
        columns: columns,
        filters: options.filters || [],
        actions: options.actions || [TableActions.edit, TableActions.delete]
    };
}

// Quick JavaScript initialization helper
function quickInitTable(tableId, entity, columns, options = {}) {
    const config = {
        apiEndpoint: `/api/admin/table/${entity}`,
        deleteEndpoint: `/api/admin/table/${entity}`,
        itemName: entity.slice(0, -1), // Remove 's' to make singular
        columns: columns,
        actions: options.actions || [
            {
                ...TableActions.edit,
                handler: options.editHandler || function(id) {
                    showNotification('edit functionality coming soon!', 'info');
                }
            },
            TableActions.delete
        ],
        customFormatters: options.customFormatters || {}
    };

    initializeTable(tableId, config);
}

// Export for global use
if (typeof window !== 'undefined') {
    window.TableColumns = TableColumns;
    window.TableActions = TableActions;
    window.TableFilters = TableFilters;
    window.buildTableConfig = buildTableConfig;
    window.quickInitTable = quickInitTable;
}
