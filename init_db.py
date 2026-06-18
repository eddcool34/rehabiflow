from app import app
from database import db
from models import Servicio, Profesional, Paciente, Cita, Venta, DetalleVenta, NotaClinica, Inventario

def init_database():
    """Crea todas las tablas en la base de datos"""
    with app.app_context():
        print("🔄 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas exitosamente.")
        print(f"📊 Tablas disponibles: {db.engine.table_names()}")

if __name__ == '__main__':
    init_database()