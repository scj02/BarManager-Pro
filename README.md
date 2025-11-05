# BarManager Pro

**Sistema de Gestión Integral para Bares**

Desarrollado por:
- **Sergio Valderrama**
- **Cristian Cruz**
- **Julian Antonio Mejía Eslava**

**Docente:** Christian Felipe Duarte  
**Fecha:** Septiembre 2025 - Bogotá D.C.

---

## 🍺 Descripción

BarManager Pro es un sistema integral de gestión diseñado para automatizar y optimizar todas las operaciones de bares y restaurantes. Mejora la eficiencia operativa, el control financiero y la experiencia del cliente.

## 📊 Módulos del Sistema

### ✅ **Gestión de Inventario**
- Control completo de productos con categorías
- Alertas automáticas de stock bajo
- Gestión de proveedores
- Historial de movimientos de inventario

### ✅ **Sistema de Ventas**
- Sistema de pedidos por mesa
- Generación de facturas
- Aplicación de descuentos y promociones
- Control de estados de pedidos

### ✅ **Administración de Personal**
- Registro y gestión de empleados
- Control de turnos y horarios
- Cálculo de comisiones por rol
- Sistema de permisos y autenticación

### ✅ **Base de Datos de Clientes**
- Registro completo de clientes
- Historial de compras
- Gestión de información personal

### ✅ **Gestión de Mesas y Reservas**
- Control de mesas (15 mesas)
- Sistema de reservas online
- Liberación automática (15 minutos)
- Verificación de disponibilidad

### ✅ **Reportes Analíticos**
- Reportes de ventas por período
- Análisis de desempeño de empleados
- Estadísticas del negocio

---

## 🚀 Instalación y Ejecución

### **Requisitos**
- Python 3.8+
- Flask 2.0+

### **Instalación**
```bash
# 1. Instalar Flask
pip install Flask

# 2. Ejecutar la aplicación
python app.py
```

### **Acceso al Sistema**
- **Página Web:** `http://localhost:5000`
- **Panel Admin:** `http://localhost:5000/admin/login`

### **Credenciales de Acceso**
| Rol | Código | Contraseña |
|-----|--------|------------|
| Administrador | `ADMIN001` | `admin123` |
| Mesero | `MES001` | `mesero123` |
| Bartender | `BAR001` | `bartender123` |

---

## 🌐 Páginas Disponibles

| Página | URL | Descripción |
|--------|-----|-------------|
| Inicio | `/` | Página principal del sistema |
| Menú | `/menu` | Catálogo de productos |
| Reservas | `/reservas` | Sistema de reservas |
| Contacto | `/contacto` | Formulario de contacto |
| Nosotros | `/nosotros` | Información del proyecto |
| Admin | `/admin/login` | Panel administrativo |

---

## 📋 Datos de Demostración

El sistema incluye datos de ejemplo para demostración:

- **8 productos** en inventario (con alertas de stock)
- **15 mesas** disponibles (M001-M015)
- **3 empleados** con diferentes roles
- **4 puestos** de trabajo definidos
- **3 clientes** registrados
- **2 reservas** de ejemplo
- **2 pedidos** de muestra
- **2 proveedores** configurados

---

## 🎯 Características Técnicas

### **Tecnologías Utilizadas**
- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, JavaScript
- **Estilos:** Bootstrap 5 + CSS personalizado
- **Iconos:** Font Awesome 6
- **Base de Datos:** Datos en memoria (demo)

### **Funcionalidades Destacadas**
- ✅ Diseño responsive (móviles y desktop)
- ✅ Alertas automáticas de stock bajo
- ✅ Sistema de autenticación por roles
- ✅ Verificación de disponibilidad en tiempo real
- ✅ Cálculo automático de totales e impuestos
- ✅ Interfaz administrativa completa
- ✅ Formularios con validación

### **Supuestos del Sistema**
- 10-15 mesas gestionadas
- 50-100 clientes diarios
- 3-8 empleados por turno
- 30-100 productos en inventario
- 12 horas de operación diaria
- Alertas de stock al 10% del mínimo
- Liberación automática de reservas (15 min)

---

## 📱 Capturas de Pantalla

### Panel Administrativo
- Dashboard con estadísticas en tiempo real
- Gestión completa de inventario
- Administración de reservas y pedidos
- Control de personal y reportes

### Página Pública
- Menú interactivo con filtros
- Sistema de reservas online
- Formulario de contacto
- Información del bar

---

## 🔧 Estructura del Proyecto

```
BarManager Pro/
├── app.py                          # Aplicación principal
├── config.py                       # Configuración
├── requirements.txt                # Dependencias
├── templates/barmanager/           # Templates HTML
│   ├── base.html                   # Template base
│   ├── index.html                  # Página principal
│   ├── menu.html                   # Menú
│   ├── reservas.html               # Reservas
│   ├── contacto.html               # Contacto
│   ├── nosotros.html               # Nosotros
│   └── admin/                      # Panel administrativo
│       ├── base.html               # Base admin
│       ├── login.html              # Login
│       └── dashboard.html          # Dashboard
├── static/                         # Archivos estáticos
│   ├── css/barmanager.css          # Estilos personalizados
│   └── js/barmanager.js            # JavaScript
└── README.md                       # Este archivo
```

---

## 🎓 Información Académica

**Proyecto desarrollado como parte del programa académico:**

- **Institución:** Universidad
- **Docente:** Christian Felipe Duarte
- **Estudiantes:** Sergio Valderrama, Cristian Cruz, Julian Antonio Mejía Eslava
- **Período:** Septiembre 2025
- **Ubicación:** Bogotá D.C., Colombia

### **Objetivos Académicos**
1. Aplicar conceptos de desarrollo web full-stack
2. Implementar sistemas de gestión empresarial
3. Utilizar tecnologías modernas de desarrollo
4. Crear soluciones prácticas para el sector gastronómico

---

## 📞 Soporte

Para consultas sobre el proyecto:
- **Email:** info@barmanagerpro.com
- **Teléfono:** +57 301 456 7890

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos.

**© 2025 BarManager Pro - Todos los derechos reservados**

---

**¡Gracias por usar BarManager Pro!** 🍺