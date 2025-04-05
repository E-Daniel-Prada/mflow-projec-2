# Usa una imagen de Python ligera
FROM python:3.10-slim

# Configura el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido de la app
COPY app /app/app

# Copia el script de inicio
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh

# Expone los puertos de FastAPI y Gradio
EXPOSE 8000
EXPOSE 8503

# Comando único de inicio
CMD ["./start.sh"]
