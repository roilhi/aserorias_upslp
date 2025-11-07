# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto que Flask usa por defecto (5000)
EXPOSE 5000

# Comando para ejecutar la aplicación cuando se inicia el contenedor
# Usa Gunicorn o un servidor de producción para entornos reales. 
# Aquí usamos 'flask run' para simplificar, pero en producción, reemplázalo con:
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
CMD ["flask", "run", "--host=0.0.0.0"]