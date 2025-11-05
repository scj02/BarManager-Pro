#!/usr/bin/env python3
"""
BarManager Pro - Sistema de Gestión Integral para Bares
Desarrollado por: Sergio Andrés Valderrama Velez, Cristian Santiago Cruz Jiménez, Julian Antonio Mejía Eslava
Docente: Christian Felipe Duarte
Noviembre 2025 - Bogotá D.C.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from datetime import datetime, date, time
import uuid

# ==================== CONFIGURACIÓN ====================

class Config:
    SECRET_KEY = 'barmanager-pro-secret-key-2025'
    BAR_NAME = 'BarManager Pro'
    BAR_ADDRESS = 'Av. Empresarial 456, Bogotá D.C.'
    BAR_PHONE = '+57 301 456 7890'
    BAR_EMAIL = 'info@barmanagerpro.com'
    BAR_SLOGAN = 'Sistema de Gestión Integral para Bares'

# ==================== DATOS EN MEMORIA ====================

# Categorías de productos
CATEGORIAS = [
    {'id': '1', 'nombre_categoria': 'Bebidas Alcohólicas', 'descripcion': 'Cervezas, vinos, licores y cócteles', 'activo': True},
    {'id': '2', 'nombre_categoria': 'Bebidas No Alcohólicas', 'descripcion': 'Refrescos, jugos, aguas y cafés', 'activo': True},
    {'id': '3', 'nombre_categoria': 'Comida Rápida', 'descripcion': 'Hamburguesas, sándwiches y snacks', 'activo': True},
    {'id': '4', 'nombre_categoria': 'Platos Principales', 'descripcion': 'Comida tradicional colombiana', 'activo': True},
    {'id': '5', 'nombre_categoria': 'Postres', 'descripcion': 'Dulces y postres tradicionales', 'activo': True}
]

# Productos del bar
PRODUCTOS = [
    {'id': '1', 'id_categoria': '1', 'nombre': 'Cerveza Corona', 'descripcion': 'Cerveza clara mexicana 355ml', 
     'precio_compra': 2500, 'precio_venta': 8000, 'stock_actual': 150, 'stock_minimo': 20, 
     'unidad_medida': 'Botella', 'activo': True, 'categoria_nombre': 'Bebidas Alcohólicas',
     'imagen_url': 'https://images.unsplash.com/photo-1544145945-f90425340c7e?ixlib=rb-4.0.3'},
    
    {'id': '2', 'id_categoria': '1', 'nombre': 'Aguardiente Antioqueño', 'descripcion': 'Aguardiente tradicional colombiano', 
     'precio_compra': 15000, 'precio_venta': 35000, 'stock_actual': 50, 'stock_minimo': 10, 
     'unidad_medida': 'Botella', 'activo': True, 'categoria_nombre': 'Bebidas Alcohólicas',
     'imagen_url': 'https://images.unsplash.com/photo-1551538827-9c037cb4f32a?ixlib=rb-4.0.3'},
    
    {'id': '3', 'id_categoria': '4', 'nombre': 'Bandeja Paisa', 'descripcion': 'Plato típico colombiano completo', 
     'precio_compra': 12000, 'precio_venta': 25000, 'stock_actual': 30, 'stock_minimo': 5, 
     'unidad_medida': 'Porción', 'activo': True, 'categoria_nombre': 'Platos Principales',
     'imagen_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?ixlib=rb-4.0.3'},
    
    {'id': '4', 'id_categoria': '4', 'nombre': 'Sancocho de Gallina', 'descripcion': 'Sopa tradicional con gallina criolla', 
     'precio_compra': 8000, 'precio_venta': 20000, 'stock_actual': 25, 'stock_minimo': 5, 
     'unidad_medida': 'Porción', 'activo': True, 'categoria_nombre': 'Platos Principales',
     'imagen_url': 'https://images.unsplash.com/photo-1547592180-85f173990554?ixlib=rb-4.0.3'},
    
    {'id': '5', 'id_categoria': '3', 'nombre': 'Hamburguesa Clásica', 'descripcion': 'Hamburguesa con carne, queso y vegetales', 
     'precio_compra': 6000, 'precio_venta': 15000, 'stock_actual': 40, 'stock_minimo': 10, 
     'unidad_medida': 'Unidad', 'activo': True, 'categoria_nombre': 'Comida Rápida',
     'imagen_url': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?ixlib=rb-4.0.3'},
    
    {'id': '6', 'id_categoria': '5', 'nombre': 'Tres Leches', 'descripcion': 'Torta tres leches casera', 
     'precio_compra': 3000, 'precio_venta': 8000, 'stock_actual': 20, 'stock_minimo': 5, 
     'unidad_medida': 'Porción', 'activo': True, 'categoria_nombre': 'Postres',
     'imagen_url': 'https://images.unsplash.com/photo-1551024506-0bccd828d307?ixlib=rb-4.0.3'},
    
    {'id': '7', 'id_categoria': '2', 'nombre': 'Limonada de Coco', 'descripcion': 'Refrescante bebida con coco natural', 
     'precio_compra': 2000, 'precio_venta': 6000, 'stock_actual': 8, 'stock_minimo': 15, 
     'unidad_medida': 'Vaso', 'activo': True, 'categoria_nombre': 'Bebidas No Alcohólicas',
     'imagen_url': 'https://images.unsplash.com/photo-1546171753-97d7676e4602?ixlib=rb-4.0.3'},
    
    {'id': '8', 'id_categoria': '3', 'nombre': 'Empanadas Vallenas', 'descripcion': 'Empanadas tradicionales de carne y pollo', 
     'precio_compra': 1000, 'precio_venta': 3000, 'stock_actual': 3, 'stock_minimo': 20, 
     'unidad_medida': 'Unidad', 'activo': True, 'categoria_nombre': 'Comida Rápida',
     'imagen_url': 'https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?ixlib=rb-4.0.3'}
]

# Puestos de trabajo
PUESTOS = [
    {'id': '1', 'nombre_puesto': 'Administrador', 'descripcion': 'Gestión general del bar', 
     'salario_minimo': 30000, 'salario_maximo': 50000, 'comision_porcentaje': 0, 'activo': True},
    {'id': '2', 'nombre_puesto': 'Mesero', 'descripcion': 'Atención a mesas y clientes', 
     'salario_minimo': 15000, 'salario_maximo': 25000, 'comision_porcentaje': 5, 'activo': True},
    {'id': '3', 'nombre_puesto': 'Bartender', 'descripcion': 'Preparación de bebidas', 
     'salario_minimo': 18000, 'salario_maximo': 30000, 'comision_porcentaje': 3, 'activo': True},
    {'id': '4', 'nombre_puesto': 'Cajero', 'descripcion': 'Manejo de pagos y facturación', 
     'salario_minimo': 16000, 'salario_maximo': 22000, 'comision_porcentaje': 2, 'activo': True}
]

# Empleados
EMPLEADOS = [
    {'id': '1', 'id_puesto': '1', 'codigo_empleado': 'ADMIN001', 'nombre': 'Administrador', 'apellido': 'Sistema',
     'email': 'admin@barmanagerpro.com', 'telefono': '+57-301-456-7890', 'fecha_ingreso': '2025-01-01',
     'salario_base': 35000, 'activo': True, 'puesto': 'Administrador', 'password': 'admin123'},
    {'id': '2', 'id_puesto': '2', 'codigo_empleado': 'MES001', 'nombre': 'Carlos', 'apellido': 'Rodríguez',
     'email': 'carlos@barmanagerpro.com', 'telefono': '+57-301-111-2222', 'fecha_ingreso': '2025-02-01',
     'salario_base': 20000, 'activo': True, 'puesto': 'Mesero', 'password': 'mesero123'},
    {'id': '3', 'id_puesto': '3', 'codigo_empleado': 'BAR001', 'nombre': 'María', 'apellido': 'González',
     'email': 'maria@barmanagerpro.com', 'telefono': '+57-301-333-4444', 'fecha_ingreso': '2025-02-15',
     'salario_base': 25000, 'activo': True, 'puesto': 'Bartender', 'password': 'bartender123'}
]

# Mesas del bar (15 mesas según especificaciones)
MESAS = []
for i in range(1, 16):
    MESAS.append({
        'id': str(i),
        'numero_mesa': f'M{i:03d}',
        'capacidad': 4 if i <= 10 else 6 if i <= 13 else 8,
        'ubicacion': 'Interior' if i <= 8 else 'Terraza' if i <= 12 else 'VIP',
        'estado': 'LIBRE',
        'activo': True
    })

# Clientes
CLIENTES = [
    {'id': '1', 'nombre': 'Juan', 'apellido': 'Pérez', 'telefono': '+57-300-111-1111', 
     'email': 'juan.perez@email.com', 'fecha_nacimiento': '1985-05-15', 'fecha_registro': '2024-01-10',
     'puntos_fidelidad': 750, 'activo': True},
    {'id': '2', 'nombre': 'María', 'apellido': 'López', 'telefono': '+57-300-222-2222', 
     'email': 'maria.lopez@email.com', 'fecha_nacimiento': '1990-08-22', 'fecha_registro': '2024-02-15',
     'puntos_fidelidad': 320, 'activo': True},
    {'id': '3', 'nombre': 'Carlos', 'apellido': 'Martínez', 'telefono': '+57-300-333-3333', 
     'email': 'carlos.martinez@email.com', 'fecha_nacimiento': '1988-12-10', 'fecha_registro': '2025-01-01',
     'puntos_fidelidad': 85, 'activo': True}
]

# Reservas
RESERVAS = [
    {'id': '1', 'id_cliente': '1', 'id_mesa': '5', 'fecha_reserva': '2025-11-05', 'hora_reserva': '19:30',
     'numero_personas': 4, 'estado': 'PENDIENTE', 'observaciones': 'Mesa cerca de la ventana',
     'cliente_nombre': 'Juan Pérez', 'mesa_numero': 'M005', 'fecha_creacion': '2025-11-03'},
    {'id': '2', 'id_cliente': '2', 'id_mesa': '8', 'fecha_reserva': '2025-11-06', 'hora_reserva': '20:00',
     'numero_personas': 2, 'estado': 'CONFIRMADA', 'observaciones': 'Celebración de aniversario',
     'cliente_nombre': 'María López', 'mesa_numero': 'M008', 'fecha_creacion': '2025-11-02'}
]

# Pedidos
PEDIDOS = [
    {'id': '1', 'numero_pedido': 'PED-20251103-001', 'id_empleado': '2', 'id_cliente': '1', 'id_mesa': '3',
     'fecha_pedido': '2025-11-03 14:30:00', 'subtotal': 33000, 'impuestos': 5280, 'descuentos': 0,
     'total': 38280, 'estado': 'ENTREGADO', 'observaciones': 'Sin cebolla en la hamburguesa',
     'empleado_nombre': 'Carlos Rodríguez', 'cliente_nombre': 'Juan Pérez', 'mesa_numero': 'M003'},
    {'id': '2', 'numero_pedido': 'PED-20251103-002', 'id_empleado': '3', 'id_cliente': '2', 'id_mesa': '7',
     'fecha_pedido': '2025-11-03 15:45:00', 'subtotal': 45000, 'impuestos': 7200, 'descuentos': 2000,
     'total': 50200, 'estado': 'EN_PREPARACION', 'observaciones': 'Extra salsa',
     'empleado_nombre': 'María González', 'cliente_nombre': 'María López', 'mesa_numero': 'M007'}
]

# Proveedores
PROVEEDORES = [
    {'id': '1', 'nombre_empresa': 'Distribuidora de Bebidas SA', 'contacto': 'Roberto Martínez',
     'telefono': '+57-555-111-2222', 'email': 'ventas@distribuidora.com', 
     'direccion': 'Av. Industrial 123, Bogotá', 'activo': True},
    {'id': '2', 'nombre_empresa': 'Carnes y Embutidos El Ganadero', 'contacto': 'María González',
     'telefono': '+57-555-333-4444', 'email': 'pedidos@elganadero.com',
     'direccion': 'Calle 45 #12-34, Bogotá', 'activo': True}
]

# Mensajes de contacto
MENSAJES_CONTACTO = [
    {'id': '1', 'nombre': 'Ana García', 'email': 'ana@email.com', 'asunto': 'Consulta sobre eventos',
     'mensaje': 'Quisiera saber si manejan eventos privados para 50 personas', 'is_read': False,
     'fecha_creacion': '2025-11-03 10:30:00'},
    {'id': '2', 'nombre': 'Pedro Ruiz', 'email': 'pedro@email.com', 'asunto': 'Felicitaciones',
     'mensaje': 'Excelente servicio y comida. Muy recomendado!', 'is_read': True,
     'fecha_creacion': '2025-11-02 16:20:00'}
]

# Contadores globales
RESERVAS_COUNTER = len(RESERVAS) + 1
PEDIDOS_COUNTER = len(PEDIDOS) + 1
MENSAJES_COUNTER = len(MENSAJES_CONTACTO) + 1

# ==================== APLICACIÓN FLASK ====================

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Decorador para requerir login
    def login_required(f):
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                flash('Por favor inicia sesión para acceder a esta página.', 'warning')
                return redirect(url_for('admin_login'))
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    
    # ==================== RUTAS PÚBLICAS ====================
    
    @app.route('/')
    def index():
        return render_template('barmanager/index.html')
    
    @app.route('/menu')
    def menu():
        return render_template('barmanager/menu.html')
    
    @app.route('/reservas')
    def reservas():
        return render_template('barmanager/reservas.html')
    
    @app.route('/contacto')
    def contacto():
        return render_template('barmanager/contacto.html')
    
    @app.route('/nosotros')
    def nosotros():
        return render_template('barmanager/nosotros.html')
    
    # ==================== API ENDPOINTS ====================
    
    @app.route('/api/productos', methods=['GET'])
    def get_productos():
        categoria = request.args.get('categoria')
        productos = PRODUCTOS.copy()
        
        if categoria:
            productos = [p for p in productos if p['categoria_nombre'] == categoria]
        
        # Agregar alerta de stock
        for producto in productos:
            producto['alerta_stock'] = producto['stock_actual'] <= producto['stock_minimo']
        
        return jsonify({'success': True, 'data': productos})
    
    @app.route('/api/categorias', methods=['GET'])
    def get_categorias():
        return jsonify({'success': True, 'data': CATEGORIAS})
    
    @app.route('/api/mesas/disponibles', methods=['GET'])
    def get_mesas_disponibles():
        personas = request.args.get('personas', type=int, default=2)
        mesas_disponibles = [m for m in MESAS if m['estado'] == 'LIBRE' and m['capacidad'] >= personas]
        
        return jsonify({
            'success': True,
            'data': mesas_disponibles,
            'disponibles': len(mesas_disponibles) > 0
        })
    
    @app.route('/api/reservas', methods=['POST'])
    def crear_reserva():
        global RESERVAS_COUNTER
        try:
            data = request.get_json()
            
            # Buscar mesa
            mesa = next((m for m in MESAS if m['numero_mesa'] == data['mesa']), None)
            if not mesa:
                return jsonify({'success': False, 'error': 'Mesa no encontrada'}), 400
            
            # Crear reserva
            nueva_reserva = {
                'id': str(RESERVAS_COUNTER),
                'id_cliente': None,
                'id_mesa': mesa['id'],
                'fecha_reserva': data['fecha'],
                'hora_reserva': data['hora'],
                'numero_personas': data['personas'],
                'estado': 'PENDIENTE',
                'observaciones': data.get('observaciones', ''),
                'cliente_nombre': data['nombre'],
                'mesa_numero': mesa['numero_mesa'],
                'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            RESERVAS.append(nueva_reserva)
            RESERVAS_COUNTER += 1
            
            return jsonify({
                'success': True,
                'data': nueva_reserva,
                'message': 'Reserva creada exitosamente'
            }), 201
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    @app.route('/api/contacto', methods=['POST'])
    def enviar_contacto():
        global MENSAJES_COUNTER
        try:
            data = request.get_json()
            
            nuevo_mensaje = {
                'id': str(MENSAJES_COUNTER),
                'nombre': data['nombre'],
                'email': data['email'],
                'asunto': data['asunto'],
                'mensaje': data['mensaje'],
                'is_read': False,
                'fecha_creacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            MENSAJES_CONTACTO.append(nuevo_mensaje)
            MENSAJES_COUNTER += 1
            
            return jsonify({
                'success': True,
                'message': 'Mensaje enviado correctamente'
            }), 201
            
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    
    # ==================== PANEL ADMINISTRATIVO ====================
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if session.get('logged_in'):
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            codigo = request.form['codigo_empleado']
            password = request.form['password']
            
            empleado = next((e for e in EMPLEADOS if e['codigo_empleado'] == codigo and e['password'] == password), None)
            
            if empleado:
                session['logged_in'] = True
                session['empleado_id'] = empleado['id']
                session['empleado_nombre'] = f"{empleado['nombre']} {empleado['apellido']}"
                flash('Inicio de sesión exitoso', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Código de empleado o contraseña incorrectos', 'error')
        
        return render_template('barmanager/admin/login.html')
    
    @app.route('/admin/logout')
    def admin_logout():
        session.clear()
        flash('Sesión cerrada correctamente', 'info')
        return redirect(url_for('index'))
    
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        # Calcular estadísticas
        total_productos = len([p for p in PRODUCTOS if p['activo']])
        productos_bajo_stock = len([p for p in PRODUCTOS if p['activo'] and p['stock_actual'] <= p['stock_minimo']])
        reservas_pendientes = len([r for r in RESERVAS if r['estado'] == 'PENDIENTE'])
        pedidos_activos = len([p for p in PEDIDOS if p['estado'] in ['PENDIENTE', 'EN_PREPARACION']])
        mensajes_no_leidos = len([m for m in MENSAJES_CONTACTO if not m['is_read']])
        
        return render_template('barmanager/admin/dashboard.html',
                             total_productos=total_productos,
                             productos_bajo_stock=productos_bajo_stock,
                             reservas_pendientes=reservas_pendientes,
                             pedidos_activos=pedidos_activos,
                             mensajes_no_leidos=mensajes_no_leidos,
                             reservas_recientes=RESERVAS[-5:],
                             pedidos_recientes=PEDIDOS[-5:])
    
    @app.route('/admin/inventario')
    @login_required
    def admin_inventario():
        return render_template('barmanager/admin/inventario.html',
                             productos=PRODUCTOS,
                             categorias=CATEGORIAS)
    
    @app.route('/admin/ventas')
    @login_required
    def admin_ventas():
        return render_template('barmanager/admin/ventas.html',
                             pedidos=PEDIDOS,
                             mesas=MESAS,
                             clientes=CLIENTES,
                             productos=PRODUCTOS,
                             categorias=CATEGORIAS)
    
    @app.route('/admin/personal')
    @login_required
    def admin_personal():
        return render_template('barmanager/admin/personal.html',
                             empleados=EMPLEADOS,
                             puestos=PUESTOS)
    
    @app.route('/admin/clientes')
    @login_required
    def admin_clientes():
        return render_template('barmanager/admin/clientes.html',
                             clientes=CLIENTES)
    
    @app.route('/admin/reservas')
    @login_required
    def admin_reservas():
        return render_template('barmanager/admin/reservas.html',
                             reservas=RESERVAS,
                             mesas=MESAS,
                             clientes=CLIENTES)
    
    @app.route('/admin/reportes')
    @login_required
    def admin_reportes():
        return render_template('barmanager/admin/reportes.html')
    
    @app.route('/admin/proveedores')
    @login_required
    def admin_proveedores():
        return render_template('barmanager/admin/proveedores.html',
                             proveedores=PROVEEDORES)
    
    @app.route('/admin/mensajes')
    @login_required
    def admin_mensajes():
        return render_template('barmanager/admin/mensajes.html',
                             mensajes=MENSAJES_CONTACTO)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('barmanager/errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('barmanager/errors/500.html'), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    print("🍺 BarManager Pro - Sistema de Gestión Integral para Bares")
    print("=" * 70)
    print("Desarrollado por:")
    print("  • Sergio Valderrama")
    print("  • Cristian Cruz") 
    print("  • Julian Antonio Mejía Eslava")
    print("")
    print("Docente: Christian Felipe Duarte")
    print("Septiembre 2025 - Bogotá D.C.")
    print("=" * 70)
    print("✅ Aplicación iniciada en: http://localhost:5000")
    print("👤 Panel Administrativo: http://localhost:5000/admin/login")
    print("")
    print("🔑 Credenciales de acceso:")
    print("   • Administrador: ADMIN001 / admin123")
    print("   • Mesero: MES001 / mesero123")
    print("   • Bartender: BAR001 / bartender123")
    print("")
    print("📊 Datos incluidos:")
    print(f"   • {len(PRODUCTOS)} productos en inventario")
    print(f"   • {len(MESAS)} mesas disponibles")
    print(f"   • {len(EMPLEADOS)} empleados registrados")
    print(f"   • {len(RESERVAS)} reservas de ejemplo")
    print(f"   • {len(PEDIDOS)} pedidos de muestra")
    print("=" * 70)
    

    app.run(debug=True, host='0.0.0.0', port=5000)
