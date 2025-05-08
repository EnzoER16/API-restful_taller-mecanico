# Flask API RESTful CRUD - Taller Mecánico

Este es un proyecto que consiste en una aplicación CRUD usando Flask, SQLAlchemy y MySQL, específicamente de un taller mecánico.

## Integrantes del grupo

- Enzo Rojas
- Matías Agüero
- Gustavo Vera
- Lautaro Videla

## Requisitos

- [Python](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/mysql/)

## Configuración e instalación

### 1) Crear entorno virtual

#### En Linux / macOS:
```sh
python3 -m venv <nombre_del_entorno>
```

#### En Windows:
```sh
python -m venv <nombre_del_entorno>
```

### 2) Activar entorno virtual

#### En Linux / macOS:
```sh
source <nombre_del_entorno>/bin/activate
```

#### En Windows:
```sh
<nombre_del_entorno>\scripts\activate
```

### 3) Clonar repositorio

```sh
git clone <url_del_repositorio>
```

### 4) Acceder al directorio del proyecto
```sh
cd <nombre_del_proyecto>
```

### 5) Instalar dependencias

#### Especificando cada una
```sh
pip install Flask Flask-SQLAlchemy PyMySQL
```

#### Desde el archivo `requirements.txt`
```sh
pip install -r requirements.txt
```

### 6) Modificar variables de entorno en `example.env`

Antes de ejecutar la aplicación, se deben configurar las siguientes variables de entorno:

```sh
DB_USER=<tu_usuario>
DB_PASSWORD=<tu_contraseña>
DB_HOST=<host_de_mysql>
DB_NAME=<nombre_de_la_base_de_datos>
```
### 7) Ejecutar aplicación
```sh
python app.py
```