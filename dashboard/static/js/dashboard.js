/**
 * Dashboard JavaScript
 * 
 * Handles charts, interactivity, and API calls for the dashboard.
 */

// Simple chart rendering using Canvas API (no external dependencies)
class SimpleChart {
    constructor(canvasId, data, options = {}) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) {
            console.error(`Canvas element with id "${canvasId}" not found`);
            return;
        }
        this.ctx = this.canvas.getContext('2d');
        this.data = data;
        this.options = {
            type: options.type || 'bar',
            color: options.color || '#4a90e2',
            backgroundColor: options.backgroundColor || 'rgba(74, 144, 226, 0.2)',
            borderColor: options.borderColor || '#4a90e2',
            borderWidth: options.borderWidth || 2,
            padding: options.padding || 40,
            ...options
        };
        this.init();
    }

    init() {
        // Set canvas size
        const parent = this.canvas.parentElement;
        this.canvas.width = parent.clientWidth;
        this.canvas.height = 300;
        
        // Draw chart
        if (this.options.type === 'bar') {
            this.drawBarChart();
        } else if (this.options.type === 'line') {
            this.drawLineChart();
        }
    }

    drawBarChart() {
        const labels = Object.keys(this.data);
        const values = Object.values(this.data);
        
        if (labels.length === 0) {
            this.drawNoData();
            return;
        }

        const maxValue = Math.max(...values, 0);
        const padding = this.options.padding;
        const chartWidth = this.canvas.width - 2 * padding;
        const chartHeight = this.canvas.height - 2 * padding;
        const barWidth = chartWidth / labels.length * 0.8;
        const barSpacing = chartWidth / labels.length * 0.2;

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw axes
        this.ctx.strokeStyle = '#404040';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, this.canvas.height - padding);
        this.ctx.lineTo(this.canvas.width - padding, this.canvas.height - padding);
        this.ctx.stroke();

        // Draw bars
        labels.forEach((label, index) => {
            const value = values[index];
            const barHeight = maxValue > 0 ? (value / maxValue) * chartHeight : 0;
            const x = padding + index * (barWidth + barSpacing) + barSpacing / 2;
            const y = this.canvas.height - padding - barHeight;

            // Draw bar
            this.ctx.fillStyle = this.options.backgroundColor;
            this.ctx.fillRect(x, y, barWidth, barHeight);
            
            this.ctx.strokeStyle = this.options.borderColor;
            this.ctx.lineWidth = this.options.borderWidth;
            this.ctx.strokeRect(x, y, barWidth, barHeight);

            // Draw value on top
            this.ctx.fillStyle = '#e0e0e0';
            this.ctx.font = '12px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(value.toFixed(2), x + barWidth / 2, y - 5);

            // Draw label
            this.ctx.save();
            this.ctx.translate(x + barWidth / 2, this.canvas.height - padding + 10);
            this.ctx.rotate(-Math.PI / 4);
            this.ctx.textAlign = 'right';
            this.ctx.fillStyle = '#b0b0b0';
            this.ctx.font = '11px sans-serif';
            this.ctx.fillText(label, 0, 0);
            this.ctx.restore();
        });
    }

    drawLineChart() {
        const labels = Object.keys(this.data);
        const values = Object.values(this.data);
        
        if (labels.length === 0) {
            this.drawNoData();
            return;
        }

        const maxValue = Math.max(...values, 0);
        const padding = this.options.padding;
        const chartWidth = this.canvas.width - 2 * padding;
        const chartHeight = this.canvas.height - 2 * padding;
        const stepX = chartWidth / (labels.length - 1 || 1);

        // Clear canvas
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

        // Draw axes
        this.ctx.strokeStyle = '#404040';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.moveTo(padding, padding);
        this.ctx.lineTo(padding, this.canvas.height - padding);
        this.ctx.lineTo(this.canvas.width - padding, this.canvas.height - padding);
        this.ctx.stroke();

        // Draw line
        this.ctx.beginPath();
        this.ctx.strokeStyle = this.options.borderColor;
        this.ctx.lineWidth = this.options.borderWidth;
        
        values.forEach((value, index) => {
            const x = padding + index * stepX;
            const y = this.canvas.height - padding - (maxValue > 0 ? (value / maxValue) * chartHeight : 0);
            
            if (index === 0) {
                this.ctx.moveTo(x, y);
            } else {
                this.ctx.lineTo(x, y);
            }
        });
        this.ctx.stroke();

        // Draw points and labels
        values.forEach((value, index) => {
            const x = padding + index * stepX;
            const y = this.canvas.height - padding - (maxValue > 0 ? (value / maxValue) * chartHeight : 0);
            
            // Draw point
            this.ctx.fillStyle = this.options.color;
            this.ctx.beginPath();
            this.ctx.arc(x, y, 4, 0, 2 * Math.PI);
            this.ctx.fill();

            // Draw value
            this.ctx.fillStyle = '#e0e0e0';
            this.ctx.font = '12px sans-serif';
            this.ctx.textAlign = 'center';
            this.ctx.fillText(value.toFixed(2), x, y - 10);

            // Draw label
            this.ctx.save();
            this.ctx.translate(x, this.canvas.height - padding + 10);
            this.ctx.rotate(-Math.PI / 4);
            this.ctx.textAlign = 'right';
            this.ctx.fillStyle = '#b0b0b0';
            this.ctx.font = '11px sans-serif';
            this.ctx.fillText(labels[index], 0, 0);
            this.ctx.restore();
        });
    }

    drawNoData() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        this.ctx.fillStyle = '#808080';
        this.ctx.font = '16px sans-serif';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('No data available', this.canvas.width / 2, this.canvas.height / 2);
    }
}

// Create revenue chart
function createRevenueChart(canvasId, data) {
    new SimpleChart(canvasId, data, {
        type: 'bar',
        color: '#4a90e2',
        backgroundColor: 'rgba(74, 144, 226, 0.3)',
        borderColor: '#4a90e2',
        borderWidth: 2
    });
}

// Create hours chart
function createHoursChart(canvasId, data) {
    new SimpleChart(canvasId, data, {
        type: 'line',
        color: '#2ecc71',
        backgroundColor: 'rgba(46, 204, 113, 0.2)',
        borderColor: '#2ecc71',
        borderWidth: 3
    });
}

// API functions
async function fetchAPI(endpoint) {
    try {
        const response = await fetch(`/api${endpoint}`);
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('API fetch error:', error);
        return null;
    }
}

// Refresh dashboard data
async function refreshData() {
    const currentPath = window.location.pathname;
    
    if (currentPath === '/') {
        const overview = await fetchAPI('/overview');
        if (overview) {
            // Update overview stats dynamically
            console.log('Overview data refreshed:', overview);
        }
    } else if (currentPath === '/projects') {
        const projects = await fetchAPI('/projects');
        if (projects) {
            console.log('Projects data refreshed:', projects);
        }
    }
    // Add more endpoints as needed
}

// Auto-refresh functionality
let autoRefreshInterval = null;

function startAutoRefresh(intervalSeconds = 300) {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        console.log('Auto-refreshing data...');
        refreshData();
    }, intervalSeconds * 1000);
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
    }
}

// Table sorting
function sortTable(tableId, columnIndex, ascending = true) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    rows.sort((a, b) => {
        const aValue = a.cells[columnIndex].textContent.trim();
        const bValue = b.cells[columnIndex].textContent.trim();
        
        // Try to parse as number
        const aNum = parseFloat(aValue.replace(/[^0-9.-]/g, ''));
        const bNum = parseFloat(bValue.replace(/[^0-9.-]/g, ''));
        
        if (!isNaN(aNum) && !isNaN(bNum)) {
            return ascending ? aNum - bNum : bNum - aNum;
        }
        
        // String comparison
        return ascending ? 
            aValue.localeCompare(bValue) : 
            bValue.localeCompare(aValue);
    });
    
    // Re-append sorted rows
    rows.forEach(row => tbody.appendChild(row));
}

// Filter table rows
function filterTable(tableId, filterText) {
    const table = document.getElementById(tableId);
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    const rows = tbody.querySelectorAll('tr');
    
    filterText = filterText.toLowerCase();
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(filterText) ? '' : 'none';
    });
}

// Format currency
function formatCurrency(amount, currency = 'USD') {
    const symbols = {
        'USD': '$',
        'EUR': '€',
        'GBP': '£',
        'JPY': '¥'
    };
    
    const symbol = symbols[currency] || currency + ' ';
    return `${symbol}${parseFloat(amount).toFixed(2)}`;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard initialized');
    
    // Optional: Start auto-refresh (disabled by default)
    // startAutoRefresh(300); // Refresh every 5 minutes
    
    // Add event listeners for interactive elements
    const sortableHeaders = document.querySelectorAll('th.sortable');
    sortableHeaders.forEach(header => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            const table = this.closest('table');
            const columnIndex = Array.from(this.parentElement.children).indexOf(this);
            const isAscending = !this.classList.contains('sorted-asc');
            
            // Remove sorted classes from all headers
            sortableHeaders.forEach(h => {
                h.classList.remove('sorted-asc', 'sorted-desc');
            });
            
            // Add sorted class to current header
            this.classList.add(isAscending ? 'sorted-asc' : 'sorted-desc');
            
            // Sort table
            sortTable(table.id, columnIndex, isAscending);
        });
    });
});

// Export functions for use in templates
window.createRevenueChart = createRevenueChart;
window.createHoursChart = createHoursChart;
window.fetchAPI = fetchAPI;
window.refreshData = refreshData;
window.startAutoRefresh = startAutoRefresh;
window.stopAutoRefresh = stopAutoRefresh;
window.sortTable = sortTable;
window.filterTable = filterTable;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
