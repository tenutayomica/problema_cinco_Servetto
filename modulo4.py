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