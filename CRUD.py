from colorama import Fore, init
import sqlite3 as sql
import time
import sys
import os
import glob

init(autoreset=True)

DB_FOLDER = "databases"
os.makedirs(DB_FOLDER, exist_ok=True)

conn    = None
cursor  = None
DB_NAME = None

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input(Fore.YELLOW + "\nPresiona Enter para continuar...")
    limpiar()

def cabecera_db():
    nombre = os.path.basename(DB_NAME) if DB_NAME else "Sin base de datos"
    print(Fore.BLUE  + "=" * 43)
    print(Fore.BLUE  + "     CRUD SQLite")
    print(Fore.GREEN + f"     DB: {nombre}")
    print(Fore.BLUE  + "=" * 43)

def tablas_disponibles():
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'")
    return [row[0] for row in cursor.fetchall()]

def seleccionar_tabla():
    tablas = tablas_disponibles()
    if not tablas:
        print(Fore.RED + "No hay tablas disponibles.")
        return None
    print(Fore.CYAN + "Tablas disponibles:")
    for i, t in enumerate(tablas, 1):
        print(Fore.CYAN + f"  [{i}] {t}")
    entrada = input(Fore.CYAN + "Numero o nombre de la tabla: ").strip()

    if entrada.isdigit():
        idx = int(entrada) - 1
        if 0 <= idx < len(tablas):
            return tablas[idx]
        print(Fore.RED + "Numero fuera de rango.")
        return None

    if entrada in tablas:
        return entrada

    print(Fore.RED + f"La tabla '{entrada}' no existe.")
    return None


def listar_bases():
    return sorted(glob.glob(os.path.join(DB_FOLDER, "*.db")))

def abrir_db(ruta):
    global conn, cursor, DB_NAME
    if conn:
        conn.close()
    conn    = sql.connect(ruta)
    cursor  = conn.cursor()
    DB_NAME = ruta

def _seleccionar_base(bases):
    for i, b in enumerate(bases, 1):
        print(Fore.CYAN + f"  [{i}] {os.path.basename(b)}")
    entrada = input(Fore.CYAN + "Numero o nombre (.db): ").strip()
    if entrada.isdigit():
        idx = int(entrada) - 1
        if 0 <= idx < len(bases):
            return bases[idx]
        print(Fore.RED + "Numero fuera de rango.")
        return None
    ruta = os.path.join(DB_FOLDER, entrada if entrada.endswith(".db") else entrada + ".db")
    if ruta in bases:
        return ruta
    print(Fore.RED + "No encontrada.")
    return None

def menu_database_manager():
    global conn, cursor, DB_NAME

    while True:
        limpiar()
        bases = listar_bases()

        print(Fore.BLUE  + "=" * 43)
        print(Fore.BLUE  + "     DATABASE MANAGER")
        print(Fore.BLUE  + "=" * 43)

        if bases:
            print(Fore.CYAN + "Bases de datos:")
            for i, b in enumerate(bases, 1):
                size_kb = os.path.getsize(b) / 1024
                activa  = Fore.GREEN + "  <- activa" if b == DB_NAME else ""
                print(Fore.WHITE + f"  [{i}] {os.path.basename(b)}  ({size_kb:.1f} KB){activa}")
        else:
            print(Fore.YELLOW + "  (No hay bases de datos aun)")

        print(Fore.BLUE + "-" * 43)
        print(Fore.CYAN +
            "[N] Nueva base de datos\n"
            "[R] Renombrar base de datos\n"
            "[X] Eliminar base de datos\n"
            "[V] Volver al CRUD\n"
            "O selecciona un numero para abrir"
        )
        print(Fore.BLUE + "-" * 43)

        ans = input(Fore.CYAN + ">> ").strip().upper()

        try:
            if ans == "N":
                nombre = input(Fore.CYAN + "Nombre de la nueva base de datos: ").strip()
                if not nombre:
                    print(Fore.RED + "Nombre invalido."); pausar(); continue
                if not nombre.endswith(".db"):
                    nombre += ".db"
                ruta = os.path.join(DB_FOLDER, nombre)
                if os.path.exists(ruta):
                    print(Fore.YELLOW + f"Ya existe '{nombre}'."); pausar(); continue
                c = sql.connect(ruta); c.close()
                print(Fore.GREEN + f"Base de datos '{nombre}' creada y abierta automaticamente")
                abrir_db(ruta)
                pausar()

            elif ans == "R":
                if not bases:
                    print(Fore.RED + "No hay bases de datos."); pausar(); continue
                b = _seleccionar_base(bases)
                if not b: pausar(); continue
                nuevo = input(Fore.CYAN + "Nuevo nombre: ").strip()
                if not nuevo: pausar(); continue
                if not nuevo.endswith(".db"):
                    nuevo += ".db"
                nueva_ruta = os.path.join(DB_FOLDER, nuevo)
                if b == DB_NAME:
                    conn.close()
                    conn = cursor = None; DB_NAME = None
                os.rename(b, nueva_ruta)
                print(Fore.GREEN + f"Renombrada a '{nuevo}' OK")
                pausar()

            elif ans == "X":
                if not bases:
                    print(Fore.RED + "No hay bases de datos."); pausar(); continue
                b = _seleccionar_base(bases)
                if not b: pausar(); continue
                confirm = input(Fore.RED + f"Eliminar '{os.path.basename(b)}'? (s/n): ").strip().lower()
                if confirm == "s":
                    if b == DB_NAME:
                        conn.close()
                        conn = cursor = None; DB_NAME = None
                    os.remove(b)
                    print(Fore.GREEN + "Eliminada OK")
                pausar()

            elif ans == "V":
                if DB_NAME is None:
                    print(Fore.RED + "Primero abre o crea una base de datos.")
                    pausar(); continue
                break

            elif ans.isdigit():
                idx = int(ans) - 1
                if 0 <= idx < len(bases):
                    abrir_db(bases[idx])
                    print(Fore.GREEN + f"Abriendo '{os.path.basename(bases[idx])}' OK")
                    pausar()
                else:
                    print(Fore.RED + "Numero fuera de rango."); pausar()
            else:
                print(Fore.RED + "Opcion invalida."); pausar()

        except KeyboardInterrupt:
            salir()

def menu():
    limpiar()
    cabecera_db()

    animation = ["|", "/", "-", "\\"]
    for i in range(20):
        time.sleep(0.05)
        sys.stdout.write(Fore.RED + "\rCargando CRUD " + animation[i % len(animation)])
        sys.stdout.flush()
    print(Fore.GREEN + "\rCRUD Cargado OK              ")
    print(Fore.BLUE + "-" * 43)

    return input(Fore.CYAN +
        "[1]  Crear tabla\n"
        "[2]  Agregar columna\n"
        "[3]  Insertar fila\n"
        "[4]  Buscar filas\n"
        "[5]  Ver columnas de una tabla\n"
        "[6]  Agregar texto a una celda\n"
        "[7]  Reescribir texto en una celda\n"
        "[8]  Mostrar tabla completa\n"
        "[9]  Eliminar tabla\n"
        "[10] Eliminar fila\n"
        "[11] Eliminar columna\n"
        "[12] Eliminar base de datos\n"
        "[13] Configurar base de datos\n"
        "[14] Mostrar todas las tablas\n"
        "[15] Database Manager\n"
        "[16] Salir\n"
        ">> "
    )

def crear_tabla():
    nombre = input(Fore.CYAN + "Nombre de la nueva tabla: ").strip()
    if not nombre:
        print(Fore.RED + "Nombre invalido.")
        return
    columnas_raw = input(Fore.CYAN + "Columnas (ej: nombre TEXT, edad INTEGER): ").strip()
    if not columnas_raw:
        print(Fore.RED + "Debes ingresar al menos una columna.")
        return
    try:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS "{nombre}" (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columnas_raw}
            )
        """)
        conn.commit()
        print(Fore.GREEN + f"Tabla '{nombre}' creada correctamente OK")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def agregar_columna():
    tabla = seleccionar_tabla()
    if not tabla: return
    columna = input(Fore.CYAN + "Nombre de la nueva columna: ").strip()
    tipo    = input(Fore.CYAN + "Tipo (TEXT, INTEGER, REAL, BLOB): ").strip().upper() or "TEXT"
    try:
        cursor.execute(f'ALTER TABLE "{tabla}" ADD COLUMN "{columna}" {tipo}')
        conn.commit()
        print(Fore.GREEN + f"Columna '{columna}' agregada a '{tabla}' OK")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def insertar_fila():
    tabla = seleccionar_tabla()
    if not tabla: return
    cursor.execute(f'PRAGMA table_info("{tabla}")')
    columnas = [row[1] for row in cursor.fetchall() if row[1] != "id"]
    if not columnas:
        print(Fore.RED + "La tabla no tiene columnas (aparte de id).")
        return
    valores = []
    print(Fore.CYAN + "Ingresa los valores para cada columna:")
    for col in columnas:
        val = input(Fore.CYAN + f"  {col}: ").strip()
        valores.append(val if val else None)
    placeholders = ", ".join(["?" for _ in columnas])
    cols_str     = ", ".join([f'"{c}"' for c in columnas])
    try:
        cursor.execute(f'INSERT INTO "{tabla}" ({cols_str}) VALUES ({placeholders})', valores)
        conn.commit()
        print(Fore.GREEN + f"Fila insertada correctamente OK  (id={cursor.lastrowid})")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def buscar_filas():
    tabla = seleccionar_tabla()
    if not tabla: return
    cursor.execute(f'PRAGMA table_info("{tabla}")')
    columnas = [row[1] for row in cursor.fetchall()]
    print(Fore.CYAN + f"Columnas: {', '.join(columnas)}")
    col = input(Fore.CYAN + "Buscar por columna: ").strip()
    if col not in columnas:
        print(Fore.RED + "Columna no encontrada.")
        return
    valor = input(Fore.CYAN + f"Valor de '{col}': ").strip()
    try:
        cursor.execute(f'SELECT * FROM "{tabla}" WHERE "{col}" LIKE ?', (f"%{valor}%",))
        filas = cursor.fetchall()
        if not filas:
            print(Fore.YELLOW + "Sin resultados.")
        else:
            _imprimir_filas(columnas, filas)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def ver_columnas():
    tabla = seleccionar_tabla()
    if not tabla: return
    cursor.execute(f'PRAGMA table_info("{tabla}")')
    info = cursor.fetchall()
    print(Fore.GREEN + f"\nColumnas de '{tabla}':")
    for col in info:
        print(Fore.WHITE + f"  {col[1]}  ({col[2]})")


def agregar_texto():
    tabla = seleccionar_tabla()
    if not tabla: return
    id_fila = input(Fore.CYAN + "ID de la fila: ").strip()
    columna = input(Fore.CYAN + "Columna a modificar: ").strip()
    texto   = input(Fore.CYAN + "Texto a agregar: ").strip()
    try:
        cursor.execute(
            f'UPDATE "{tabla}" SET "{columna}" = COALESCE("{columna}", "") || ? WHERE id = ?',
            (texto, id_fila)
        )
        conn.commit()
        if cursor.rowcount:
            print(Fore.GREEN + "Texto agregado OK")
        else:
            print(Fore.YELLOW + "No se encontro la fila con ese id.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def reescribir_texto():
    tabla = seleccionar_tabla()
    if not tabla: return
    id_fila = input(Fore.CYAN + "ID de la fila: ").strip()
    columna = input(Fore.CYAN + "Columna a reescribir: ").strip()
    nuevo   = input(Fore.CYAN + "Nuevo valor: ").strip()
    try:
        cursor.execute(
            f'UPDATE "{tabla}" SET "{columna}" = ? WHERE id = ?',
            (nuevo, id_fila)
        )
        conn.commit()
        if cursor.rowcount:
            print(Fore.GREEN + "Valor actualizado OK")
        else:
            print(Fore.YELLOW + "No se encontro la fila con ese id.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def _imprimir_filas(columnas, filas):
    anchos = [len(col) for col in columnas]
    for fila in filas:
        for i, val in enumerate(fila):
            anchos[i] = max(anchos[i], len(str(val) if val is not None else "NULL"))
    PAD = 3

    separador  = "-+-".join("-" * (anchos[i] + PAD) for i in range(len(columnas)))
    encabezado = " | ".join(Fore.GREEN + col.ljust(anchos[i] + PAD) for i, col in enumerate(columnas))

    print()
    print(encabezado)
    print(Fore.BLUE + separador)
    for fila in filas:
        print(" | ".join(
            Fore.WHITE + str(v if v is not None else "NULL").ljust(anchos[i] + PAD)
            for i, v in enumerate(fila)
        ))


def mostrar_tabla():
    tabla = seleccionar_tabla()
    if not tabla: return
    try:
        cursor.execute(f'SELECT * FROM "{tabla}"')
        filas = cursor.fetchall()
        cursor.execute(f'PRAGMA table_info("{tabla}")')
        columnas = [row[1] for row in cursor.fetchall()]
        if not filas:
            print(Fore.YELLOW + "(Tabla vacia)")
        else:
            _imprimir_filas(columnas, filas)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def eliminar_tabla():
    tabla = seleccionar_tabla()
    if not tabla: return
    confirm = input(Fore.RED + f"Seguro que deseas eliminar '{tabla}'? (s/n): ").strip().lower()
    if confirm == "s":
        try:
            cursor.execute(f'DROP TABLE IF EXISTS "{tabla}"')
            conn.commit()
            print(Fore.GREEN + f"Tabla '{tabla}' eliminada OK")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")


def eliminar_fila():
    tabla = seleccionar_tabla()
    if not tabla: return
    id_fila = input(Fore.CYAN + "ID de la fila a eliminar: ").strip()
    try:
        cursor.execute(f'DELETE FROM "{tabla}" WHERE id = ?', (id_fila,))
        conn.commit()
        if cursor.rowcount:
            print(Fore.GREEN + f"Fila {id_fila} eliminada OK")
        else:
            print(Fore.YELLOW + "No se encontro esa fila.")
    except Exception as e:
        print(Fore.RED + f"Error: {e}")


def eliminar_columna():
    tabla = seleccionar_tabla()
    if not tabla: return
    cursor.execute(f'PRAGMA table_info("{tabla}")')
    todas    = cursor.fetchall()
    columnas = [row[1] for row in todas if row[1] != "id"]
    print(Fore.CYAN + f"Columnas: {', '.join(columnas)}")
    col = input(Fore.CYAN + "Columna a eliminar: ").strip()
    if col not in columnas:
        print(Fore.RED + "Columna no encontrada.")
        return
    confirm = input(Fore.RED + f"Eliminar columna '{col}'? (s/n): ").strip().lower()
    if confirm != "s": return
    try:
        restantes    = [row for row in todas if row[1] != col]
        cols_def     = ", ".join(
            f'"{r[1]}" {r[2]}' + (" PRIMARY KEY AUTOINCREMENT" if r[5] else "")
            for r in restantes
        )
        cols_nombres = ", ".join(f'"{r[1]}"' for r in restantes)
        cursor.execute(f'ALTER TABLE "{tabla}" RENAME TO "_tmp_{tabla}"')
        cursor.execute(f'CREATE TABLE "{tabla}" ({cols_def})')
        cursor.execute(f'INSERT INTO "{tabla}" ({cols_nombres}) SELECT {cols_nombres} FROM "_tmp_{tabla}"')
        cursor.execute(f'DROP TABLE "_tmp_{tabla}"')
        conn.commit()
        print(Fore.GREEN + f"Columna '{col}' eliminada OK")
    except Exception as e:
        conn.rollback()
        print(Fore.RED + f"Error: {e}")


def eliminar_base_de_datos():
    confirm = input(Fore.RED + f"Vaciar TODA la base de datos '{os.path.basename(DB_NAME)}'? (escribe 'CONFIRMAR'): ").strip()
    if confirm == "CONFIRMAR":
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for (t,) in cursor.fetchall():
            cursor.execute(f'DROP TABLE IF EXISTS "{t}"')
        conn.commit()
        print(Fore.GREEN + "Base de datos vaciada OK")
    else:
        print(Fore.YELLOW + "Operacion cancelada.")


def configurar_base_de_datos():
    print(Fore.CYAN + "\n Configuracion")
    print(Fore.WHITE + f"Archivo: {os.path.abspath(DB_NAME)}")
    cursor.execute("PRAGMA journal_mode")
    print(Fore.WHITE + f"Journal mode: {cursor.fetchone()[0]}")
    cursor.execute("PRAGMA foreign_keys")
    fk = cursor.fetchone()[0]
    print(Fore.WHITE + f"Foreign keys: {'ON' if fk else 'OFF'}")
    toggle = input(Fore.CYAN + "\n[1] Activar foreign keys  [2] Desactivar  [Enter] Volver: ").strip()
    if toggle == "1":
        cursor.execute("PRAGMA foreign_keys = ON")
        print(Fore.GREEN + "Foreign keys activadas OK")
    elif toggle == "2":
        cursor.execute("PRAGMA foreign_keys = OFF")
        print(Fore.GREEN + "Foreign keys desactivadas OK")


def mostrar_todas_las_tablas():
    tablas = tablas_disponibles()
    if not tablas:
        print(Fore.YELLOW + "No hay tablas en la base de datos.")
    else:
        print(Fore.GREEN + f"\nTablas en '{os.path.basename(DB_NAME)}':")
        for t in tablas:
            cursor.execute(f'SELECT COUNT(*) FROM "{t}"')
            n = cursor.fetchone()[0]
            print(Fore.WHITE + f"  - {t}  ({n} filas)")

def salir():
    print(Fore.RED + "\n\nSaliendo del programa... Hasta luego!")
    if conn:
        conn.close()
    sys.exit(0)

def CRUD():
    while True:
        try:
            ans = menu()

            if   ans == "1":  crear_tabla()
            elif ans == "2":  agregar_columna()
            elif ans == "3":  insertar_fila()
            elif ans == "4":  buscar_filas()
            elif ans == "5":  ver_columnas()
            elif ans == "6":  agregar_texto()
            elif ans == "7":  reescribir_texto()
            elif ans == "8":  mostrar_tabla()
            elif ans == "9":  eliminar_tabla()
            elif ans == "10": eliminar_fila()
            elif ans == "11": eliminar_columna()
            elif ans == "12": eliminar_base_de_datos()
            elif ans == "13": configurar_base_de_datos()
            elif ans == "14": mostrar_todas_las_tablas()
            elif ans == "15": menu_database_manager()
            elif ans == "16": salir()
            else:
                print(Fore.RED + "Opcion invalida, intenta de nuevo.")

            pausar()

        except KeyboardInterrupt:
            salir()

if __name__ == "__main__":
    try:
        menu_database_manager()
        CRUD()
    except KeyboardInterrupt:
        salir()
