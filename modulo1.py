import struct
import os

# --- Constantes globales ---
FORMATO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO)

def empaquetar_paciente(dni: int, apellido: str, nombre: str, telefono: str, prioridad: int) -> bytes:
    """
    Empaqueta los datos de un paciente en un registro binario de longitud fija.
    
    Precondición: dni e i son enteros; apellido, nombre y telefono son cadenas.
                  prioridad está entre 1 y 3.
    Postcondición: Devuelve un bloque de bytes de tamaño TAM_REGISTRO con codificación UTF-8
                   y truncamiento/relleno según corresponda.
    """
    # Codificar cadenas a UTF-8 y truncar para no exceder el formato de struct
    apellido_bytes = apellido.encode('utf-8')[:30]
    nombre_bytes = nombre.encode('utf-8')[:24]
    telefono_bytes = telefono.encode('utf-8')[:16]
    
    return struct.pack(FORMATO, dni, apellido_bytes, nombre_bytes, telefono_bytes, prioridad)

def desempaquetar_paciente(registro_bytes: bytes) -> tuple:
    """
    Desempaquetar un registro binario y recupera los datos limpios del paciente.
    
    Precondición: registro_bytes tiene una longitud igual a TAM_REGISTRO.
    Postcondición: Devuelve una tupla (dni, apellido, nombre, telefono, prioridad) 
                   removiendo el relleno de ceros y decodificando a string de python.
    """
    dni, apellido_b, nombre_b, telefono_b, prioridad = struct.unpack(FORMATO, registro_bytes)
    
    # Decodificar removiendo los bytes nulos del padding
    apellido = apellido_b.decode('utf-8').rstrip('\x00')
    nombre = nombre_b.decode('utf-8').rstrip('\x00')
    telefono = telefono_b.decode('utf-8').rstrip('\x00')
    
    return (dni, apellido, nombre, telefono, prioridad)

def crear_archivo_pacientes(ruta: str, lista_pacientes: list) -> None:
    """
    Crea o sobrescribe un archivo binario a partir de una lista de pacientes en memoria.
    
    Precondición: lista_pacientes es una lista de tuplas o diccionarios con los datos requeridos.
    Postcondición: El archivo en 'ruta' contendrá los registros empaquetados secuencialmente.
    """
    with open(ruta, 'wb') as archivo:
        for p in lista_pacientes:
            # Se asume que p es una tupla: (dni, apellido, nombre, telefono, prioridad)
            bloque = empaquetar_paciente(p[0], p[1], p[2], p[3], p[4])
            archivo.write(bloque)

def leer_paciente(archivo, k: int) -> tuple:
    """
    Lee el k-ésimo paciente de un archivo binario usando acceso directo por offset.
    
    Precondición: archivo es un file object abierto en modo 'rb'. 
                  k es un entero no negativo que representa el índice del registro.
    Postcondición: Devuelve la tupla de datos del paciente desempaquetado. 
                   Si k está fuera de rango, levanta un IndexError.
    """
    archivo.seek(k * TAM_REGISTRO)
    registro_bytes = archivo.read(TAM_REGISTRO)
    if len(registro_bytes) < TAM_REGISTRO:
        raise IndexError("El índice del registro solicitado está fuera de los límites del archivo.")
    return desempaquetar_paciente(registro_bytes)

# Validación Módulo 1

if __name__ == "__main__":

    print("=== Validando Módulo 1: Persistencia Binaria ===")
    
    ruta_test = "test_pacientes.dat"
    pacientes_test = [
        (111, "Gomez", "Juan", "123", 2),
        (222, "Lopez", "Ana", "456", 1)
    ]
    
    # Ejecutamos la función a probar
    crear_archivo_pacientes(ruta_test, pacientes_test)
    
    # Verificar que os.path.getsize coincide con cantidad * TAM_REGISTRO
    tam_esperado = len(pacientes_test) * TAM_REGISTRO
    tam_real = os.path.getsize(ruta_test)
    
    print(f"Tamaño esperado: {tam_esperado} bytes | Real: {tam_real} bytes.")
    assert tam_real == tam_esperado, "ERROR: El tamaño físico en disco no coincide."
    print("Módulo 1 validado exitosamente.\n")
    
    # Limpieza
    if os.path.exists(ruta_test):
        os.remove(ruta_test)