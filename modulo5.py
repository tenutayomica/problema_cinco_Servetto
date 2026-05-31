import os
from modulo1 import crear_archivo_pacientes, TAM_REGISTRO
from modulo2 import construir_indices, buscar_por_dni
from modulo3 import listar_pacientes_ordenados
from modulo4 import asignar_agenda

def ejecutar_pruebas_y_demo():
    ruta_db = "pacientes.dat"
    
    # Datos de prueba para inicializar el archivo binario
    # Estructura: (dni, apellido, nombre, telefono, prioridad)
    pacientes_iniciales = [
        (48313594, "Gomez", "Juan", "112233", 2),
        (22337719, "Lopez", "Ana", "445566", 1),
        (33333455, "Lepera", "Luis", "778899", 1),
        (44444444, "Zarate", "Maria", "001122", 3),
    ]
    
    print("--- [Módulo 1] Inicializando Persistencia Binaria ---")
    crear_archivo_pacientes(ruta_db, pacientes_iniciales)
    # Verificación del tamaño físico esperado
    tam_esperado = len(pacientes_iniciales) * TAM_REGISTRO
    tam_real = os.path.getsize(ruta_db)
    print(f"Tamaño esperado en disco: {tam_esperado} bytes. Real: {tam_real} bytes.")
    assert tam_esperado == tam_real, "Error en la persistencia del tamaño binario."
    
    print("\n--- [Módulo 2] Construyendo Índices en Memoria ---")
    indice_dni, indice_ape = construir_indices(ruta_db)
    print(f"Índice DNI generado: {indice_dni}")
    print(f"Índice Apellido generado: {indice_ape}")
    
    # Definición de la agenda y disponibilidades para el Módulo 4
    franjas_consultorio = ["08:00", "08:30", "09:00", "09:30"]
    pacientes_del_dia = [48313594, 22337719, 33333455] 
    
    # Caso 1: Caso Con Solución
    disponibilidad_viable = {
        1111: ["08:00", "08:30"],
        2222: ["08:00"],
        3333: ["09:00", "09:30"]
    }
    
    # Caso 2: Caso Sobre-restringido 
    disponibilidad_inviable = {
        1111: ["08:00"],
        2222: ["08:00"], 
        3333: ["09:00"]
    }

    # Interfaz de Menú 
    while True:
        print("\n========================================")
        print("SISTEMA DE GESTIÓN DE TURNOS MÉDICOS")
        print("========================================")
        print("1. Buscar paciente por DNI (O(1))")
        print("2. Reporte: Pacientes ordenados por Apellido")
        print("3. Reporte: Pacientes ordenados por Prioridad (y Apellido)")
        print("4. Resolver Agenda Diaria (Backtracking) - Caso Exitoso")
        print("5. Resolver Agenda Diaria (Backtracking) - Caso Sobre-restringido")
        print("6. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            try:
                target_dni = int(input("Ingrese el DNI a buscar: "))
                with open(ruta_db, 'rb') as f:
                    resultado = buscar_por_dni(f, indice_dni, target_dni)
                if resultado:
                    print(f"Paciente Encontrado: DNI={resultado[0]}, Apellido={resultado[1]}, Nombre={resultado[2]}, Teléfono={resultado[3]}, Prioridad={resultado[4]}")
                else:
                    print("El DNI ingresado no se encuentra en el sistema.")
            except ValueError:
                print("Por favor, ingrese un DNI numérico válido.")
                
        elif opcion == "2":
            print("\nReporte Alfabético de Pacientes:")
            reporte = listar_pacientes_ordenados(ruta_db, "apellido")
            for p in reporte:
                print(f"- {p[1]}, {p[2]} (DNI: {p[0]})")
                
        elif opcion == "3":
            print("\nReporte por Prioridad (Desempate por Apellido):")
            reporte = listar_pacientes_ordenados(ruta_db, "prioridad")
            for p in reporte:
                print(f"- [Prioridad {p[4]}] {p[1]}, {p[2]}")
                
        elif opcion == "4":
            print("\nProcesando asignación para el Caso Exitoso...")
            agenda_resuelta = asignar_agenda(pacientes_del_dia, franjas_consultorio, disponibilidad_viable)
            if agenda_resuelta:
                print("Agenda diaria asignada con éxito:")
                for franja, dni in sorted(agenda_resuelta.items()):
                    print(f"  * {franja} -> Paciente DNI: {dni}")
            else:
                print("No se encontró ninguna combinación horaria válida.")
                
        elif opcion == "5":
            print("\nProcesando asignación para el Caso Sobre-restringido...")
            agenda_resuelta = asignar_agenda(pacientes_del_dia, franjas_consultorio, disponibilidad_inviable)
            if agenda_resuelta:
                print("Agenda diaria asignada:", agenda_resuelta)
            else:
                print("Resultado Exitoso: El sistema de backtracking detectó correctamente que no existe una solución válida debido a las restricciones de horario.")
                
        elif opcion == "6":
            print("Saliendo del sistema de gestión médica...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    ejecutar_pruebas_y_demo()