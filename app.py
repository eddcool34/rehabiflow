from flask import Flask, jsonify, render_template, send_from_directory, session, redirect, url_for, request
from flask_cors import CORS
from config import Config
from database import init_db, db
import os

# ============================================
# CONFIGURAR FLASK CON CARPETAS DE FRONTEND
# ============================================
app = Flask(__name__,
    template_folder='frontend',
    static_folder='frontend'
)

app.config.from_object(Config)

# ============================================
# CONFIGURACIÓN DE SESIÓN
# ============================================
app.secret_key = os.getenv('SECRET_KEY', 'rehabiflow-secret-key-2025')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 24 horas

# ============================================
# CORS - Permitir conexiones externas
# ============================================
CORS(app, origins=['http://127.0.0.1:5500', 'http://localhost:5500', '*'])

# ============================================
# INICIALIZAR BASE DE DATOS
# ============================================
init_db(app)

# ============================================
# IMPORTAR MIDDLEWARE
# ============================================
from middleware.auth import login_required

# ============================================
# IMPORTAR RUTAS
# ============================================
from routes.administracion import admin_bp
from routes.pacientes import pacientes_bp
from routes.agenda import agenda_bp
from routes.ventas import ventas_bp
from routes.reportes import reportes_bp
from routes.auth import auth_bp

# ============================================
# REGISTRAR BLUEPRINTS
# ============================================
app.register_blueprint(admin_bp, url_prefix='/api/administracion')
app.register_blueprint(pacientes_bp, url_prefix='/api/pacientes')
app.register_blueprint(agenda_bp, url_prefix='/api/agenda')
app.register_blueprint(ventas_bp, url_prefix='/api/ventas')
app.register_blueprint(reportes_bp, url_prefix='/api/reportes')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# ============================================
# RUTA PRINCIPAL - PROTEGIDA
# ============================================
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# ============================================
# RUTAS DEL FRONTEND - PROTEGIDAS
# ============================================
@app.route('/admin.html')
@login_required
def admin_page():
    return render_template('admin.html')

@app.route('/pacientes.html')
@login_required
def pacientes_page():
    return render_template('pacientes.html')

@app.route('/agenda.html')
@login_required
def agenda_page():
    return render_template('agenda.html')

@app.route('/ventas.html')
@login_required
def ventas_page():
    return render_template('ventas.html')

@app.route('/reportes.html')
@login_required
def reportes_page():
    return render_template('reportes.html')

@app.route('/configuracion.html')
@login_required
def configuracion_page():
    return render_template('configuracion.html')

# ============================================
# RUTAS PARA ARCHIVOS ESTÁTICOS (CSS, JS, IMÁGENES)
# ============================================
@app.route('/<path:path>')
def static_files(path):
    # Si la ruta empieza con api/, no interferir
    if path.startswith('api/'):
        return jsonify({'error': 'Ruta no encontrada'}), 404
    
    # Permitir acceso a login.html sin autenticación
    if path == 'login.html':
        return send_from_directory('frontend', path)
    
    # Permitir acceso a archivos estáticos
    if path.startswith('css/') or path.startswith('js/') or path.startswith('img/') or path.startswith('assets/'):
        return send_from_directory('frontend', path)
    
    # Verificar autenticación para cualquier otro archivo HTML
    if path.endswith('.html') and path != 'login.html':
        if 'user_id' not in session:
            return redirect('/login.html')
    
    return send_from_directory('frontend', path)

# ============================================
# RUTAS DE LA API (NO REQUIEREN AUTENTICACIÓN)
# ============================================
@app.route('/api/health')
def health():
    return jsonify({
        'status': 'OK',
        'version': '1.0.0',
        'database': 'connected'
    })

# ============================================
# MANEJO DE ERRORES
# ============================================
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Ruta no encontrada'}), 404
    return redirect('/login.html')

@app.errorhandler(500)
def server_error(e):
    if request.path.startswith('/api/'):
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500
    return redirect('/login.html')

# ============================================
# INICIAR SERVIDOR
# ============================================
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',      # Escucha en todas las interfaces (WiFi)
        port=5000,           # Puerto 5000
        debug=True
    )