import os
from modulo1 import TAM_REGISTRO, desempaquetar_paciente

def _merge(izq: list, der: list, clave_idx: int) -> list:
    """Función auxiliar para fusionar de forma estable dos sublistas ordenadas."""
    resultado = []
    i, j = 0, 0
    while i < len(izq) and j < len(der):
        # El operador '<=' preserva el orden relativo de elementos idénticos (Estabilidad)
        if izq[i][clave_idx] <= der[j][clave_idx]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

def merge_sort(lista: list, clave_idx: int) -> list:
    """
    Ordena una lista de tuplas mediante Divide y Vencerás utilizando un índice como criterio.
    Complejidad: O(n log n) tiempo, O(n) espacio auxiliar.
    """
    if len(lista) <= 1:
        return lista
    
    medio = len(lista) // 2
    mitad_izq = merge_sort(lista[:medio], clave_idx)
    mitad_der = merge_sort(lista[medio:], clave_idx)
    
    return _merge(mitad_izq, mitad_der, clave_idx)

def listar_pacientes_ordenados(ruta: str, criterio: str) -> list:
    """
    Lee todos los pacientes del archivo y devuelve una lista ordenada bajo el criterio establecido.
    
    Criterios válidos: "apellido" o "prioridad".
    """
    pacientes = []
    if not os.path.exists(ruta):
        return pacientes

    with open(ruta, 'rb') as archivo:
        while True:
            registro_bytes = archivo.read(TAM_REGISTRO)
            if len(registro_bytes) < TAM_REGISTRO:
                break
            pacientes.append(desempaquetar_paciente(registro_bytes))
            
    if criterio == "apellido":
        # Índice 1 corresponde al campo 'apellido'
        return merge_sort(pacientes, clave_idx=1)
        
    elif criterio == "prioridad":
        # Procedimiento de dos pasadas aprovechando la estabilidad:
        # Pasada 1: Ordenar alfabéticamente por apellido (criterio secundario / de desempate)
        pacientes_ordenados_apellido = merge_sort(pacientes, clave_idx=1)
        # Pasada 2: Ordenar numéricamente por prioridad (criterio primario)
        return merge_sort(pacientes_ordenados_apellido, clave_idx=4)
    else:
        raise ValueError("Criterio de ordenamiento no válido.")