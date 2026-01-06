from ip_utils import *
import math

    
class CalculadoraCIDR:
    """
    Calculadora para operaciones CIDR
    """
    
    def __init__(self, ip_con_prefijo: str = None):
        self.ip = None
        self.prefijo = None
        self.mascara = None
        
        if ip_con_prefijo:
            self.analizar_entrada(ip_con_prefijo)
    
    def analizar_entrada(self, entrada: str):
        entrada = entrada.strip()
        
        # Formato: IP/prefijo
        if '/' in entrada:
            partes = entrada.split('/')
            if len(partes) != 2:
                raise ValueError("Formato incorrecto. Use: IP/prefijo o IP máscara")
            
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
            
            self.ip = ip
            self.prefijo = prefijo
            self.mascara = prefijo_a_mascara(prefijo)
        
        # Formato: IP máscara
        else:
            partes = entrada.split()
            if len(partes) != 2:
                raise ValueError("Formato incorrecto. Use: IP/prefijo o IP máscara")
            
            ip = partes[0].strip()
            mascara = partes[1].strip()
            
            if not validar_ip(ip):
                raise ValueError("Dirección IP inválida")
            
            if not validar_ip(mascara):
                raise ValueError("Máscara inválida")
            
            try:
                prefijo = mascara_a_prefijo(mascara)
            except ValueError as e:
                raise ValueError(f"Máscara inválida: {e}")
            
            self.ip = ip
            self.prefijo = prefijo
            self.mascara = mascara
    
    def calcular(self):
        """
        Calcula todas las propiedades de la red CIDR.
        """
        if not self.ip or self.prefijo is None:
            raise ValueError("Debe proporcionar una IP y prefijo primero")
        
        ip_entero = ip_a_entero(self.ip)
        mascara_entero = ip_a_entero(self.mascara) if self.mascara else (0xFFFFFFFF << (32 - self.prefijo)) & 0xFFFFFFFF
        
        # Calcular dirección de red
        red_entero = ip_entero & mascara_entero
        red = entero_a_ip(red_entero)
        
        # Calcular broadcast
        wildcard = mascara_entero ^ 0xFFFFFFFF
        broadcast_entero = red_entero | wildcard
        broadcast = entero_a_ip(broadcast_entero)
        
        # Calcular primer y último host
        if self.prefijo == 32:
            primer_host = red
            ultimo_host = red
            hosts_validos = 1
        elif self.prefijo == 31:
            # Caso especial: /31 (RFC 3021)
            primer_host = red
            ultimo_host = broadcast
            hosts_validos = 2
        else:
            primer_host_entero = red_entero + 1
            ultimo_host_entero = broadcast_entero - 1
            primer_host = entero_a_ip(primer_host_entero)
            ultimo_host = entero_a_ip(ultimo_host_entero)
            hosts_validos = ultimo_host_entero - primer_host_entero + 1
        
        # Calcular número total de hosts
        if self.prefijo == 32:
            total_hosts = 1
        else:
            total_hosts = 2 ** (32 - self.prefijo)
        
        # Calcular desperdicio
        desperdicio = total_hosts - hosts_validos if self.prefijo < 31 else 0
        
        # Representaciones binarias
        bin_ip = obtener_binario_ip(self.ip)
        bin_mascara = obtener_binario_ip(self.mascara)
        bin_red = obtener_binario_ip(red)
        
        return {
            "ip_original": self.ip,
            "prefijo": self.prefijo,
            "mascara": self.mascara,
            "red": red,
            "broadcast": broadcast,
            "primer_host": primer_host,
            "ultimo_host": ultimo_host,
            "hosts_validos": hosts_validos,
            "total_hosts": total_hosts,
            "desperdicio": desperdicio,
            "bin_ip": bin_ip,
            "bin_mascara": bin_mascara,
            "bin_red": bin_red,
            "rango_hosts": f"{primer_host} - {ultimo_host}",
            "notacion_cidr": f"{red}/{self.prefijo}"
        }
    
    def imprimir_resultados(self, resultados: dict):
        print("\n" + "="*50)
        print("RESULTADOS CALCULADORA CIDR")
        print("="*50)
        print(f"IP original:      {resultados['ip_original']}")
        print(f"Notación CIDR:    {resultados['notacion_cidr']}")
        print(f"Máscara:          {resultados['mascara']} (/{resultados['prefijo']})")
        print(f"Dirección de red: {resultados['red']}")
        print(f"Broadcast:        {resultados['broadcast']}")
        print(f"Rango de hosts:   {resultados['rango_hosts']}")
        print(f"Hosts válidos:    {resultados['hosts_validos']}")
        print(f"Total direcciones: {resultados['total_hosts']}")
        print(f"Desperdicio:      {resultados['desperdicio']} direcciones")
        print("-"*50)
        print("REPRESENTACIÓN BINARIA")
        print(f"IP:       {resultados['bin_ip']}")
        print(f"Máscara:  {resultados['bin_mascara']}")
        print(f"Red:      {resultados['bin_red']}")
        print("="*50 + "\n")
    
    def ejecutar_desde_consola(self):
        """
        Interfaz de consola para la calculadora CIDR.
        """
        print("\n" + "="*50)
        print("CALCULADORA CIDR")
        print("="*50)
        print("Formato de entrada:")
        print("1. IP/prefijo (ej: 192.168.1.0/24)")
        print("2. IP máscara (ej: 192.168.1.0 255.255.255.0)")
        print("="*50)
        
        while True:
            entrada = input("\nIngrese dirección IP con prefijo o máscara (o 'salir'): ").strip()
            
            if entrada.lower() == 'salir':
                break
            
            try:
                self.analizar_entrada(entrada)
                resultados = self.calcular()
                self.imprimir_resultados(resultados)
            except ValueError as e:
                print(f"Error: {e}")
                print("Intente nuevamente.")

if __name__ == "__main__":
    calculadora = CalculadoraCIDR()
    calculadora.ejecutar_desde_consola()