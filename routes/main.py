from flask import Blueprint, render_template, request, jsonify
from models.models import MenuItem
from config import Config

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Página principal del bar"""
    return render_template('index.html')

@main_bp.route('/menu')
def menu():
    """Página del menú"""
    try:
        # Obtener todas las categorías disponibles
        categories = ['bebidas', 'aperitivos', 'principales', 'postres']
        
        # Obtener elementos del menú por categoría
        menu_by_category = {}
        for category in categories:
            items = MenuItem.query.filter_by(category=category, available=True).all()
            if items:  # Solo incluir categorías que tienen elementos
                menu_by_category[category] = [item.to_dict() for item in items]
        
        return render_template('menu.html', menu_by_category=menu_by_category)
    except Exception as e:
        return render_template('menu.html', menu_by_category={}, error=str(e))

@main_bp.route('/reservations')
def reservations():
    """Página de reservas"""
    return render_template('reservations.html')

@main_bp.route('/contact')
def contact():
    """Página de contacto"""
    return render_template('contact.html')

@main_bp.route('/about')
def about():
    """Página acerca del bar"""
    return render_template('about.html')

# Error handlers
@main_bp.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500