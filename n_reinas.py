import random
import math


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
    # n*(n-1)/3 es el maximo de colisiones que se pueden dar para un tablero de tamaño n asi que se le resta el acumulador para obtener el numero de no colisiones
    return (n * (n - 1) / 2) - acum


def select(poblacion, colisiones, num_select, mejores):
    # se le seleccionan los que tengan menos colisiones
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


def cruzamiento(mejores, poblacion_inicial):
    # crea listas para guardar heads(las primeros n/2 posiciones de la reina en el tablero) y tails(lo que resta de las posiciones) e hijos para guardar el cruzamiento
    heads = []
    tails = []
    hijos = []
    # ciclo que separa los tableros en dos para asignarlas a heads
    for i in range(len(mejores)):
        lista = mejores[i]
        aux = math.ceil(len(lista) / 2)
        aux2 = [
            lista[i : i + aux] for i in range(0, len(lista), aux)
        ]  # [[2,3,1,4],[5,6,7,8]]
        # factor de mutacion de un 50% (1: mutar, 2:pasar), si muta se asignan valores aleatorios a las posiciones
        for j in range(len(aux2)):
            if random.randint(1, 10) == 1:
                parte_actual = aux2[j]
                if len(parte_actual) > 0:  # Verificar que la parte no esté vacía
                    # Índices corregidos (0-based)
                    columna = random.randint(0, len(parte_actual) - 1)
                    fila = random.randint(1, n)
                    aux2[j][columna] = str(fila)
        # se introducen las listas separadas a sus respectiva lista
        heads.append(aux2[0])
        tails.append(aux2[1])
    # Se combinan en todas las posibilidades para dar 200 poblaciones nuevas distintas a las anteriores
    while len(hijos) < poblacion_inicial:
        i = random.randint(0, len(heads) - 1)
        j = random.randint(0, len(tails) - 1)
        if i != j:
            hijos.append(heads[i] + tails[j])
    return hijos[:poblacion_inicial]


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


# inicializan variables
print("Ingrese n:")
n = int(input())

solucion_encontrada = False

# Ejecutar hasta 10 intentos
for intento in range(10):
    poblacion = []
    mejores = []
    poblacion_inicial = 100
    generaciones = 500
    colisiones = []
    solucion = 0

    # Genera una poblacion inicial aleatoria
    for i in range(poblacion_inicial):
        aux = " "
        # genero tableros con reinas en filas aleatorias
        for j in range(n):
            aux = str(aux) + str(random.randint(1, n)) + " "
        poblacion.append(list(aux.split()))

    # ciclo principal de tamaño de generaciones
    for a in range(generaciones):
        # calcula y se guarda en colisiones el fitnes de la poblacion inicial
        for i in range(poblacion_inicial):
            colisiones.append(fitness(poblacion[i], n))

        # Buscar la mejor solución en esta generación
        mejor_fitnes = 0
        for i in range(poblacion_inicial):
            if colisiones[i] == (n * (n - 1) / 2):  # comprueba le fitnes
                solucion = poblacion[i]
                print("SOLUCION ENCONTRADA = " + str(solucion) + "\n")
                print("Tablero:")
                printTablero(solucion)
                print(f"Fitness: {colisiones[i]}")
                solucion_encontrada = True
                break
            elif colisiones[i] > mejor_fitnes:
                mejor_fitnes = colisiones[i]

        if solucion_encontrada:
            break

        mejores = select(
            poblacion, colisiones, 50, mejores
        )  # selecciona los mejores de la poblacion
        poblacion = cruzamiento(mejores, poblacion_inicial)  # cruza los mejores
        colisiones.clear()
        mejores.clear()

    if solucion_encontrada:
        break
    else:
        print(f"intento {intento + 1} sin exito, mejor fitnes: {mejor_fitnes}")

if not solucion_encontrada:
    print("no se ha encontrado solucion")
