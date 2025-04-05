#!/bin/bash

# Cargar variables de entorno desde el archivo .env
if [ -f /app/.env ]; then
  export $(grep -v '^#' /app/.env | xargs)
  echo "Variables de entorno cargadas"
else
  echo "Archivo .env no encontrado en /app"
fi

# Iniciar FastAPI en segundo plano
echo "Iniciando FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

# Iniciar Gradio en primer plano
echo "Iniciando interfaz Gradio..."
python app/interface.py
