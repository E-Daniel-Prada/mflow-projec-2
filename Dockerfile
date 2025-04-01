# Dockerfile
FROM jupyter/scipy-notebook:latest

# Dependencias del sistema
USER root
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Carpeta para MLflow con permisos adecuados
RUN mkdir -p /mlflow && chown -R jovyan:users /mlflow

# Cambiar a usuario jovyan
USER jovyan

# Dependencias de Python
RUN pip install mlflow psycopg2-binary scikit-learn pandas sqlalchemy

# Exponer puertos
EXPOSE 8888 5000 5432

# Comando por defecto
CMD ["start-notebook.sh", "--NotebookApp.token=''"]
