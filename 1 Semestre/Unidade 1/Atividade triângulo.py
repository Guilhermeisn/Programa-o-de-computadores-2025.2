# Importando bibliotecas
import sys
import math
import os

# Obtendo input dos lados
try:
    ladoA = float(input('Digite o valor do lado A do triângulo: '))
    print(f'O lado A do triângulo é: {ladoA}')
    ladoB = float(input('Digite o valor do lado B do triângulo: '))
    print(f'O lado B do triângulo é: {ladoB}')
    ladoC = float(input('Digite o valor do lado C do triângulo: '))
    print(f'O lado C do triângulo é: {ladoC}')
except ValueError:
    sys.exit('ERRO: Insira um valor válido.')

# Verificando se é possível formar um triângulo
if not (ladoA + ladoB > ladoC and ladoA + ladoC > ladoB and ladoB + ladoC > ladoA):
    sys.exit('Não é possível formar um triângulo com os lados fornecidos.')

# Classificação quanto aos lados
if ladoA == ladoB == ladoC:
    tipo_lado = 'equilátero'
elif ladoA == ladoB or ladoA == ladoC or ladoB == ladoC:
    tipo_lado = 'isósceles'
else:
    tipo_lado = 'escaleno'

# Cálculo dos ângulos (usando a Lei dos Cossenos)
A = math.degrees(math.acos((ladoB**2 + ladoC**2 - ladoA**2) / (2 * ladoB * ladoC)))
B = math.degrees(math.acos((ladoA**2 + ladoC**2 - ladoB**2) / (2 * ladoA * ladoC)))
C = 180 - (A + B)

# Classificação quanto aos ângulos
if round(A, 2) == 90 or round(B, 2) == 90 or round(C, 2) == 90:
    tipo_angulo = 'retângulo'
elif A > 90 or B > 90 or C > 90:
    tipo_angulo = 'obtusângulo'
else:
    tipo_angulo = 'acutângulo'

# Exibindo resultados
print(f'Os lados fornecidos formam um triângulo {tipo_lado} e {tipo_angulo}.')
print(f'Ângulos aproximados: A = {A:.2f}°, B = {B:.2f}°, C = {C:.2f}°')
