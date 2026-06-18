from database import db
from datetime import datetime

# ============================================
# MODELO: Servicio
# ============================================
class Servicio(db.Model):
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    duracion_minutos = db.Column(db.Integer, default=30)
    precio = db.Column(db.Float, nullable=False)
    costo = db.Column(db.Float, default=0)
    requiere_inventario = db.Column(db.Boolean, default=False)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    citas = db.relationship('Cita', backref='servicio', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'duracion_minutos': self.duracion_minutos,
            'precio': self.precio,
            'costo': self.costo,
            'requiere_inventario': self.requiere_inventario,
            'activo': self.activo
        }

# ============================================
# MODELO: Profesional
# ============================================
class Profesional(db.Model):
    __tablename__ = 'profesionales'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100))
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    comision_porcentaje = db.Column(db.Float, default=0)
    horario_laboral = db.Column(db.JSON)
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    citas = db.relationship('Cita', backref='profesional', lazy=True)
    ventas = db.relationship('Venta', backref='profesional', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'email': self.email,
            'telefono': self.telefono,
            'comision_porcentaje': self.comision_porcentaje,
            'horario_laboral': self.horario_laboral,
            'activo': self.activo
        }

# ============================================
# MODELO: Paciente
# ============================================
class Paciente(db.Model):
    __tablename__ = 'pacientes'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_completo = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20), nullable=False)
    telefono_alternativo = db.Column(db.String(20))
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.String(20), default='no_especificado')
    direccion = db.Column(db.Text)
    ocupacion = db.Column(db.String(100))
    alergias = db.Column(db.Text)
    condiciones_medicas = db.Column(db.Text)
    medicamentos_actuales = db.Column(db.Text)
    seguro_medico = db.Column(db.String(100))
    numero_seguro = db.Column(db.String(50))
    total_gastado = db.Column(db.Float, default=0)
    saldo_pendiente = db.Column(db.Float, default=0)
    activo = db.Column(db.Boolean, default=True)
    etiquetas = db.Column(db.JSON, default=list)
    notas_internas = db.Column(db.Text)
    ultima_visita = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    citas = db.relationship('Cita', backref='paciente', lazy=True)
    ventas = db.relationship('Venta', backref='paciente', lazy=True)
    notas_clinicas = db.relationship('NotaClinica', backref='paciente', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre_completo': self.nombre_completo,
            'email': self.email,
            'telefono': self.telefono,
            'telefono_alternativo': self.telefono_alternativo,
            'fecha_nacimiento': self.fecha_nacimiento.strftime('%Y-%m-%d') if self.fecha_nacimiento else None,
            'genero': self.genero,
            'direccion': self.direccion,
            'ocupacion': self.ocupacion,
            'alergias': self.alergias,
            'condiciones_medicas': self.condiciones_medicas,
            'medicamentos_actuales': self.medicamentos_actuales,
            'seguro_medico': self.seguro_medico,
            'numero_seguro': self.numero_seguro,
            'total_gastado': self.total_gastado,
            'saldo_pendiente': self.saldo_pendiente,
            'activo': self.activo,
            'etiquetas': self.etiquetas,
            'notas_internas': self.notas_internas,
            'ultima_visita': self.ultima_visita.isoformat() if self.ultima_visita else None
        }

# ============================================
# MODELO: Cita
# ============================================
class Cita(db.Model):
    __tablename__ = 'citas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profesional_id = db.Column(db.Integer, db.ForeignKey('profesionales.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.String(5), nullable=False)
    hora_fin = db.Column(db.String(5), nullable=False)
    duracion_minutos = db.Column(db.Integer)
    
    estado = db.Column(db.String(20), default='confirmada')
    notas = db.Column(db.Text)
    monto = db.Column(db.Float)
    pagado = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    venta = db.relationship('Venta', backref='cita', lazy=True, uselist=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'paciente_nombre': self.paciente.nombre_completo if self.paciente else None,
            'profesional_id': self.profesional_id,
            'profesional_nombre': self.profesional.nombre if self.profesional else None,
            'servicio_id': self.servicio_id,
            'servicio_nombre': self.servicio.nombre if self.servicio else None,
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'hora_inicio': self.hora_inicio,
            'hora_fin': self.hora_fin,
            'duracion_minutos': self.duracion_minutos,
            'estado': self.estado,
            'notas': self.notas,
            'monto': self.monto,
            'pagado': self.pagado
        }

# ============================================
# MODELO: Nota Clinica
# ============================================
class NotaClinica(db.Model):
    __tablename__ = 'notas_clinicas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    profesional_id = db.Column(db.Integer, db.ForeignKey('profesionales.id'))
    
    titulo = db.Column(db.String(100))
    contenido = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(20), default='general')
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'profesional_id': self.profesional_id,
            'titulo': self.titulo,
            'contenido': self.contenido,
            'tipo': self.tipo,
            'created_at': self.created_at.isoformat()
        }

# ============================================
# MODELO: Venta
# ============================================
class Venta(db.Model):
    __tablename__ = 'ventas'
    
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=True)
    profesional_id = db.Column(db.Integer, db.ForeignKey('profesionales.id'), nullable=True)
    
    tipo = db.Column(db.String(20), default='servicio')
    subtotal = db.Column(db.Float, default=0)
    descuento = db.Column(db.Float, default=0)
    impuesto = db.Column(db.Float, default=0)
    total = db.Column(db.Float, default=0)
    
    metodo_pago = db.Column(db.String(20), default='pendiente')
    estado = db.Column(db.String(20), default='pendiente')
    
    notas = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'paciente_nombre': self.paciente.nombre_completo if self.paciente else None,
            'cita_id': self.cita_id,
            'profesional_id': self.profesional_id,
            'tipo': self.tipo,
            'subtotal': self.subtotal,
            'descuento': self.descuento,
            'impuesto': self.impuesto,
            'total': self.total,
            'metodo_pago': self.metodo_pago,
            'estado': self.estado,
            'notas': self.notas,
            'detalles': [d.to_dict() for d in self.detalles],
            'created_at': self.created_at.isoformat()
        }

# ============================================
# MODELO: Detalle Venta
# ============================================
class DetalleVenta(db.Model):
    __tablename__ = 'detalles_venta'
    
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    
    tipo_item = db.Column(db.String(20), nullable=False)
    item_id = db.Column(db.Integer, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'tipo_item': self.tipo_item,
            'item_id': self.item_id,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario,
            'subtotal': self.subtotal
        }

# ============================================
# MODELO: Inventario
# ============================================
class Inventario(db.Model):
    __tablename__ = 'inventario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True)
    descripcion = db.Column(db.Text)
    categoria = db.Column(db.String(50))
    
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    precio_compra = db.Column(db.Float, default=0)
    precio_venta = db.Column(db.Float, default=0)
    unidad_medida = db.Column(db.String(20), default='unidad')
    
    activo = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'codigo': self.codigo,
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'precio_compra': self.precio_compra,
            'precio_venta': self.precio_venta,
            'unidad_medida': self.unidad_medida,
            'activo': self.activo
        }

# ============================================
# MODELO: Usuario (Autenticación)
# ============================================
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100))
    nombre_completo = db.Column(db.String(150))
    activo = db.Column(db.Boolean, default=True)
    es_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'nombre_completo': self.nombre_completo,
            'activo': self.activo,
            'es_admin': self.es_admin
        }
    
    def set_password(self, password):
        """Genera el hash de la contraseña"""
        import bcrypt
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verifica la contraseña"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))