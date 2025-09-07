import random
import math
import time


def generar_real_aleatorio():
    return random.random()


def generar_entero_aleatorio(n):
    return random.randint(1, n)


def inicializar_poblacion(tamaño_poblacion, n):
    poblacion = []
    for i in range(tamaño_poblacion):
        aux = " "
        # genero tableros con reinas en filas aleatorias
        for j in range(n):
            aux = str(aux) + str(generar_entero_aleatorio(n)) + " "
        poblacion.append(list(aux.split()))
    return poblacion


def mutar_individuo(individuo, prob_mutacion, n):
    if generar_real_aleatorio() < prob_mutacion:
        # Seleccionar una posición aleatoria para mutar
        posicion = random.randint(0, len(individuo) - 1)
        individuo[posicion] = str(generar_entero_aleatorio(n))
    return individuo


def reducir_poblacion(poblacion, tamaño_deseado):
    return poblacion[:tamaño_deseado]


def cruzar_individuos(padre1, padre2):
    """Cruzar dos individuos con un punto de cruza"""
    punto_cruza = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_cruza] + padre2[punto_cruza:]
    hijo2 = padre2[:punto_cruza] + padre1[punto_cruza:]
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
            if int(tablero[j]) + (j - columna_i) == int(i) or int(tablero[j]) - (
                j - columna_i
            ) == int(i):
                acum = acum + 1
        columna_i = columna_i + 1
    # n*(n-1)/2 es el maximo de colisiones que se pueden dar para un tablero de tamaño n asi que se le resta el acumulador para obtener el numero de no colisiones
    return (n * (n - 1) / 2) - acum


def select(poblacion, colisiones, num_select, mejores):
    # se seleccionan los que tengan menos colisiones
    fitnes_total = sum(colisiones)

    if fitnes_total == 0:
        for _ in range(num_select):
            mejores.append(random.choice(poblacion)[:])  # seleccion aleatoria entre la poblacion
        return mejores

    for _ in range(num_select):
        ruleta = random.uniform(0, fitnes_total) #selecciona un numero aleatorio

        acum = 0
        for i in range(len(poblacion)):
            acum += colisiones[i] # acumula el fitnes hasta que supere el numeor aleatoria generado y lo agrega
            if ruleta <= acum:
                mejores.append(poblacion[i][:])
                break
    return mejores


def cruzamiento(mejores, poblacion_inicial, prob_cruza, prob_mutacion, n):
    hijos = []
    
    while len(hijos) < poblacion_inicial:
        # Seleccionar dos padres aleatoriamente
        padre1 = random.choice(mejores)
        padre2 = random.choice(mejores)
        
        # Decidir si aplicar cruzamiento según probabilidad
        if generar_real_aleatorio() < prob_cruza:
            hijo1, hijo2 = cruzar_individuos(padre1, padre2)
        else:
            # Si no hay cruzamiento, los hijos son copias de los padres
            hijo1, hijo2 = padre1[:], padre2[:]
        
        # Aplicar mutación a cada hijo
        hijo1 = mutar_individuo(hijo1, prob_mutacion, n)
        hijo2 = mutar_individuo(hijo2, prob_mutacion, n)
        
        # Agregar hijos a la población
        hijos.append(hijo1)
        if len(hijos) < poblacion_inicial:
            hijos.append(hijo2)
    
    # Reducir población al tamaño deseado
    return reducir_poblacion(hijos, poblacion_inicial)


def printTablero(tablero):  # Display de tablero
    size = len(tablero)
    for i in range(size):
        aux = ""
        for j in tablero:
            if int(j) == i + 1:
                aux = aux + " # "
            else:
                aux = aux + " '' "
        print(aux)


# inicializan variables y parámetros de entrada

print("Valor de la semilla:")
semilla = int(input())
random.seed(semilla)

print("Tamaño del tablero (N):")
n = int(input())

print("Tamaño de la poblacion:")
poblacion_inicial = int(input())

print("Probabilidad de cruza (0.0 - 1.0):")
prob_cruza = float(input())

print("Probabilidad de mutacion (0.0 - 1.0):")
prob_mutacion = float(input())

print("Numero de iteraciones:")
generaciones = int(input())

solucion_encontrada = False

# Ejecutar hasta 10 intentos
for intento in range(10):
    tiempo_inicio = time.time()  # Iniciar medición de tiempo
    
    # Genera una poblacion inicial aleatoria
    poblacion = inicializar_poblacion(poblacion_inicial, n)
    mejor_fitnes_global = 0

    # Genera una poblacion inicial aleatoria
    poblacion = inicializar_poblacion(poblacion_inicial, n)

    # ciclo principal de tamaño de generaciones
    for a in range(generaciones):
        colisiones = []  # Reinicializar colisiones cada generación
        
        # calcula y se guarda en colisiones el fitnes de la poblacion inicial
        for i in range(poblacion_inicial):
            colisiones.append(fitness(poblacion[i], n))

        # Buscar la mejor solución en esta generación
        for i in range(poblacion_inicial):
            if colisiones[i] == (n * (n - 1) / 2):  # comprueba le fitnes
                tiempo_fin = time.time()
                tiempo_transcurrido = tiempo_fin - tiempo_inicio
                print("SOLUCION ENCONTRADA = " + str(poblacion[i]) + "\n")
                print("Tablero:")
                printTablero(poblacion[i])
                print(f"Fitness: {colisiones[i]}")
                print(f"Tiempo del intento {intento + 1}: {tiempo_transcurrido:.4f} segundos")
                solucion_encontrada = True
                break
            elif colisiones[i] > mejor_fitnes_global:
                mejor_fitnes_global = colisiones[i]

        if solucion_encontrada:
            break

        mejores = select(poblacion, colisiones, int(poblacion_inicial * 0.25), [])  # selecciona el 25% de los mejores de la poblacion
        poblacion = cruzamiento(mejores, poblacion_inicial, prob_cruza, prob_mutacion, n)  # cruza los mejores

    if solucion_encontrada:
        break
    else:
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        print(f"intento {intento + 1} sin exito, mejor fitnes: {mejor_fitnes_global}, tiempo: {tiempo_transcurrido:.4f} segundos")

if not solucion_encontrada:
    print("no se ha encontrado solucion")
