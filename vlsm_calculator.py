from ip_utils import *
import math


class CalculadoraVLSM:
    """
    Calculadora para VLSM (Variable Length Subnet Masking).
    """
    
    def __init__(self):
        self.red_base = None
        self.prefijo_base = None
        self.subredes = []
        self.resultados = []
    
    def configurar_red_base(self, red_base: str):
        """
        Configura la red base para el cálculo VLSM.
        """
        if '/' not in red_base:
            raise ValueError("Formato incorrecto. Use: IP/prefijo (ej: 10.0.0.0/16)")
        
        partes = red_base.split('/')
        ip = partes[0].strip()
        prefijo_str = partes[1].strip()
        
        if not validar_ip(ip):
            raise ValueError("Dirección IP inválida")
        
        try:
            prefijo = int(prefijo_str)
        except ValueError:
            raise ValueError("Prefijo debe ser un número")
        
        if not 0 <= prefijo <= 32:
            raise ValueError("Prefijo debe estar entre 0 y 32")
        
        self.red_base = ip
        self.prefijo_base = prefijo
    
    def agregar_subred(self, nombre: str, hosts_requeridos: int):
        """
        Agrega una subred a la lista de requerimientos.
        """
        if hosts_requeridos <= 0:
            raise ValueError("El número de hosts debe ser mayor a 0")
        
        self.subredes.append({
            "nombre": nombre,
            "hosts_requeridos": hosts_requeridos
        })
    
    def calcular_vlsm(self):
        """
        Ejecuta el algoritmo VLSM y calcula las asignaciones.
        """
        if not self.red_base or self.prefijo_base is None:
            raise ValueError("Debe configurar la red base primero")
        
        if not self.subredes:
            raise ValueError("Debe agregar al menos una subred")
        
        # 1. Preparar lista: calcular hosts_necesarios (hosts + 2)
        for subred in self.subredes:
            subred["hosts_necesarios"] = subred["hosts_requeridos"] + 2
        
        # 2. Ordenar subredes por tamaño descendente
        subredes_ordenadas = sorted(self.subredes, 
                                    key=lambda x: x["hosts_necesarios"], 
                                    reverse=True)
        
        # 3. Inicializar puntero
        ip_actual_entero = ip_a_entero(self.red_base)
        espacio_total = 2 ** (32 - self.prefijo_base)
        limite_superior = ip_actual_entero + espacio_total
        
        self.resultados = []
        
        # 4. Asignar subredes
        for subred in subredes_ordenadas:
            # Calcular bits de host necesarios
            bits_host = math.ceil(math.log2(subred["hosts_necesarios"]))
            bits_red = 32 - bits_host
            
            # Calcular tamaño del bloque
            bloque = 2 ** bits_host
            
            # Verificar que haya espacio suficiente
            if ip_actual_entero + bloque > limite_superior:
                raise ValueError(
                    f"No hay espacio suficiente para la subred '{subred['nombre']}'. "
                    f"Espacio insuficiente en la red base."
                )
            
            # Calcular propiedades de la subred
            red = entero_a_ip(ip_actual_entero)
            broadcast_entero = ip_actual_entero + bloque - 1
            broadcast = entero_a_ip(broadcast_entero)
            
            # Calcular primer y último host (excepto para /31 y /32)
            if bits_red == 32:  # /32
                primer_host = red
                ultimo_host = red
                hosts_validos = 1
            elif bits_red == 31:  # /31 (RFC 3021)
                primer_host = red
                ultimo_host = broadcast
                hosts_validos = 2
            else:
                primer_host_entero = ip_actual_entero + 1
                ultimo_host_entero = broadcast_entero - 1
                primer_host = entero_a_ip(primer_host_entero)
                ultimo_host = entero_a_ip(ultimo_host_entero)
                hosts_validos = ultimo_host_entero - primer_host_entero + 1
            
            # Calcular desperdicio
            desperdicio = bloque - hosts_validos if bits_red < 31 else 0
            
            # Guardar resultados
            self.resultados.append({
                "nombre": subred["nombre"],
                "hosts_requeridos": subred["hosts_requeridos"],
                "red": red,
                "prefijo": bits_red,
                "mascara": prefijo_a_mascara(bits_red),
                "broadcast": broadcast,
                "primer_host": primer_host,
                "ultimo_host": ultimo_host,
                "hosts_validos": hosts_validos,
                "tam_bloque": bloque,
                "desperdicio": desperdicio,
                "rango_hosts": f"{primer_host} - {ultimo_host}",
                "notacion_cidr": f"{red}/{bits_red}"
            })
            
            # Actualizar puntero
            ip_actual_entero += bloque
        
        # 5. Calcular espacio restante
        self.espacio_usado = ip_actual_entero - ip_a_entero(self.red_base)
        self.espacio_total = espacio_total
        self.espacio_restante = espacio_total - self.espacio_usado
        
        return self.resultados
    
    def imprimir_resultados(self):
        """
        Imprime los resultados del cálculo VLSM
        """
        if not self.resultados:
            print("No hay resultados para mostrar. Ejecute calcular_vlsm() primero.")
            return
        
        print("\n" + "="*70)
        print("RESULTADOS CALCULADORA VLSM")
        print("="*70)
        print(f"Red base: {self.red_base}/{self.prefijo_base}")
        print(f"Espacio total: {self.espacio_total} direcciones")
        print(f"Espacio usado: {self.espacio_usado} direcciones")
        print(f"Espacio restante: {self.espacio_restante} direcciones")
        print("="*70)
        
        for i, subred in enumerate(self.resultados, 1):
            print(f"\nSubred {i}: {subred['nombre']}")
            print("-" * 40)
            print(f"  Hosts requeridos:  {subred['hosts_requeridos']}")
            print(f"  Dirección de red:  {subred['notacion_cidr']}")
            print(f"  Máscara:           {subred['mascara']} (/{subred['prefijo']})")
            print(f"  Rango de hosts:    {subred['rango_hosts']}")
            print(f"  Broadcast:         {subred['broadcast']}")
            print(f"  Hosts válidos:     {subred['hosts_validos']}")
            print(f"  Tamaño de bloque:  {subred['tam_bloque']} direcciones")
            print(f"  Desperdicio:       {subred['desperdicio']} direcciones")
        
        print("\n" + "="*70)
        print("RESUMEN")
        print("="*70)
        
        # Tabla resumen
        print(f"\n{'No.':<4} {'Subred':<15} {'Red':<18} {'Hosts Req.':<12} {'Hosts Disp.':<12} {'Desperdicio':<12}")
        print("-" * 75)
        
        for i, subred in enumerate(self.resultados, 1):
            print(f"{i:<4} {subred['nombre']:<15} {subred['notacion_cidr']:<18} "
                  f"{subred['hosts_requeridos']:<12} {subred['hosts_validos']:<12} "
                  f"{subred['desperdicio']:<12}")
        
        print("-" * 75)
        print(f"\nTotal hosts requeridos: {sum(s['hosts_requeridos'] for s in self.resultados)}")
        print(f"Total hosts disponibles: {sum(s['hosts_validos'] for s in self.resultados)}")
        print(f"Total desperdicio: {sum(s['desperdicio'] for s in self.resultados)} direcciones")
        print("="*70 + "\n")
    
    def ejecutar_desde_consola(self):
        """
        Interfaz de consola para la calculadora VLSM.
        """
        print("\n" + "="*50)
        print("CALCULADORA VLSM")
        print("="*50)
        
        # Configurar red base
        while True:
            red_base = input("Ingrese red base (ej: 192.168.0.0/24): ").strip()
            try:
                self.configurar_red_base(red_base)
                break
            except ValueError as e:
                print(f"Error: {e}")
        
        # Configurar subredes
        self.subredes = []
        print("\nIngrese las subredes (nombre y número de hosts requeridos)")
        print("Ingrese 'fin' cuando termine")
        
        while True:
            nombre = input("\nNombre de la subred (o 'fin'): ").strip()
            if nombre.lower() == 'fin':
                if not self.subredes:
                    print("Debe agregar al menos una subred.")
                    continue
                break
            
            try:
                hosts = input(f"Número de hosts para '{nombre}': ").strip()
                hosts_int = int(hosts)
                self.agregar_subred(nombre, hosts_int)
                print(f"Subred '{nombre}' agregada con {hosts_int} hosts.")
            except ValueError as e:
                print(f"Error: {e}")
        
        # Calcular VLSM
        try:
            print("\nCalculando asignaciones VLSM...")
            self.calcular_vlsm()
            self.imprimir_resultados()
        except ValueError as e:
            print(f"\nError en el cálculo: {e}")

if __name__ == "__main__":
    calculadora = CalculadoraVLSM()
    calculadora.ejecutar_desde_consola()