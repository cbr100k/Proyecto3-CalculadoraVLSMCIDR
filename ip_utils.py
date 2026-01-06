import re
import math

def ip_a_entero(ip: str) -> int:
    """
    Convierte una dirección IP en formato string a entero de 32 bits.
    """
    octetos = ip.split('.')
    if len(octetos) != 4:
        raise ValueError("La IP debe tener 4 octetos")
    
    resultado = 0
    for i, octeto in enumerate(octetos):
        valor = int(octeto)
        if valor < 0 or valor > 255:
            raise ValueError(f"Octeto {i+1} fuera de rango (0-255)")
        resultado = (resultado << 8) | valor
    
    return resultado

def entero_a_ip(entero: int) -> str:
    """
    Convierte un entero de 32 bits a dirección IP en formato string.
    """
    if entero < 0 or entero > 0xFFFFFFFF:
        raise ValueError("Entero fuera de rango para dirección IP")
    
    octetos = []
    for i in range(3, -1, -1):
        octeto = (entero >> (8 * i)) & 0xFF
        octetos.append(str(octeto))
    
    return ".".join(octetos)

def mascara_a_prefijo(mascara: str) -> int:
    """
    Convierte máscara en formato decimal punteado a prefijo CIDR.
    """
    entero = ip_a_entero(mascara)
    
    # Verificar que sea una máscara válida
    binario = bin(entero)[2:].zfill(32)
    
    # Buscar transición de 1 a 0
    encontrado_cero = False
    for bit in binario:
        if bit == '0':
            encontrado_cero = True
        elif encontrado_cero and bit == '1':
            raise ValueError("Máscara inválida: los 1s deben ser contiguos")
    
    return binario.count('1')

def prefijo_a_mascara(prefijo: int) -> str:
    """
    Convierte prefijo CIDR a máscara en formato decimal punteado.
    """
    if prefijo < 0 or prefijo > 32:
        raise ValueError("Prefijo debe estar entre 0 y 32")
    
    mascara_entero = (0xFFFFFFFF << (32 - prefijo)) & 0xFFFFFFFF
    return entero_a_ip(mascara_entero)

def validar_ip(ip: str) -> bool:
    """
    Valida que una dirección IP sea correcta.
    """
    patron = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
    match = re.match(patron, ip)
    
    if not match:
        return False
    
    for grupo in match.groups():
        if int(grupo) > 255:
            return False
    
    return True

def validar_prefijo(prefijo: str) -> bool:
    """
    Valida que un prefijo CIDR sea correcto.
    """
    try:
        p = int(prefijo)
        return 0 <= p <= 32
    except ValueError:
        return False

def obtener_binario_ip(ip: str) -> str:
    """
    Obtiene la representación binaria de una IP.
    """
    octetos = ip.split('.')
    binarios = [bin(int(o))[2:].zfill(8) for o in octetos]
    return ".".join(binarios)