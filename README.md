# Proyecto FERREMAS

FERREMAS es una aplicación de eCommerce para la gestión y venta de productos de ferretería y construcción. Este proyecto incluye una interfaz web desarrollada con Django, una API REST para usuarios con FastAPI, y una API de productos basada en Node.js.

## Requisitos previos

- Python 3.9 o superior  
- Node.js 14 o superior  
- Oracle Database  
- pip (gestor de paquetes de Python)  
- npm (gestor de paquetes de Node.js)

---

## 1. Crear base de datos en Oracle

Ejecutar las siguientes sentencias en Oracle SQL*Plus o una herramienta compatible:

```sql
ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;
CREATE USER productobd IDENTIFIED BY productobd;
GRANT CONNECT, RESOURCE, DBA TO productobd;

2. Importar estructura de la base de datos

Abrir el archivo basededatos.sql, copiar su contenido y ejecutarlo sobre el usuario productobd creado anteriormente.
3. Instalar dependencias de Python

Desde la raíz del proyecto, ejecutar:

pip install -r requirements.txt

4. Ejecutar la aplicación web (FERREMAS)

cd ferremas
python manage.py runserver

Esto iniciará el sitio web de FERREMAS en http://127.0.0.1:8000.
5. Ejecutar la API de usuarios (FastAPI)

En una nueva consola:

cd ferremas
uvicorn api_usuarios.main:app --reload --port 8001

Esto levantará la API de usuarios en http://127.0.0.1:8001.
6. Ejecutar la API de productos (Node.js)

En otra consola:

cd api_productos
node index.js

Esto iniciará la API de productos en http://localhost:3000 (o el puerto configurado).
7. Iniciar sesión como administrador

Acceder a la aplicación web de FERREMAS:

    Usuario: admin

    Contraseña: admin123

Una vez iniciada la sesión, en el menú junto a la opción "Tienda", aparecerá el panel de Administración. Desde allí, seleccionar "Adm. Usuarios" para crear y gestionar nuevos usuarios.
