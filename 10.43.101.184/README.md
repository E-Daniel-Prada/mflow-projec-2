# Proyecto MLOps MLflow, Mysql y Docker

## 📌 Descripción
En esta seccion instalamos  un modelo de **MLFlow** configurado a una base de datos **MYSQL** y utilizando **MINIO** como repositorio de objectos tipo bucket.

## 📁 Estructura del Proyecto
```
├── docker-compose.yml  # Despliegue de servicio de MYSQL y MINIO
├── Dockerfile          # Configuracion y parametrizacion de imagen MINIO
├── mlflow_serv.service/# Configuración del servidor MLflow
├── requirements.txt    # Archivo con librerias a instalar en Python
├── README.md           # Documentación del proyecto
```

## 🚀 Requisitos Previos
Antes de ejecutar este proyecto, asegúrate de tener instalado:
- **Docker** y **Docker Compose**
- **Python 3.x**

## ⚙️ Instalación y Configuración

### 1️⃣ **Configurar y ejecutar Docker**
Ejecuta el siguiente comando para construir y levantar los contenedores:
```sh
docker-compose up --build
```
Esto iniciará los siguientes servicios:
- **Mysql** en `http://localhost:3306`
- **MiNio** en `http://localhost:9000 ~ 9001`
-
### 2️⃣ **Se debe ejecutar el siguiente comando sobre la terminal utilizando permisos de administrador**
- **systemctl enable mlflow_serv.service**
- **systemctl start mlflow_serv.service**
- **systemctl status mlflow_serv.service**

Con estos comando se ejecutara **MLFlow** y quedara disponible atravez del puerto 5000

## 📌 Conclusión
Este proyecto demuestra cómo instalar **MLOps** utilizando **Docker, MYSQL y MiNio** para almacenar experimentos y sus modelos entrenados. 🚀

