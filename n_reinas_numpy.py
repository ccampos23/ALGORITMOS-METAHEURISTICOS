import random
import math
import time
import numpy as np
import sys
import pandas as pd
from datetime import datetime


def generar_real_aleatorio():
    return random.random()


def generar_entero_aleatorio(n):
    return random.randint(1, n)


def inicializar_poblacion(tamaño_poblacion, n):
    # genarar la poblacion con numpy
    poblacion_array = np.random.randint(1, n + 1, size=(tamaño_poblacion, n), dtype=np.int8)
    poblacion = []
    for i in range(tamaño_poblacion):
        poblacion.append(poblacion_array[i])
    return poblacion


def mutar_individuo(individuo, prob_mutacion, n):
    if generar_real_aleatorio() < prob_mutacion:
        # seleccionar dos posiciones aleatorias para swapear
        posicion1 = random.randint(0, len(individuo) - 1)
        posicion2 = random.randint(0, len(individuo) - 1)
        
        # asegurar que las posiciones sean !=
        while posicion1 == posicion2:
            posicion2 = random.randint(0, len(individuo) - 1)
        
        # swap de los valores en las dos posiciones
        individuo[posicion1], individuo[posicion2] = individuo[posicion2], individuo[posicion1]
    
    return individuo


def reducir_poblacion(poblacion, tamaño_deseado):
    return poblacion[:tamaño_deseado]


def cruzar_individuos(padre1, padre2):
    punto_cruza = random.randint(1, len(padre1) - 1)
    hijo1 = np.concatenate([padre1[:punto_cruza], padre2[punto_cruza:]])
    hijo2 = np.concatenate([padre2[:punto_cruza], padre1[punto_cruza:]])
    return hijo1, hijo2


def fitness(tablero, n):
    acum = 0
    size = len(tablero)
    columna_i = 0
    # se cuentan las coliciones entre las reinas y se asignan al acumulador
    for i in tablero:
        for j in range(columna_i + 1, size):
            if i == tablero[j]:
                acum = acum + 1
            # resto las columnas y veo si quedan en la misma fila
            if int(tablero[j]) + (j - columna_i) == int(i) or int(tablero[j]) - (j - columna_i) == int(i):
                acum = acum + 1
        columna_i = columna_i + 1
    # n*(n-1)/2 es el maximo de colisiones que se pueden dar para un tablero de tamaño n asi que se le resta el acumulador para obtener el numero de no colisiones
    return (n * (n - 1) / 2) - acum


def seleccionar_padre(poblacion, colisiones):
    fitnes_total = sum(colisiones)
    
    # manejo de caso especial: todos tienen fitness 0
    if fitnes_total == 0:
        return random.choice(poblacion).copy()  # seleccion aleatoria uniforme
    
    ruleta = random.uniform(0, fitnes_total)
    acum = 0
    
    for i in range(len(poblacion)):
        acum += colisiones[i]
        if ruleta <= acum:
            return poblacion[i].copy()


def generar_nueva_poblacion(poblacion_actual, colisiones, tamaño_poblacion, prob_cruza, prob_mutacion, n):
    nueva_poblacion = []
    
    while len(nueva_poblacion) < tamaño_poblacion:
        # seleccionar dos padres usando ruleta
        padre1 = seleccionar_padre(poblacion_actual, colisiones)
        padre2 = seleccionar_padre(poblacion_actual, colisiones)
        
        # decidir si aplicar cruzamiento segun probabilidad
        if generar_real_aleatorio() < prob_cruza:
            hijo1, hijo2 = cruzar_individuos(padre1, padre2)
            
            # aplicar mutación a cada hijo
            hijo1 = mutar_individuo(hijo1, prob_mutacion, n)
            hijo2 = mutar_individuo(hijo2, prob_mutacion, n)
            
            # agregar hijos a la nueva poblacion
            nueva_poblacion.append(hijo1)
            if len(nueva_poblacion) < tamaño_poblacion:
                nueva_poblacion.append(hijo2)
    
    return nueva_poblacion


# inicializan variables y parámetros de entrada

# leer inputs
semilla = int(sys.argv[1])
n = int(sys.argv[2])
poblacion_inicial = int(sys.argv[3])
prob_cruza = float(sys.argv[4])
prob_mutacion = float(sys.argv[5])
generaciones = int(sys.argv[6])

# parametros utilizados
print(f"Parámetros utilizados:")
print(f"Semilla: {semilla}")
print(f"Tamaño del tablero (N): {n}")
print(f"Tamaño de la población: {poblacion_inicial}")
print(f"Probabilidad de cruza: {prob_cruza}")
print(f"Probabilidad de mutación: {prob_mutacion}")
print(f"Número de generaciones: {generaciones}")
print("-" * 50)

random.seed(semilla)
np.random.seed(semilla) 

solucion_encontrada = False
resultados = []  # lista para almacenar todos los resultados

# ejecutar hasta 10 intentos
for intento in range(10):
    tiempo_inicio = time.time()  # iniciar medicion de tiempo
    
    # genera una poblacion inicial aleatoria
    poblacion = inicializar_poblacion(poblacion_inicial, n)
    mejor_fitnes_global = 0

    # ciclo principal de tamaño de generaciones
    for a in range(generaciones):
        colisiones = []  # Reinicializar colisiones cada generacion
        
        # calcula y se guarda en colisiones el fitnes de la poblacion inicial
        for i in range(poblacion_inicial):
            colisiones.append(fitness(poblacion[i], n))

        # buscar la mejor solucion en esta generacion
        for i in range(poblacion_inicial):
            if colisiones[i] == (n * (n - 1) / 2):  # comprueba le fitnes
                tiempo_fin = time.time()
                tiempo_transcurrido = tiempo_fin - tiempo_inicio
                solucion = str(poblacion[i])
                
                # Guardar resultdao exitoso
                resultados.append({
                    'Intento': intento + 1,
                    'Generacion': a + 1,
                    'Solucion_Encontrada': 'SI',
                    'Solucion': solucion,
                    'Fitness': colisiones[i],
                    'Tiempo_segundos': round(tiempo_transcurrido, 4),
                    'Semilla': semilla,
                    'N': n,
                    'Poblacion': poblacion_inicial,
                    'Prob_Cruza': prob_cruza,
                    'Prob_Mutacion': prob_mutacion,
                    'Max_Generaciones': generaciones
                })
                
                print("SOLUCION ENCONTRADA = " + solucion)
                print(f"Fitness: {colisiones[i]}")
                print(f"Tiempo del intento {intento + 1}: {tiempo_transcurrido:.4f} segundos")
                solucion_encontrada = True
                break
            elif colisiones[i] > mejor_fitnes_global:
                mejor_fitnes_global = colisiones[i]

        if solucion_encontrada:
            break

        # generar nueva poblacion
        poblacion = generar_nueva_poblacion(poblacion, colisiones, poblacion_inicial, prob_cruza, prob_mutacion, n)

    if solucion_encontrada:
        break
    else:
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        
        # Guardar resultado sin éxito
        resultados.append({
            'Intento': intento + 1,
            'Generacion': generaciones,
            'Solucion_Encontrada': 'NO',
            'Solucion': 'N/A',
            'Fitness': mejor_fitnes_global,
            'Tiempo_segundos': round(tiempo_transcurrido, 4),
            'Semilla': semilla,
            'N': n,
            'Poblacion': poblacion_inicial,
            'Prob_Cruza': prob_cruza,
            'Prob_Mutacion': prob_mutacion,
            'Max_Generaciones': generaciones
        })
        
        print(f"intento {intento + 1} sin exito, mejor fitnes: {mejor_fitnes_global}, tiempo: {tiempo_transcurrido:.4f} segundos")

if not solucion_encontrada:
    print("no se ha encontrado solucion")

# Exportar resultados a Excel
try:
    df = pd.DataFrame(resultados)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resultados_n_reinas_numpy_{timestamp}.xlsx"
    df.to_excel(filename, index=False)
    print(f"\nResultados exportados a: {filename}")
except ImportError:
    print("\nPara exportar a Excel, instala pandas: pip install pandas openpyxl")
except Exception as e:
    print(f"\nError al exportar a Excel: {e}")
    # Guardar como CSV como alternativa
    try:
        import csv
        csv_filename = f"resultados_n_reinas_numpy_{timestamp}.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            if resultados:
                writer = csv.DictWriter(csvfile, fieldnames=resultados[0].keys())
                writer.writeheader()
                writer.writerows(resultados)
        print(f"Resultados guardados como CSV: {csv_filename}")
    except Exception as csv_error:
        print(f"Error al guardar CSV: {csv_error}")
