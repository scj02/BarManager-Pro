// BarManager Pro - JavaScript Principal

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            if (bsAlert) {
                bsAlert.close();
            }
        });
    }, 5000);

    // Initialize DataTables if present
    if (typeof $.fn.DataTable !== 'undefined') {
        $('.data-table').DataTable({
            language: {
                url: '//cdn.datatables.net/plug-ins/1.11.5/i18n/es-ES.json'
            },
            responsive: true,
            pageLength: 25,
            order: [[0, 'desc']]
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });

    // Set active navigation item
    setActiveNavItem();
});

// Utility Functions for BarManager Pro
function showAlert(message, type = 'info', duration = 5000) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const main = document.querySelector('main') || document.body;
    main.insertBefore(alertDiv, main.firstChild);
    
    if (duration > 0) {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                const bsAlert = new bootstrap.Alert(alertDiv);
                bsAlert.close();
            }
        }, duration);
    }
    
    return alertDiv;
}

function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle',
        'primary': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0
    }).format(amount);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function formatTime(timeString) {
    if (!timeString) return '';
    const time = new Date(`2000-01-01T${timeString}`);
    return time.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// API Helper Functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    const config = { ...defaultOptions, ...options };
    
    try {
        const response = await fetch(url, config);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API Request Error:', error);
        throw error;
    }
}

// Loading States
function showLoading(element, text = 'Cargando...') {
    const originalContent = element.innerHTML;
    element.dataset.originalContent = originalContent;
    element.innerHTML = `<i class="fas fa-spinner fa-spin me-2"></i>${text}`;
    element.disabled = true;
    return originalContent;
}

function hideLoading(element) {
    if (element.dataset.originalContent) {
        element.innerHTML = element.dataset.originalContent;
        delete element.dataset.originalContent;
    }
    element.disabled = false;
}

// Navigation Helpers
function setActiveNavItem() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// BarManager Pro Specific Functions

// Inventory Management
function checkStockAlert(producto) {
    return producto.stock_actual <= producto.stock_minimo;
}

function getStockStatus(producto) {
    if (producto.stock_actual <= 0) {
        return { status: 'sin-stock', class: 'danger', text: 'Sin Stock' };
    } else if (producto.stock_actual <= producto.stock_minimo) {
        return { status: 'bajo-stock', class: 'warning', text: 'Stock Bajo' };
    } else {
        return { status: 'stock-ok', class: 'success', text: 'Stock OK' };
    }
}

// Sales Management
function calculateOrderTotal(detalles) {
    const subtotal = detalles.reduce((sum, detalle) => sum + (detalle.cantidad * detalle.precio_unitario), 0);
    const impuestos = subtotal * 0.16; // 16% IVA
    const total = subtotal + impuestos;
    
    return {
        subtotal: subtotal,
        impuestos: impuestos,
        total: total
    };
}

// Employee Management
function calculateCommission(empleado, ventas) {
    if (!empleado.puesto || !empleado.puesto.comision_porcentaje) {
        return 0;
    }
    
    const totalVentas = ventas.reduce((sum, venta) => sum + venta.total, 0);
    return totalVentas * (empleado.puesto.comision_porcentaje / 100);
}

// Table Management
function getTableStatus(mesa) {
    const statusConfig = {
        'LIBRE': { class: 'success', icon: 'check-circle', text: 'Libre' },
        'OCUPADA': { class: 'danger', icon: 'times-circle', text: 'Ocupada' },
        'RESERVADA': { class: 'warning', icon: 'clock', text: 'Reservada' },
        'MANTENIMIENTO': { class: 'secondary', icon: 'tools', text: 'Mantenimiento' }
    };
    
    return statusConfig[mesa.estado] || statusConfig['LIBRE'];
}

// Reservation Management
function isReservationExpired(reserva) {
    const now = new Date();
    const reservaDateTime = new Date(`${reserva.fecha_reserva}T${reserva.hora_reserva}`);
    const diffMinutes = (now - reservaDateTime) / (1000 * 60);
    
    return diffMinutes > 15; // 15 minutes tolerance as per requirements
}

// Report Generation
function generateSalesReport(pedidos, fechaInicio, fechaFin) {
    const filteredPedidos = pedidos.filter(pedido => {
        const fechaPedido = new Date(pedido.fecha_pedido);
        return fechaPedido >= new Date(fechaInicio) && fechaPedido <= new Date(fechaFin);
    });
    
    const totalVentas = filteredPedidos.reduce((sum, pedido) => sum + pedido.total, 0);
    const totalPedidos = filteredPedidos.length;
    const promedioVenta = totalPedidos > 0 ? totalVentas / totalPedidos : 0;
    
    return {
        totalVentas: totalVentas,
        totalPedidos: totalPedidos,
        promedioVenta: promedioVenta,
        pedidos: filteredPedidos
    };
}

// Form Validation
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^[\+]?[1-9][\d]{0,15}$/;
    return re.test(phone.replace(/\s/g, ''));
}

function validateRequired(value) {
    return value && value.trim().length > 0;
}

function validateCodigoEmpleado(codigo) {
    const re = /^[A-Z]{3}\d{3}$/; // Format: ABC123
    return re.test(codigo);
}

// Local Storage Helpers
function saveToStorage(key, data) {
    try {
        localStorage.setItem(`barmanager_${key}`, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

function loadFromStorage(key) {
    try {
        const data = localStorage.getItem(`barmanager_${key}`);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// Image Error Handling
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            this.src = 'https://via.placeholder.com/300x200/e9ecef/6c757d?text=Imagen+no+disponible';
        });
    });
});

// Keyboard Shortcuts
document.addEventListener('keydown', function(e) {
    // ESC key closes modals
    if (e.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
    
    // Ctrl+S to save (prevent default and trigger save if available)
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        const saveBtn = document.querySelector('[data-action="save"], .btn-save, button[type="submit"]');
        if (saveBtn && !saveBtn.disabled) {
            saveBtn.click();
        }
    }
});

// Performance Monitoring
if ('performance' in window) {
    window.addEventListener('load', function() {
        setTimeout(function() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData && perfData.loadEventEnd - perfData.loadEventStart > 3000) {
                console.warn('Page load time is slow:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
            }
        }, 0);
    });
}

// Export functions for global use
window.BarManagerPro = {
    // Utility functions
    showAlert,
    formatCurrency,
    formatDate,
    formatTime,
    apiRequest,
    showLoading,
    hideLoading,
    
    // Validation functions
    validateEmail,
    validatePhone,
    validateRequired,
    validateCodigoEmpleado,
    
    // Business logic functions
    checkStockAlert,
    getStockStatus,
    calculateOrderTotal,
    calculateCommission,
    getTableStatus,
    isReservationExpired,
    generateSalesReport,
    
    // Storage functions
    saveToStorage,
    loadFromStorage
};

// Initialize BarManager Pro
console.log('🍺 BarManager Pro JavaScript initialized successfully');
console.log('📊 Available functions:', Object.keys(window.BarManagerPro));