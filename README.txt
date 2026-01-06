PROYECTO 3: CALCULADORA IP - CIDR Y VLSM
=========================================

DESCRIPCION

Este proyecto implementa dos calculadoras de red en Python:

Calculadora CIDR y Calculadora VLSM

AUTORES

Blanco Resendiz Cuauhtemoc - 2024630579
--------------------------------------------------------

INSTITUCION

Instituto Politecnico Nacional
Escuela Superior de Computo
Materia: Redes de Computadoras
Profesor: Alcaraz Torres Juan Jesus

REQUISITOS DEL SISTEMA

Python 3.6 o superior

Sistema operativo: Windows

Aprox. 50 MB de espacio libre en disco
--------------------------------------------------------

ARCHIVOS INCLUIDOS

ip_utils.py - Funciones auxiliares para conversion de IPs

cidr_calculator.py - Calculadora CIDR completa

vlsm_calculator.py - Calculadora VLSM con algoritmo

main.py - Menu principal unificado

--------------------------------------------------------
INSTALACION RAPIDA

METODO (Directo):

Abrir terminal/cmd en la carpeta del proyecto

Ejecutar: python main.py


USO DEL PROGRAMA

Al ejecutar, aparecera un menu con 5 opciones:
--------------------------------------------------------

OPCION 1: CALCULADORA CIDR

Formato de entrada aceptado:

192.168.1.0/24

192.168.1.0 255.255.255.0

--------------------------------------------------------
OPCION 2: CALCULADORA VLSM

Pasos:

Ingresar red base (ej: 192.168.0.0/24)

Agregar subredes con nombre y numero de hosts

El programa calcula automaticamente

--------------------------------------------------------
OPCION 3: CASOS DE PRUEBA (sugeridos por el profesor)

Ejecuta automaticamente:

CIDR: 192.168.10.0/24

VLSM: 192.168.0.0/24 con A=100, B=50, C=25, D=10

Caso limite: Error por espacio insuficiente
--------------------------------------------------------

OPCION 4: ACERCA DEL PROYECTO

Muestra informacion del equipo y proyecto
--------------------------------------------------------

OPCION 5: SALIR

Termina el programa
--------------------------------------------------------

CASOS DE PRUEBA PARA VALIDACION

Caso 1 (CIDR):
Entrada: 10.0.0.0/8
Red: 10.0.0.0
Broadcast: 10.255.255.255
Hosts: 16,777,214

Caso 2 (VLSM):
Red base: 172.16.0.0/16
Subredes: Ventas=500, TI=250, RH=120, Marketing=60

Caso 3 (Limite):
Entrada: 192.168.1.0/30 con 10 hosts
Resultado: Error "Espacio insuficiente"

--------------------------------------------------------

FUNCIONALIDADES IMPLEMENTADAS

CALCULADORA CIDR:

Conversion CIDR <-> mascara decimal

Calculo de red, broadcast, rango hosts

Representación binaria

Validación de IPs

Manejo de /31 y /32
--------------------------------------------------------

CALCULADORA VLSM:

Algoritmo VLSM optimo

Ordenamiento descendente

Asignación sin solapamientos

Calculo de desperdicio

Validación de espacio

--------------------------------------------------------
ENTREGABLES COMPLETADOS

[✓] Documento PDF
[✓] Código fuente comentado
[✓] Ejecutable funcional
[✓] Video explicativo
[✓] README con instrucciones
[✓] Casos de prueba
[✓] Pruebas unitarias

ULTIMA ACTUALIZACION: 4 enero 2026