from app import app
from database import db
from models import Servicio, Profesional

def create_tables():
    """Crea todas las tablas"""
    with app.app_context():
        print("🔄 Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas/verificadas.")

def seed_database():
    """Agrega datos de prueba a la base de datos"""
    with app.app_context():
        # --- PRIMERO CREAR TABLAS ---
        create_tables()
        
        # --- LUEGO AGREGAR DATOS ---
        print("🔄 Insertando datos de prueba...")
        
        servicios_data = [
            {'nombre': 'Terapia de columna lumbar', 'descripcion': 'Tratamiento para dolor lumbar', 'duracion_minutos': 60, 'precio': 800.00, 'costo': 200.00},
            {'nombre': 'Rehabilitación de rodilla', 'descripcion': 'Terapia post-operatoria', 'duracion_minutos': 45, 'precio': 700.00, 'costo': 150.00},
            {'nombre': 'Electroterapia', 'descripcion': 'Terapia con corriente eléctrica', 'duracion_minutos': 30, 'precio': 350.00, 'costo': 80.00},
            {'nombre': 'Masaje terapéutico', 'descripcion': 'Masaje para relajación muscular', 'duracion_minutos': 60, 'precio': 600.00, 'costo': 100.00},
            {'nombre': 'Evaluación inicial', 'descripcion': 'Valoración completa del paciente', 'duracion_minutos': 90, 'precio': 500.00, 'costo': 120.00}
        ]
        
        for s in servicios_data:
            existe = Servicio.query.filter_by(nombre=s['nombre']).first()
            if not existe:
                servicio = Servicio(**s)
                db.session.add(servicio)
                print(f'  ✅ Servicio creado: {s["nombre"]}')
            else:
                print(f'  ⏩ Servicio ya existe: {s["nombre"]}')
        
        # ========== PROFESIONAL FIJO ==========
        profesional_existente = Profesional.query.filter_by(nombre='José Vera Arellano').first()
        if not profesional_existente:
            profesional = Profesional(
                nombre='José Vera Arellano',
                especialidad='Fisioterapia y Rehabilitación',
                email='jose.vera@rehabiflow.com',
                telefono='555-1234',
                comision_porcentaje=0,
                horario_laboral={
                    'lunes': {'activo': True, 'inicio': '09:00', 'fin': '18:00'},
                    'martes': {'activo': True, 'inicio': '09:00', 'fin': '18:00'},
                    'miercoles': {'activo': True, 'inicio': '09:00', 'fin': '18:00'},
                    'jueves': {'activo': True, 'inicio': '09:00', 'fin': '18:00'},
                    'viernes': {'activo': True, 'inicio': '09:00', 'fin': '18:00'},
                    'sabado': {'activo': False},
                    'domingo': {'activo': False}
                },
                activo=True
            )
            db.session.add(profesional)
            print('  ✅ Profesional fijo creado: José Vera Arellano')
        else:
            print('  ⏩ Profesional fijo ya existe.')
        
        db.session.commit()
        print('🎉 ¡Datos de prueba cargados exitosamente!')

if __name__ == '__main__':
    seed_database()