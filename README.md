# FERREMAS - Plataforma de eCommerce para Ferreterías y Construcción 🛠️

**FERREMAS** es una solución integral de comercio electrónico orientada a la venta y gestión de productos del rubro ferretero y de la construcción. La aplicación está compuesta por tres módulos principales:

- 🌐 Interfaz web desarrollada con **Django**
- 🔐 API REST de usuarios implementada con **FastAPI**
- 📦 API de productos construida con **Node.js**

---

## 🚀 Tecnologías y Requisitos

Asegúrate de tener instalado lo siguiente:

- **Python** 3.9 o superior  
- **Node.js** 14 o superior  
- **Oracle Database**  
- **pip** (gestor de paquetes de Python)  
- **npm** (gestor de paquetes de Node.js)

---

## ⚙️ Configuración del Entorno

### 1. Crear usuario en Oracle

Ejecuta los siguientes comandos en Oracle SQL*Plus o una herramienta compatible:

```sql
ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;
CREATE USER usuariosbd IDENTIFIED BY usuariosbd;
GRANT CONNECT, RESOURCE, DBA TO usuariosbd;
```

### 2. Importar estructura de base de datos

Abre el archivo `basededatos.sql`, copia su contenido y ejecútalo dentro del usuario `usuariosbd`.

---

## 📦 Instalación del Proyecto

### 3. Instalar dependencias de Python

Desde la raíz del proyecto, ejecuta:

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación web (Django)

```bash
cd ferremas
python manage.py runserver
```

Accede a la interfaz en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🔐 API de Usuarios (FastAPI)

### 5. Iniciar FastAPI

En una nueva terminal:

```bash
cd ferremas
uvicorn api_usuarios.main:app --reload --port 8001
```

Disponible en: [http://127.0.0.1:8001](http://127.0.0.1:8001)

---

## 📦 API de Productos (Node.js)

### 6. Iniciar Node.js

En otra terminal:

```bash
cd api_productos
node index.js
```

Disponible en: [http://localhost:3000](http://localhost:3000)

---

## 👤 Acceso como Administrador

Inicia sesión en la plataforma con las siguientes credenciales:

- **Usuario:** `admin`  
- **Contraseña:** `admin123`

Una vez dentro, accede al panel de administración desde el menú principal. En la sección "Adm. Usuarios" podrás gestionar el registro y control de usuarios.

---

