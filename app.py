from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

# Carga las variables de entorno desde el archivo .env
load_dotenv() 

app = Flask(__name__)

# --- CONFIGURACIÓN DE MONGODB ---
# Usa la variable de entorno o un valor por defecto (localhost)
MONGO_URI = os.getenv('MONGO_URI', "mongodb+srv://itecidb2:iteci2021@clusteriteci.rnxhk.mongodb.net/Prepa_ITECI_Ens?connect=replicaSet") 
DB_NAME = 'seguimiento_semestral_db'
COLLECTION_NAME = 'registros'

# 1. Inicializar la variable 'collection' a None antes del bloque try
client = None
db = None
collection = None

try:
    client = MongoClient(MONGO_URI)
    # Ping para verificar la conexión
    client.admin.command('ping') 
    db = client[DB_NAME]
    # 'collection' solo se asigna si la conexión fue exitosa
    collection = db[COLLECTION_NAME] 
    print("✅ Conexión a MongoDB Atlas exitosa.")
except Exception as e:
    # Si falla, 'collection' se mantiene como None
    print(f"❌ Error CRÍTICO de conexión a MongoDB. Los datos NO se podrán guardar. Error: {e}")


@app.route('/', methods=['GET'])
def index():
    """Ruta para mostrar el formulario."""
    return render_template('formulario.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    """Ruta para manejar el envío del formulario y guardar los datos."""
    
    # 2. Verificar la conexión ANTES de intentar usar la colección
    if collection is None:
        return render_template('error.html', 
                               error="La aplicación no pudo conectarse a la base de datos. Por favor, verifica la MONGO_URI y la conexión a MongoDB Atlas.")
    
    # 1. Convertir los datos inmutables del formulario a un diccionario mutable
    form_data = request.form.to_dict()

    # 2. Estructurar los datos para MongoDB (Asegúrate de que las claves coincidan con los 'name' del HTML)
    documento = {
        'fecha_registro': datetime.now(),
        'datos_generales': {
            'nombre': form_data.get('nombre'),
            'matricula': form_data.get('matricula'),
            'carrera': form_data.get('carrera'),
            'cuatrimestre': form_data.get('cuatrimestre')
        },
        'analisis_semestre_anterior': {
            'ant_materia1_nombre': form_data.get('ant_materia1_nombre'),
            'ant_materia1_final': form_data.get('ant_materia1_final'),
            'ant_materia1_inasist': form_data.get('ant_materia1_inasist'),
            'promedio_anterior': form_data.get('promedio_anterior'),
            'avance_carrera_reflexion': form_data.get('avance_carrera')
        },
        'plan_accion_personal': {
            'balance_aprobacion': form_data.get('reflexion_aprobacion'),
            'acciones_aprobacion': form_data.get('acciones_aprobacion'),
            'estrategias_academicas': form_data.get('estrategias_academicas'),
            'objetivos_corto_plazo': form_data.get('objetivos_corto_plazo'),
        },
        'seguimiento_y_cierre': {
            'solicitud_canalizacion': form_data.get('solicitud_canalizacion'),
            'observaciones_tutor': form_data.get('observaciones_tutor'), 
            'pronostico_cierre': form_data.get('pronostico_cierre')
        }
    }
    
    # 3. Insertar en MongoDB
    try:
        collection.insert_one(documento)
        return render_template('exito.html', mensaje="¡Formulario enviado con éxito! Los datos han sido guardados en MongoDB Atlas.")
    except Exception as e:
        return render_template('error.html', error=f"Error al guardar los datos en MongoDB: {e}")

# Rutas de éxito y error
@app.route('/exito')
def exito():
    return render_template('exito.html', mensaje="Operación exitosa.")

@app.route('/error')
def error():
    # Muestra un mensaje de error genérico si se accede directamente
    return render_template('error.html', error="Ocurrió un error desconocido durante el proceso.")

if __name__ == '__main__':
    app.run(debug=True)