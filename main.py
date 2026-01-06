from cidr_calculator import CalculadoraCIDR
from vlsm_calculator import CalculadoraVLSM
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "="*50)
    print("CALCULADORAS DE RED - CIDR y VLSM")
    print("="*50)
    print("1. Calculadora CIDR")
    print("2. Calculadora VLSM")
    print("3. Ejecutar casos de prueba")
    print("4. Acerca del proyecto")
    print("5. Salir")
    print("="*50)

def ejecutar_casos_prueba():
    print("\n" + "="*50)
    print("CASOS DE PRUEBA")
    print("="*50)
    
    # Caso de prueba CIDR
    print("\n1. CASO CIDR: 192.168.10.0/24")
    print("-" * 40)
    try:
        cidr = CalculadoraCIDR("192.168.10.0/24")
        resultados = cidr.calcular()
        cidr.imprimir_resultados(resultados)
    except Exception as e:
        print(f"Error: {e}")
    
    # Caso de prueba VLSM
    print("\n2. CASO VLSM: 192.168.0.0/24 con A=100, B=50, C=25, D=10")
    print("-" * 40)
    try:
        vlsm = CalculadoraVLSM()
        vlsm.configurar_red_base("192.168.0.0/24")
        vlsm.agregar_subred("A", 100)
        vlsm.agregar_subred("B", 50)
        vlsm.agregar_subred("C", 25)
        vlsm.agregar_subred("D", 10)
        vlsm.calcular_vlsm()
        vlsm.imprimir_resultados()
    except Exception as e:
        print(f"Error: {e}")
    
    # Caso límite VLSM
    print("\n3. CASO LÍMITE VLSM: Red pequeña con muchos hosts")
    print("-" * 40)
    try:
        vlsm2 = CalculadoraVLSM()
        vlsm2.configurar_red_base("192.168.0.0/30")  # Solo 4 direcciones
        vlsm2.agregar_subred("S1", 10)  # Requiere 12 direcciones
        vlsm2.calcular_vlsm()
        vlsm2.imprimir_resultados()
    except ValueError as e:
        print(f"Error esperado: {e}")
    
    input("\nPresione Enter para continuar...")

def mostrar_acerca():
    """Muestra información sobre el proyecto."""
    limpiar_pantalla()
    print("\n" + "="*50)
    print("ACERCA DEL PROYECTO")
    print("="*50)
    print("\nCalculadoras de Red - CIDR y VLSM")
    print("Proyecto 3: Redes de Computadoras")
    print("\nIntegrantes del equipo:")
    print("- Blanco Resendiz Cuauhtemoc - 2024630579")
    print("\nFuncionalidades:")
    print("• Calculadora CIDR completa")
    print("• Calculadora VLSM")
    print("• Validación de entradas")
    print("• Manejo de errores")
    print("• Interfaz de consola")
    print("\nInstrucciones:")
    print("1. Ejecutar: python main.py")
    print("2. Seleccionar opción del menú")
    print("3. Seguir las instrucciones en pantalla")
    print("\n" + "="*50)
    input("\nPresione Enter para continuar...")

def main():
    """Función principal del programa."""
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("\nSeleccione una opción (1-5): ").strip()
        
        if opcion == '1':
            limpiar_pantalla()
            cidr = CalculadoraCIDR()
            cidr.ejecutar_desde_consola()
        
        elif opcion == '2':
            limpiar_pantalla()
            vlsm = CalculadoraVLSM()
            vlsm.ejecutar_desde_consola()
        
        elif opcion == '3':
            limpiar_pantalla()
            ejecutar_casos_prueba()
        
        elif opcion == '4':
            mostrar_acerca()
        
        elif opcion == '5':
            limpiar_pantalla()
            print("\n¡Gracias por usar las Calculadoras de Red!")
            print("Hasta luego.\n")
            break
        
        else:
            print("\nOpción inválida. Intente nuevamente.")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError inesperado: {e}")