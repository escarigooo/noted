/**
 * Graphics Data Handler - Interactive Charts for Analytics Page
 */

class GraphicsHandler {
    constructor() {
        this.dataUrl = '/static/data/graphics.json';
        this.refreshUrl = '/admin/refresh-graphics';
        this.data = null;
        this.charts = {};
        this.currentFilter = 'Last 12 months';
    }

    async fetchData() {
        try {
            const response = await fetch(this.dataUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            this.data = await response.json();
            console.log('DATA Graphics data loaded:', this.data);
            return this.data;
        } catch (error) {
            console.error('FAILED Error fetching graphics data:', error);
            return null;
        }
    }

    async refreshGraphics() {
        try {
            console.log('REFRESH Refreshing graphics data...');
            
            const response = await fetch(this.refreshUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const result = await response.json();
            
            if (result.success) {
                this.data = result.data;
                console.log('SUCCESS Graphics refreshed successfully');
                this.updateAllCharts();
                return this.data;
            } else {
                throw new Error(result.error || 'Failed to refresh graphics');
            }
            
        } catch (error) {
            console.error('FAILED Error refreshing graphics:', error);
            throw error;
        }
    }

    initializeCharts() {
        if (!this.data) return;

        // Destroy existing charts before creating new ones
        this.destroyAllCharts();

        this.createSalesChart();
        this.createOrdersChart();
        this.createProductsChart();
        this.createTopCustomersChart();
        this.setupFilters();
        this.updateLastUpdated();
    }

    destroyAllCharts() {
        // Destroy all existing charts to prevent canvas reuse errors
        Object.values(this.charts).forEach(chart => {
            if (chart && typeof chart.destroy === 'function') {
                chart.destroy();
            }
        });
        this.charts = {};
    }

    createSalesChart() {
        const ctx = document.getElementById('salesChart');
        if (!ctx) return;

        // Use dynamic date range data or fallback to backward compatibility
        const chartData = this.data.date_ranges?.[this.currentFilter]?.sales_chart || this.data.sales_chart;
        if (!chartData || !chartData.data) {
            console.warn('WARNING No sales chart data available for:', this.currentFilter);
            return;
        }

        const config = {
            type: 'line',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Sales (€)',
                    data: chartData.data,
                    borderColor: '#3b82f6',
                    backgroundColor: 'rgba(59, 130, 246, 0.1)',
                    fill: true,
                    tension: 0.4,
                    pointBackgroundColor: '#3b82f6',
                    pointBorderColor: '#ffffff',
                    pointBorderWidth: 2,
                    pointRadius: 5
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: chartData.title
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '€' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        };

        this.charts.sales = new Chart(ctx, config);
    }

    createOrdersChart() {
        const ctx = document.getElementById('ordersChart');
        if (!ctx) return;

        // Use dynamic date range data or fallback to backward compatibility
        const chartData = this.data.date_ranges?.[this.currentFilter]?.orders_chart || this.data.orders_chart;
        if (!chartData || !chartData.data) {
            console.warn('WARNING No orders chart data available for:', this.currentFilter);
            return;
        }

        const config = {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Orders',
                    data: chartData.data,
                    backgroundColor: '#10b981',
                    borderColor: '#059669',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: chartData.title
                    },
                    legend: {
                        display: false
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
        };

        this.charts.orders = new Chart(ctx, config);
    }

    createProductsChart() {
        const ctx = document.getElementById('productsChart');
        if (!ctx) return;

        // Use static chart data (doesn't change with date range)
        const chartData = this.data.static_charts?.products_chart || this.data.products_chart;
        if (!chartData || !chartData.data) {
            console.warn('WARNING No products chart data available');
            return;
        }

        const config = {
            type: 'doughnut',
            data: {
                labels: chartData.labels,
                datasets: [{
                    data: chartData.data,
                    backgroundColor: [
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#8b5cf6',
                        '#06b6d4'
                    ],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: chartData.title
                    },
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        };

        this.charts.products = new Chart(ctx, config);
    }

    createTopCustomersChart() {
        const ctx = document.getElementById('topCustomersChart');
        if (!ctx) return;

        // Use static chart data (doesn't change with date range)
        const chartData = this.data.static_charts?.top_customers || this.data.top_customers;
        if (!chartData || !chartData.data) {
            console.warn('WARNING No top customers chart data available');
            return;
        }

        const config = {
            type: 'bar',
            data: {
                labels: chartData.labels,
                datasets: [{
                    label: 'Total Spent (€)',
                    data: chartData.data,
                    backgroundColor: '#8b5cf6',
                    borderColor: '#7c3aed',
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: chartData.title
                    },
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '€' + value.toLocaleString();
                            }
                        }
                    }
                }
            }
        };

        this.charts.topCustomers = new Chart(ctx, config);
    }

    setupFilters() {
        // Setup date range filter only
        const dateFilter = document.getElementById('dateFilter');
        if (dateFilter && this.data.filters && this.data.filters.date_ranges) {
            // Clear existing options
            dateFilter.innerHTML = '';
            
            // Add options from data
            this.data.filters.date_ranges.forEach(range => {
                const option = document.createElement('option');
                option.value = range;
                option.textContent = range;
                if (range === this.currentFilter) option.selected = true;
                dateFilter.appendChild(option);
            });

            dateFilter.addEventListener('change', (e) => {
                this.currentFilter = e.target.value;
                this.applyDateFilter(this.currentFilter);
            });
            
            console.log('SUCCESS Date filter setup complete');
        } else {
            console.warn('WARNING Date filter setup failed - missing elements or data');
        }
    }

    applyDateFilter(dateRange) {
        if (!this.data || !this.data.date_ranges || !this.data.date_ranges[dateRange]) {
            console.warn('WARNING No data available for date range:', dateRange);
            this.showFilterNotification(`No data available for ${dateRange}`, 'warning');
            return;
        }
        
        console.log('REFRESH Applying date filter:', dateRange);
        
        // Store current filter
        this.currentFilter = dateRange;
        
        // Get data for the selected date range
        const rangeData = this.data.date_ranges[dateRange];
        
        // Update sales chart
        if (this.charts.sales && rangeData.sales_chart) {
            this.charts.sales.data.labels = rangeData.sales_chart.labels;
            this.charts.sales.data.datasets[0].data = rangeData.sales_chart.data;
            this.charts.sales.options.plugins.title.text = rangeData.sales_chart.title;
            this.charts.sales.update('resize');
        }
        
        // Update orders chart
        if (this.charts.orders && rangeData.orders_chart) {
            this.charts.orders.data.labels = rangeData.orders_chart.labels;
            this.charts.orders.data.datasets[0].data = rangeData.orders_chart.data;
            this.charts.orders.options.plugins.title.text = rangeData.orders_chart.title;
            this.charts.orders.update('resize');
        }
        
        // Static charts don't need updating (products, top customers)
        // Show notification
        this.showFilterNotification(`Charts updated to show: ${dateRange}`);
        
        // Update last updated time
        this.updateLastUpdated();
    }

    showFilterNotification(message) {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.filter-notification');
        existingNotifications.forEach(n => n.remove());
        
        // Show a brief notification that filters were applied
        const notification = document.createElement('div');
        notification.className = 'filter-notification';
        notification.textContent = `REFRESH ${message}`;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #10b981;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 1000;
            font-size: 14px;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
            animation: slideInRight 0.3s ease-out;
        `;
        
        // Add animation styles
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
            style.remove();
        }, 3000);
    }

    updateAllCharts() {
        this.destroyAllCharts();
        this.initializeCharts();
    }

    updateLastUpdated() {
        const lastUpdated = document.getElementById('charts-last-updated'); // Fixed ID to match HTML
        if (lastUpdated && this.data) {
            const date = new Date(this.data.last_updated);
            const formattedDate = new Intl.DateTimeFormat('pt-PT', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
            lastUpdated.textContent = formattedDate || 'Unknown';
        }
    }

    hideLoading() {
        const loading = document.getElementById('graphics-loading');
        if (loading) {
            loading.style.display = 'none';
        }
    }

    showLoading() {
        const loading = document.getElementById('graphics-loading');
        if (loading) {
            loading.style.display = 'block';
        }
    }
}

// Export classes for global use - don't auto-initialize
window.GraphicsHandler = GraphicsHandler;

// Refresh function for manual use
window.refreshGraphics = async function() {
    if (!window.graphicsHandler) {
        console.error('FAILED Graphics handler not initialized');
        if (typeof showNotification === 'function') {
            showNotification('Graphics handler not initialized', 'error');
        }
        return;
    }
    
    const refreshBtn = document.querySelector('button[onclick="refreshGraphics()"]');
    
    try {
        // Show notification only, not loading state
        if (typeof showNotification === 'function') {
            showNotification('Refreshing charts data...', 'info');
        }
        
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.textContent = 'Refreshing...';
        }
        
        await window.graphicsHandler.refreshGraphics();
        
        console.log('SUCCESS Graphics refreshed successfully!');
        
        if (typeof showNotification === 'function') {
            showNotification('Charts data refreshed successfully!', 'success');
        }
        
    } catch (error) {
        console.error('FAILED Graphics refresh failed:', error);
        
        if (typeof showNotification === 'function') {
            showNotification('Failed to refresh charts data', 'error');
        } else {
            alert('Failed to refresh graphics: ' + error.message);
        }
    } finally {
        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Update Charts';
        }
    }
};
