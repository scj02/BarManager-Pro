#!/usr/bin/env python3
"""
BarManager Pro - Versión con PostgreSQL y Funciones Avanzadas
Desarrollado por: Sergio Andrés Valderrama Velez, Cristian Santiago Cruz Jiménez, Julian Antonio Mejía Eslava
Docente: Christian Felipe Duarte
Septiembre 2025 - Bogotá D.C.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date, time
from decimal import Decimal
import uuid
import os
from config import config

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()

# ==================== MODELOS DE BASE DE DATOS ====================

class BaseModel(db.Model):
    __abstract__ = True
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    fecha_creacion = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    activo = db.Column(db.Boolean, nullable=False, default=True)

class Categoria(BaseModel):
    __tablename__ = 'categorias'
    
    id_categoria = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    nombre_categoria = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    
    # Relaciones
    productos = db.relationship('Producto', backref='categoria', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_categoria': self.id_categoria,
            'nombre_categoria': self.nombre_categoria,
            'descripcion': self.descripcion,
            'activo': self.activo
        }class Pr
oducto(BaseModel):
    __tablename__ = 'productos'
    
    id_producto = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    id_categoria = db.Column(db.String(36), db.ForeignKey('categorias.id_categoria'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio_compra = db.Column(db.Numeric(10, 2), nullable=False)
    precio_venta = db.Column(db.Numeric(10, 2), nullable=False)
    stock_actual = db.Column(db.Integer, nullable=False, default=0)
    stock_minimo = db.Column(db.Integer, nullable=False, default=0)
    unidad_medida = db.Column(db.String(20), nullable=False)
    codigo_barras = db.Column(db.String(50))
    imagen_url = db.Column(db.String(200))
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio_compra': float(self.precio_compra),
            'precio_venta': float(self.precio_venta),
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'unidad_medida': self.unidad_medida,
            'codigo_barras': self.codigo_barras,
            'imagen_url': self.imagen_url,
            'activo': self.activo,
            'categoria_nombre': self.categoria.nombre_categoria if self.categoria else None,
            'alerta_stock': self.stock_actual <= self.stock_minimo
        }

class Puesto(BaseModel):
    __tablename__ = 'puestos'
    
    id_puesto = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    nombre_puesto = db.Column(db.String(50), nullable=False, unique=True)
    descripcion = db.Column(db.Text)
    salario_minimo = db.Column(db.Numeric(10, 2), nullable=False)
    salario_maximo = db.Column(db.Numeric(10, 2), nullable=False)
    comision_porcentaje = db.Column(db.Numeric(5, 2), default=0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_puesto': self.id_puesto,
            'nombre_puesto': self.nombre_puesto,
            'descripcion': self.descripcion,
            'salario_minimo': float(self.salario_minimo),
            'salario_maximo': float(self.salario_maximo),
            'comision_porcentaje': float(self.comision_porcentaje),
            'activo': self.activo
        }

class Empleado(UserMixin, BaseModel):
    __tablename__ = 'empleados'
    
    id_empleado = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    id_puesto = db.Column(db.String(36), db.ForeignKey('puestos.id_puesto'), nullable=False)
    codigo_empleado = db.Column(db.String(20), nullable=False, unique=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(20))
    fecha_ingreso = db.Column(db.Date, nullable=False)
    salario_base = db.Column(db.Numeric(10, 2), nullable=False)
    password_hash = db.Column(db.String(128))
    puntos_fidelidad = db.Column(db.Integer, default=0)
    
    # Relaciones
    puesto = db.relationship('Puesto', backref='empleados')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_empleado': self.id_empleado,
            'codigo_empleado': self.codigo_empleado,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'telefono': self.telefono,
            'fecha_ingreso': self.fecha_ingreso.isoformat() if self.fecha_ingreso else None,
            'salario_base': float(self.salario_base),
            'puesto': self.puesto.nombre_puesto if self.puesto else None,
            'activo': self.activo
        }

class Cliente(BaseModel):
    __tablename__ = 'clientes'
    
    id_cliente = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    fecha_registro = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    puntos_fidelidad = db.Column(db.Integer, default=0)
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_cliente': self.id_cliente,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'nombre_completo': self.nombre_completo,
            'telefono': self.telefono,
            'email': self.email,
            'fecha_nacimiento': self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None,
            'puntos_fidelidad': self.puntos_fidelidad,
            'activo': self.activo
        }class
 Mesa(BaseModel):
    __tablename__ = 'mesas'
    
    id_mesa = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    numero_mesa = db.Column(db.String(10), nullable=False, unique=True)
    capacidad = db.Column(db.Integer, nullable=False)
    ubicacion = db.Column(db.String(50))
    estado = db.Column(db.String(20), nullable=False, default='LIBRE')  # LIBRE, OCUPADA, RESERVADA, MANTENIMIENTO
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_mesa': self.id_mesa,
            'numero_mesa': self.numero_mesa,
            'capacidad': self.capacidad,
            'ubicacion': self.ubicacion,
            'estado': self.estado,
            'activo': self.activo
        }

class Reserva(BaseModel):
    __tablename__ = 'reservas'
    
    id_reserva = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    id_cliente = db.Column(db.String(36), db.ForeignKey('clientes.id_cliente'))
    id_mesa = db.Column(db.String(36), db.ForeignKey('mesas.id_mesa'), nullable=False)
    fecha_reserva = db.Column(db.DateTime, nullable=False)
    hora_reserva = db.Column(db.Time, nullable=False)
    numero_personas = db.Column(db.Integer, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='PENDIENTE')  # PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA
    observaciones = db.Column(db.Text)
    
    # Relaciones
    cliente = db.relationship('Cliente', backref='reservas')
    mesa = db.relationship('Mesa', backref='reservas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_reserva': self.id_reserva,
            'fecha_reserva': self.fecha_reserva.isoformat() if self.fecha_reserva else None,
            'hora_reserva': self.hora_reserva.strftime('%H:%M') if self.hora_reserva else None,
            'numero_personas': self.numero_personas,
            'estado': self.estado,
            'observaciones': self.observaciones,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else 'Cliente Anónimo',
            'mesa_numero': self.mesa.numero_mesa if self.mesa else None
        }

class Pedido(BaseModel):
    __tablename__ = 'pedidos'
    
    id_pedido = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    id_empleado = db.Column(db.String(36), db.ForeignKey('empleados.id_empleado'), nullable=False)
    id_cliente = db.Column(db.String(36), db.ForeignKey('clientes.id_cliente'))
    id_mesa = db.Column(db.String(36), db.ForeignKey('mesas.id_mesa'), nullable=False)
    numero_pedido = db.Column(db.String(20), nullable=False, unique=True)
    fecha_pedido = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    impuestos = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    descuentos = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    estado = db.Column(db.String(20), nullable=False, default='PENDIENTE')  # PENDIENTE, EN_PREPARACION, LISTO, ENTREGADO, PAGADO, CANCELADO
    observaciones = db.Column(db.Text)
    
    # Relaciones
    empleado = db.relationship('Empleado', backref='pedidos')
    cliente = db.relationship('Cliente', backref='pedidos')
    mesa = db.relationship('Mesa', backref='pedidos')
    detalles = db.relationship('DetallePedido', backref='pedido', lazy=True, cascade='all, delete-orphan')
    pagos = db.relationship('Pago', backref='pedido', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_pedido': self.id_pedido,
            'numero_pedido': self.numero_pedido,
            'fecha_pedido': self.fecha_pedido.isoformat() if self.fecha_pedido else None,
            'subtotal': float(self.subtotal),
            'impuestos': float(self.impuestos),
            'descuentos': float(self.descuentos or 0),
            'total': float(self.total),
            'estado': self.estado,
            'observaciones': self.observaciones,
            'empleado_nombre': self.empleado.nombre_completo if self.empleado else None,
            'cliente_nombre': self.cliente.nombre_completo if self.cliente else 'Cliente Anónimo',
            'mesa_numero': self.mesa.numero_mesa if self.mesa else None

        }
