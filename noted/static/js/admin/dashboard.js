/**
 * Dashboard Handler - Manage dashboard analytics and stats
 */

class DashboardHandler {
    constructor() {
        this.statsData = {};
        this.chartsInitialized = false;
        
        // Chart instances
        this.salesChart = null;
        this.ordersChart = null;
        this.productsChart = null;
        
        // Chart colors
        this.chartColors = {
            primary: 'rgba(78, 115, 223, 1)',
            secondary: 'rgba(28, 200, 138, 1)',
            accent: 'rgba(246, 194, 62, 1)',
            danger: 'rgba(231, 74, 59, 1)',
            light: 'rgba(133, 135, 150, 0.2)',
            dark: 'rgba(90, 92, 105, 1)',
            transparentPrimary: 'rgba(78, 115, 223, 0.1)',
            transparentSecondary: 'rgba(28, 200, 138, 0.1)',
            transparentAccent: 'rgba(246, 194, 62, 0.1)',
            transparentDanger: 'rgba(231, 74, 59, 0.1)'
        };
        
        console.log('Dashboard Handler initialized');
    }
    
    /**
     * Initialize dashboard with data and charts
     */
    async init() {
        console.log('Initializing dashboard...');
        
        try {
            // Show loading state
            this.toggleLoading(true);
            
            // Fetch data
            await this.fetchDashboardData();
            
            // Update stats cards
            this.updateStatCards();
            
            // Initialize charts if dashboard has charts section
            if (document.querySelector('.charts-section')) {
                this.initializeCharts();
            }
            
            // Update last updated timestamp
            this.updateLastUpdated();
            
        } catch (error) {
            console.error('Error initializing dashboard:', error);
            alert('error loading dashboard data: ' + error.message);
        } finally {
            // Hide loading state
            this.toggleLoading(false);
        }
    }
    
    /**
     * Fetch dashboard data from API
     */
    async fetchDashboardData() {
        try {
            const response = await fetch('/api/admin/dashboard', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'include'
            });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status} ${response.statusText}`);
            }
            
            this.statsData = await response.json();
            console.log('Dashboard data loaded:', this.statsData);
            
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            
            // Fallback to analytics.json if API fails
            try {
                const fallbackResponse = await fetch('/static/data/analytics.json');
                if (fallbackResponse.ok) {
                    const analyticsData = await fallbackResponse.json();
                    this.statsData = analyticsData;
                    console.log('Using fallback analytics data');
                }
            } catch (fallbackError) {
                console.error('Error loading fallback data:', fallbackError);
                throw error; // Throw the original error
            }
        }
    }
    
    /**
     * Show or hide loading state - now uses notifications only
     */
    toggleLoading(show) {
        // Loading overlay removed, now using notifications only
    }
    
    /**
     * Update stat cards with data
     */
    updateStatCards() {
        // Dashboard stats from the data
        const dashboard = this.statsData.dashboard || {};
        
        // Update each stat card if the element exists
        this.updateStatValue('total-sales', dashboard.total_sales, 'currency');
        this.updateStatValue('monthly-sales', dashboard.monthly_sales, 'currency');
        this.updateStatValue('total-orders', dashboard.total_orders, 'number');
        this.updateStatValue('monthly-orders', dashboard.monthly_orders, 'number');
        this.updateStatValue('total-customers', dashboard.total_customers || this.statsData.users?.total_users, 'number');
        this.updateStatValue('active-products', dashboard.active_products || this.statsData.products?.total_products, 'number');
        
        // Revenue growth with trend indicator
        if (document.getElementById('revenue-growth')) {
            const growthValue = dashboard.revenue_growth || 0;
            const formattedValue = this.formatValue(growthValue, 'percentage');
            const trendClass = growthValue >= 0 ? 'positive' : 'negative';
            const trendArrow = growthValue >= 0 ? '↑' : '↓';
            
            document.getElementById('revenue-growth').innerHTML = 
                `${formattedValue} <span class="trend-indicator ${trendClass}">${trendArrow}</span>`;
        }
        
        // Products page stats
        const products = this.statsData.products || {};
        this.updateStatValue('total-products', products.total_products, 'number');
        this.updateStatValue('total-categories', products.total_categories, 'number');
        this.updateStatValue('out-of-stock', products.out_of_stock_count, 'number');
        
        // Orders page stats
        const orders = this.statsData.orders || {};
        this.updateStatValue('paid-orders', orders.paid_orders, 'number');
        this.updateStatValue('unpaid-orders', orders.unpaid_orders, 'number');
        this.updateStatValue('total-revenue', dashboard.total_sales, 'currency');
        
        // Users page stats
        const users = this.statsData.users || {};
        this.updateStatValue('total-users', users.total_users, 'number');
        this.updateStatValue('total-admins', users.total_admins, 'number');
        this.updateStatValue('total-customers', users.total_customers, 'number');
        this.updateStatValue('users-with-orders', users.users_with_orders, 'number');
        
        // Categories page stats
        const categories = this.statsData.products || {};
        this.updateStatValue('total-categories', categories.total_categories, 'number');
        this.updateStatValue('active-categories', categories.total_categories, 'number');
        this.updateStatValue('products-assigned', categories.total_products, 'number');
    }
    
    /**
     * Update a single stat value with formatting
     */
    updateStatValue(elementId, value, format) {
        const element = document.getElementById(elementId);
        if (element && value !== undefined) {
            element.textContent = this.formatValue(value, format);
        }
    }
    
    /**
     * Format a value based on type
     */
    formatValue(value, format) {
        if (value === undefined || value === null) return '--';
        
        switch (format) {
            case 'currency':
                return AdminTableUtils.formatCurrency(value);
            case 'percentage':
                return `${parseFloat(value).toFixed(1)}%`;
            case 'number':
            default:
                return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        }
    }
    
    /**
     * Initialize dashboard charts
     */
    initializeCharts() {
        if (this.chartsInitialized) return;
        
        const chartsSection = document.querySelector('.charts-section');
        if (!chartsSection) return;
        
        // Create chart containers if they don't exist
        if (!document.getElementById('sales-chart-container')) {
            chartsSection.innerHTML = `
                <div class="charts-grid">
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3>Sales Overview</h3>
                            <p>Monthly sales data</p>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="sales-chart"></canvas>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3>Orders Timeline</h3>
                            <p>Daily order count</p>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="orders-chart"></canvas>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3>Top Products</h3>
                            <p>Best selling products</p>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="products-chart"></canvas>
                        </div>
                    </div>
                    <div class="chart-container">
                        <div class="chart-header">
                            <h3>Products by Category</h3>
                            <p>Category distribution</p>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="categories-chart"></canvas>
                        </div>
                    </div>
                </div>
            `;
        }
        
        // Initialize charts
        this.initSalesChart();
        this.initOrdersChart();
        this.initProductsChart();
        this.initCategoriesChart();
        
        this.chartsInitialized = true;
    }
    
    /**
     * Initialize sales chart
     */
    initSalesChart() {
        const ctx = document.getElementById('sales-chart');
        if (!ctx) return;
        
        // Get sales data
        const salesData = this.statsData.analytics?.sales_by_month || this.getDefaultSalesData();
        
        this.salesChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: salesData.map(item => item.month),
                datasets: [{
                    label: 'Sales (€)',
                    data: salesData.map(item => item.sales),
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 2,
                    tension: 0.3,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Sales: ${AdminTableUtils.formatCurrency(context.raw)}`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return AdminTableUtils.formatCurrency(value);
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Initialize orders chart
     */
    initOrdersChart() {
        const ctx = document.getElementById('orders-chart');
        if (!ctx) return;
        
        // Get orders data
        const ordersData = this.statsData.analytics?.orders_by_day || this.getDefaultOrdersData();
        
        this.ordersChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ordersData.map(item => item.date),
                datasets: [{
                    label: 'Orders',
                    data: ordersData.map(item => item.count),
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Initialize products chart
     */
    initProductsChart() {
        const ctx = document.getElementById('products-chart');
        if (!ctx) return;
        
        // Get top products data
        const productsData = this.statsData.analytics?.top_products || this.getDefaultProductsData();
        
        this.productsChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: productsData.map(item => item.name),
                datasets: [{
                    label: 'Revenue',
                    data: productsData.map(item => item.revenue),
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(255, 206, 86, 0.5)',
                        'rgba(75, 192, 192, 0.5)',
                        'rgba(153, 102, 255, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `Revenue: ${AdminTableUtils.formatCurrency(context.raw)}`;
                            }
                        }
                    }
                }
            }
        });
    }
    
    /**
     * Initialize categories chart
     */
    initCategoriesChart() {
        const ctx = document.getElementById('categories-chart');
        if (!ctx) return;
        
        // Get categories data
        const categoriesData = this.statsData.products?.products_by_category || this.getDefaultCategoriesData();
        
        // Create chart
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categoriesData.map(item => item.name),
                datasets: [{
                    label: 'Products',
                    data: categoriesData.map(item => item.count),
                    backgroundColor: [
                        'rgba(255, 159, 64, 0.5)',
                        'rgba(255, 99, 132, 0.5)',
                        'rgba(54, 162, 235, 0.5)',
                        'rgba(75, 192, 192, 0.5)'
                    ],
                    borderColor: [
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(75, 192, 192, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    }
    
    /**
     * Update last updated timestamp
     */
    updateLastUpdated() {
        const lastUpdatedElement = document.getElementById('last-updated');
        if (lastUpdatedElement) {
            const timestamp = this.statsData.last_updated 
                ? new Date(this.statsData.last_updated).toLocaleString()
                : new Date().toLocaleString();
                
            lastUpdatedElement.textContent = timestamp;
        }
    }
    
    /**
     * Generate default data if none is available
     */
    getDefaultSalesData() {
        return [
            { month: 'Jan', sales: 1200 },
            { month: 'Feb', sales: 1900 },
            { month: 'Mar', sales: 1500 },
            { month: 'Apr', sales: 1800 },
            { month: 'May', sales: 2200 },
            { month: 'Jun', sales: 1700 }
        ];
    }
    
    getDefaultOrdersData() {
        return [
            { date: 'Mon', count: 5 },
            { date: 'Tue', count: 8 },
            { date: 'Wed', count: 6 },
            { date: 'Thu', count: 9 },
            { date: 'Fri', count: 12 },
            { date: 'Sat', count: 15 },
            { date: 'Sun', count: 10 }
        ];
    }
    
    getDefaultProductsData() {
        return [
            { name: 'Product A', revenue: 5200 },
            { name: 'Product B', revenue: 3800 },
            { name: 'Product C', revenue: 2900 },
            { name: 'Product D', revenue: 1500 },
            { name: 'Others', revenue: 3600 }
        ];
    }
    
    getDefaultCategoriesData() {
        return [
            { name: 'note', count: 8 },
            { name: 'write', count: 8 },
            { name: 'type', count: 8 },
            { name: 'essentials', count: 7 }
        ];
    }
    
    /**
     * Refresh dashboard data and update UI
     */
    async refreshDashboard() {
        try {
            this.toggleLoading(true);
            
            // Fetch fresh data
            await this.fetchDashboardData();
            
            // Update UI components
            this.updateStatCards();
            this.updateCharts();
            this.updateLastUpdated();
            
            console.log('Dashboard refreshed');
            
        } catch (error) {
            console.error('Error refreshing dashboard:', error);
            alert('error refreshing dashboard: ' + error.message);
        } finally {
            this.toggleLoading(false);
        }
    }
    
    /**
     * Update existing charts with new data
     */
    updateCharts() {
        if (!this.chartsInitialized) {
            this.initializeCharts();
            return;
        }
        
        // Update sales chart
        if (this.salesChart) {
            const salesData = this.statsData.analytics?.sales_by_month || this.getDefaultSalesData();
            this.salesChart.data.labels = salesData.map(item => item.month);
            this.salesChart.data.datasets[0].data = salesData.map(item => item.sales);
            this.salesChart.update();
        }
        
        // Update orders chart
        if (this.ordersChart) {
            const ordersData = this.statsData.analytics?.orders_by_day || this.getDefaultOrdersData();
            this.ordersChart.data.labels = ordersData.map(item => item.date);
            this.ordersChart.data.datasets[0].data = ordersData.map(item => item.count);
            this.ordersChart.update();
        }
        
        // Update products chart
        if (this.productsChart) {
            const productsData = this.statsData.analytics?.top_products || this.getDefaultProductsData();
            this.productsChart.data.labels = productsData.map(item => item.name);
            this.productsChart.data.datasets[0].data = productsData.map(item => item.revenue);
            this.productsChart.update();
        }
    }
}

// Initialize dashboard when document is ready
document.addEventListener('DOMContentLoaded', function() {
    const currentPath = window.location.pathname;
    
    // Initialize dashboard on dashboard page only
    if (currentPath.includes('/admin/dashboard') || currentPath === '/admin' || currentPath.endsWith('/admin/')) {
        window.dashboardHandler = new DashboardHandler();
        window.dashboardHandler.init();
    }
});

// Global refresh function for dashboard
function refreshDashboard() {
    if (window.dashboardHandler) {
        window.dashboardHandler.refreshDashboard();
    } else {
        console.error('Dashboard handler not initialized');
    }
}

// Export for global use
window.refreshDashboard = refreshDashboard;
