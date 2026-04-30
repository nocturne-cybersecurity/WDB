# WSQL - SQLite Database Manager
![WDB](images/WDB.png)
Una aplicación de consola interactiva para gestionar bases de datos SQLite con una interfaz CRUD completa.

## Características

- **Gestión de Bases de Datos**: Crear, renombrar, eliminar y cambiar entre múltiples bases de datos
- **Operaciones CRUD Completas**: Crear, leer, actualizar y eliminar tablas y registros
- **Gestión de Columnas**: Agregar, modificar y eliminar columnas dinámicamente
- **Interfaz Atractiva**: Banner ASCII con colores y animaciones usando Rich y pyfiglet
- **Menú Intuitivo**: Sistema de menús fácil de navegar con opciones numeradas
- **Búsqueda Avanzada**: Buscar registros por cualquier columna con coincidencias parciales
- **Visualización de Datos**: Tablas formateadas con colores para mejor legibilidad

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/nocturne-cybersecurity/WDB.git
cd WSQL
```

2. Crea un entorno virtual:
```bash
python -m venv .venv
```

3. Activa el entorno virtual:
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

Ejecuta la aplicación principal:
```bash
python3 main.py
```

Si no funciona python3:
```bash
python main.py
```

### Flujo de Trabajo

1. **Database Manager**: Se abre automáticamente al iniciar para gestionar bases de datos
2. **Seleccionar o Crear BD**: Elige una base de datos existente o crea una nueva
3. **Operaciones CRUD**: Accede al menú principal para gestionar tablas y datos

## Funcionalidades Principales

### Database Manager
- [N] Nueva base de datos
- [R] Renombrar base de datos
- [X] Eliminar base de datos
- [V] Volver al CRUD

### Operaciones CRUD
- [1] Crear tabla
- [2] Agregar columna
- [3] Insertar fila
- [4] Buscar filas
- [5] Ver columnas de una tabla
- [6] Agregar texto a una celda
- [7] Reescribir texto en una celda
- [8] Mostrar tabla completa
- [9] Eliminar tabla
- [10] Eliminar fila
- [11] Eliminar columna
- [12] Eliminar base de datos
- [13] Configurar base de datos
- [14] Mostrar todas las tablas
- [15] Database Manager
- [16] Salir

## Estructura del Proyecto

```
WSQL/
├── main.py          # Punto de entrada principal
├── CRUD.py          # Módulo de operaciones CRUD
├── requirements.txt # Dependencias del proyecto
├── README.md        # Documentación
└── databases/       # Carpeta para bases de datos (creada automáticamente)
```

## Dependencias

- **colorama**: Para colores en la consola
- **pyfiglet**: Para generar arte ASCII
- **rich**: Para interfaces mejoradas en consola
- **sqlite3**: Para gestión de bases de datos SQLite (incluido en Python estándar)

## Ejemplos de Uso

### Crear una Tabla
```
Nombre de la nueva tabla: usuarios
Columnas (ej: nombre TEXT, edad INTEGER): nombre TEXT, email TEXT, edad INTEGER
```

### Insertar Datos
```
Selecciona tabla: usuarios
Ingresa los valores:
  nombre: Juan Pérez
  email: juan@example.com
  edad: 25
```

### Buscar Registros
```
Selecciona tabla: usuarios
Buscar por columna: nombre
Valor de 'nombre': Juan
```

## Atajos de Teclado

- **Ctrl+C**: Salir del programa en cualquier momento
- **Enter**: Confirmar selecciones y continuar

## Notas

- Las bases de datos se guardan automáticamente en la carpeta `databases/`
- Todas las tablas incluyen un campo `id` autoincremental como clave primaria
- El programa mantiene un registro de la base de datos activa
- Los cambios se guardan automáticamente en la base de datos

## Licencia

Este proyecto es de código abierto y está disponible bajo la Licencia MIT.

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Autor

Desarrollado como una herramienta de gestión de bases de datos SQLite con interfaz de consola moderna.
