1.crear base de datos usuariosbd:
ALTER SESSION SET "_ORACLE_SCRIPT" = TRUE;
CREATE USER productobd IDENTIFIED BY productobd;
GRANT CONNECT, RESOURCE, DBA TO productobd;
2.en basededatos.sql copiar y pegar en usuariosbd y ejecutar
3.pip install -r requirements.txt
4.abrir consola y ejecutar cd ferremas y luego escribir python manage.py runserver y se ejecutará la página ferremas
5.abrir consola y ejecutar cd ferremas y luego escribir uvicorn api_usuarios.main:app --reload --port 8001 y se ejecutará la api usuarios
6.abrir consola y ejecutar cd api_productos y luego escribir node index.js y se ejecutará la api productos
7.iniciar sesion en ferremas con administrador con el nombre admin y contraseña admin123, al lado de tienda abrá una opcion de administración y selecionar adm. usuarios para crear mas usuarios (en pagina ferremas en registrar solo se podrán crear usuarios con rol de cliente ya que el administrador otorga los demás roles)
