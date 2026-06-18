from app import app
from database import db
from models import Usuario

with app.app_context():
    # Verificar si ya hay usuarios
    if Usuario.query.count() == 0:
        admin = Usuario(
            username='admin',
            email='admin@rehabiflow.com',
            nombre_completo='Administrador',
            es_admin=True,
            activo=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('✅ Usuario admin creado')
        print('📋 Usuario: admin')
        print('🔑 Contraseña: admin123')
    else:
        print('⚠️ Ya existen usuarios en el sistema')
        print(f'📊 Total de usuarios: {Usuario.query.count()}')