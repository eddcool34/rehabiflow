import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'rehabiflow-secret-key-2025')
    
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        'sqlite:///rehabiflow.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    EMPRESA_NOMBRE = 'RehabiFlow'
    EMPRESA_TELEFONO = '555-0000'
    HORARIO_INICIO = '09:00'
    HORARIO_FIN = '18:00'