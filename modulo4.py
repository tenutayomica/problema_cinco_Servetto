def asignar_agenda(pacientes_del_dia: list, franjas: list, disponibilidad: dict) -> dict or None:
    """
    Asigna mediante backtracking cada paciente a una franja horaria respetando las restricciones.
    
    - disponibilidad: Diccionario { paciente_dni: [lista_de_franjas_compatibles] }
    - Devuelve: Un diccionario { franja: paciente_dni } si hay solución, o None si no existe.
    """
    # Representamos nuestro estado parcial como un diccionario: { franja: paciente_dni }
    asignacion_inicial = {}
    
    def _backtracking(idx_paciente, estado_actual):
        # Caso Base: Si ya procesamos a todos los pacientes con éxito, encontramos una solución válida
        if idx_paciente == len(pacientes_del_dia):
            return estado_actual.copy()
            
        dni_actual = pacientes_del_dia[idx_paciente]
        franjas_compatibles = disponibilidad.get(dni_actual, [])
        
        for franja in franjas_compatibles:
            # Condición 1: Comprobar que la franja pertenezca a la agenda del consultorio
            # Condición 2: Comprobar que la franja no esté ya ocupada por otro paciente
            if franja in franjas and franja not in estado_actual:
                
                # Acción: Tomar la decisión (Asignar)
                estado_actual[franja] = dni_actual
                
                # Recursión: Pasar al siguiente paciente
                resultado = _backtracking(idx_paciente + 1, estado_actual)
                if resultado is not None:
                    return resultado # Propagar el éxito hacia arriba
                
                # Backtrack: Deshacer la decisión si no condujo a una solución válida
                del estado_actual[franja]
                
        return None # Agotó las opciones para este camino sin éxito

    return _backtracking(0, asignacion_inicial)

# Validación Módulo 4

if __name__ == "__main__":
    print("=== Validando Módulo 4: Agenda y Backtracking ===")
    
    franjas_test = ["08:00", "08:30", "09:00"]
    pacientes_test = [111, 222]
    dispo_test = {111: ["08:00"], 222: ["08:00", "08:30"]}
    
    asignacion = asignar_agenda(pacientes_test, franjas_test, dispo_test)
    assert asignacion is not None, "Error: Debería existir una solución válida."
    
    # Verificar manualmente disponibilidad y unicidad
    pacientes_asignados = list(asignacion.values())
    
    # 1. Verificación de Unicidad (No hay colisiones de franjas ni pacientes duplicados)
    assert len(pacientes_asignados) == len(set(pacientes_asignados)), "ERROR: Hay pacientes duplicados en diferentes franjas."
    
    # 2. Verificación de Disponibilidad
    for franja, dni in asignacion.items():
        assert franja in franjas_test, "Error: Se asignó una franja inválida."
        assert franja in dispo_test[dni], f"Error: El paciente {dni} no está disponible en la franja {franja}."
        
    print("Módulo 4 validado exitosamente.\n")