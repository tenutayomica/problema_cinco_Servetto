import os
from modulo1 import TAM_REGISTRO, desempaquetar_paciente, leer_paciente, crear_archivo_pacientes

def construir_indices(ruta: str) -> tuple:
    """
    Recorre el archivo binario una sola vez para construir los índices.
    
    Precondición: El archivo en 'ruta' existe y está estructurado bajo el FORMATO global.
    Postcondición: Devuelve una tupla con dos diccionarios: (indice_por_dni, indice_por_apellido).
    """
    indice_por_dni = {}
    indice_por_apellido = {}
    
    if not os.path.exists(ruta):
        return indice_por_dni, indice_por_apellido

    with open(ruta, 'rb') as archivo:
        k = 0
        while True:
            registro_bytes = archivo.read(TAM_REGISTRO)
            if len(registro_bytes) < TAM_REGISTRO:
                break # Fin del archivo
            
            dni, apellido, _, _, _ = desempaquetar_paciente(registro_bytes)
            
            # El DNI es único: mapeo directo a la posición k
            indice_por_dni[dni] = k
            
            # El apellido puede repetirse: mapeo a una lista de posiciones k
            if apellido not in indice_por_apellido:
                indice_por_apellido[apellido] = []
            indice_por_apellido[apellido].append(k)
            
            k += 1
            
    return indice_por_dni, indice_por_apellido

def buscar_por_dni(archivo, indice_por_dni: dict, dni: int) -> tuple:
    """
    Resuelve la búsqueda de un paciente por DNI de manera eficiente utilizando el índice.
    
    Concepto y Costo (Docstring):
    Esta función logra un costo de O(1) promedio para localizar la posición del registro. 
    Al buscar la clave en el diccionario (tabla de hash), obtenemos de forma inmediata el 
    índice 'k'. Luego se realiza una única operación de lectura física en disco 
    usando 'seek', cuyo costo es independiente de la cantidad de registros (N).
    
    En contraste, una búsqueda secuencial sin índices sobre el archivo binario nos obligaría 
    a leer e inspeccionar uno por uno los registros desde el principio hasta encontrar la 
    coincidencia o el fin del archivo. Esto conllevaría un costo de peor caso y promedio de O(n), 
    lo cual penaliza críticamente el rendimiento del sistema a medida que el volumen de 
    datos crece (N operaciones de E/S en disco frente a 1 sola operación con índice).
    
    Precondición: 'archivo' está abierto en modo 'rb'. indice_por_dni contiene las posiciones mapeadas.
    Postcondición: Devuelve la tupla del paciente si se encuentra; None si no existe en el índice.
    """
    if dni not in indice_por_dni:
        return None
    
    posicion_k = indice_por_dni[dni]
    return leer_paciente(archivo, posicion_k)

# Validación Módulo 2

if __name__ == "__main__":
    
    print("=== Validando Módulo 2: Índices y Búsqueda Eficiente ===")
    
    ruta_test = "test_indices.dat"
    pacientes_test = [(999, "Test", "Paciente", "000", 1)]
    crear_archivo_pacientes(ruta_test, pacientes_test)
    
    idx_dni, _ = construir_indices(ruta_test)
    
    # Comprobar que toda búsqueda por DNI devuelve el registro correcto
    with open(ruta_test, 'rb') as f:
        resultado = buscar_por_dni(f, idx_dni, 999)
        assert resultado is not None, "Error: No se encontró el DNI indexado."
        assert resultado[0] == 999 and resultado[1] == "Test", "Error: Los datos recuperados son incorrectos."
        
        # Comprobar camino de falla
        resultado_inexistente = buscar_por_dni(f, idx_dni, 12345)
        assert resultado_inexistente is None, "Error: Se devolvió un registro para un DNI inexistente."
        
    print("Módulo 2 validado exitosamente.\n")
    if os.path.exists(ruta_test):
        os.remove(ruta_test)