import numpy as np
import random

from utils.rangos_parametros_audio import parametros_audio

def generar_individuo():
    return {
        "low_cut": np.random.randint(parametros_audio["low_cut"]["inf"], parametros_audio["low_cut"]["sup"]),
        "high_cut": np.random.randint(parametros_audio["high_cut"]["inf"], parametros_audio["high_cut"]["sup"]),
        "filtro_order": np.random.randint(parametros_audio["filtro_order"]["inf"], parametros_audio["filtro_order"]["sup"]),
        "prop_decrease": np.random.uniform(parametros_audio["prop_decrease"]["inf"], parametros_audio["prop_decrease"]["sup"])
    }

def generar_poblacion(n_individuos: int):
    poblacion = []
    for i in range(n_individuos):
        poblacion.append(generar_individuo())
    return poblacion

def seleccionar_mejores(poblacion: list, puntuaciones: list, num_mejores: int = 2, torneo_size: int = 2):
    """
    Selecciona los mejores individuos de una población usando elitismo + torneo.

    Args:
        poblacion (list[dict]): Lista de diccionarios con los parámetros de cada individuo.
        puntuaciones (list[float]): Lista con las puntuaciones correspondientes a cada individuo.
        num_mejores (int): Número de individuos que pasan directo por elitismo.
        torneo_size (int): Tamaño del torneo para el resto.

    Returns:
        list[dict]: Lista con los individuos seleccionados.
    """
    # Emparejar cada individuo con su puntuación
    emparejados = list(zip(poblacion, puntuaciones))

    # Ordenar por mejor puntuación (mayor es mejor)
    emparejados.sort(key=lambda x: x[1], reverse=True)

    # Elitismo → los mejores pasan directamente
    seleccionados = [ind for ind, _ in emparejados[:num_mejores]]

    # Torneo para el resto
    while len(seleccionados) <= len(poblacion):
        torneo = random.sample(emparejados, torneo_size)
        # print(torneo)
        ganador = max(torneo, key=lambda x: x[1])[0]
        seleccionados.append(ganador)

    return seleccionados


def cruzar_padres(parent1, parent2, crossover_rate=0.85):
    """
    Realiza cruce de un punto entre dos padres para generar dos hijos.

    parent1, parent2: listas o arrays con los genes (parámetros)
    crossover_rate: probabilidad de realizar cruce (si no, copia directa)
    """
    # Copia directa si no hay cruce
    if random.random() > crossover_rate:
        # return parent1[:], parent2[:]
        return parent1, parent2

    # Elegir punto de cruce (no en el extremo)
    point = random.randint(1, len(parent1) - 1)

    # Generar hijos
    # print(f"parent1: {parent1}")
    # print(f"parent2: {parent2}")
    # print(f"point: {point}")
    child1 = []
    child2 = []

    if type(parent1) == dict:
        child1 = {}
        child2 = {}
        keys = list(parent1.keys())
        # Para las claves antes del punto, hijo1 toma de padre1, hijo2 de padre2
        for k in keys[:point]:
            child1[k] = parent1[k]
            child2[k] = parent2[k]

        # Para las claves después del punto, se cruzan
        for k in keys[point:]:
            child1[k] = parent2[k]
            child2[k] = parent1[k]

    else:
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]


    return child1, child2


def generar_nueva_poblacion(seleccionados, fitness, num_hijos, pase_directo = 1):
    nueva_poblacion = []

    emparejados = list(zip(seleccionados, fitness))
    # Ordenar por mejor puntuación (mayor es mejor)
    emparejados.sort(key=lambda x: x[1], reverse=True)

    nueva_poblacion = [emparejados[:pase_directo][0][0]]
    # print(nueva_poblacion)

    while len(nueva_poblacion) < num_hijos:
        # Selecciona padres aleatoriamente de la lista de seleccionados
        padre1 = None
        padre2 = None
        while padre1 == padre2:
            padre1, padre2 = random.sample(seleccionados, 2)

        # Cruza para obtener hijos
        hijo1, hijo2 = cruzar_padres(padre1, padre2)

        nueva_poblacion.extend([hijo1, hijo2])

    # Cortar si se generan más hijos de los necesarios
    return nueva_poblacion[:num_hijos]

def mutar_individuo(individuo, prob_mutacion=0.1, rango_mutacion=(-1, 1)):
    """
    Aplica mutación a un individuo.

    Args:
        individuo (list[float]): Lista con los parámetros (genes) del individuo.
        prob_mutacion (float): Probabilidad de que cada gen mute (0 a 1).
        rango_mutacion (tuple): Rango del cambio aleatorio (mín, máx).

    Returns:
        list[float]: El individuo mutado.
    """
    individuo_mutado = individuo.copy()

    if type(individuo) == dict:
        for clave in individuo_mutado:
            if random.random() < prob_mutacion:  # condición normal de mutación
                if clave == "prop_decrease":
                    cambio = random.uniform(-0.05, 0.05)
                    nuevo_valor = individuo_mutado[clave] + cambio
                else:
                    cambio = random.uniform(rango_mutacion[0], rango_mutacion[1])
                    if isinstance(individuo_mutado[clave], int):
                        nuevo_valor = individuo_mutado[clave] + round(cambio)
                    else:
                        nuevo_valor = individuo_mutado[clave] + cambio

                # Limitar valor según rango definido
                inf = parametros_audio[clave]["inf"]
                sup = parametros_audio[clave]["sup"]
                nuevo_valor = max(min(nuevo_valor, sup), inf)

                # Actualizar valor mutado
                individuo_mutado[clave] = nuevo_valor
                print(f"ind[{clave}]: {individuo_mutado[clave]}")
    else:
        for i in range(len(individuo_mutado)):
            if random.random() < prob_mutacion:
                cambio = random.uniform(rango_mutacion[0], rango_mutacion[1])
                if type(individuo_mutado[i]) == int:
                    individuo_mutado[i] += round(cambio)  # Se altera el valor
                else:
                    individuo_mutado[i] += cambio  # Se altera el valor
                    individuo_mutado[i] = max(min(individuo_mutado[i], parametros_audio["prop_decrease"]["inf"]), parametros_audio["prop_decrease"]["sup"])
                # Si quieres, aquí puedes limitar los valores a un rango fijo
                # individuo_mutado[i] = max(min(individuo_mutado[i], limite_max), limite_min)

    return individuo_mutado


if __name__ == "__main__":
    print(generar_individuo())
    print("\n")
    print(generar_poblacion(3))

    poblacion_arbitraria = [10, 9, 2, 4, 1, 5, 6, 7]
    puntuaciones = [2.484, 8.144, 6.165, 7.415, 2.215, 8.45, 9.1231]
    print(seleccionar_mejores(poblacion_arbitraria, puntuaciones))

    p1 = [0.1, 0.2, 0.3, 0.4]
    p2 = [0.5, 0.6, 0.7, 0.8]

    h1, h2 = cruzar_padres(p1, p2)
    print("Padre 1:", p1)
    print("Padre 2:", p2)
    print("Hijo 1 :", h1)
    print("Hijo 2 :", h2)

    # print(generar_nueva_poblacion([p1, p2], 2))

    print(mutar_individuo(p1, prob_mutacion=.25))
