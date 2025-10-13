import numpy as np
import random

from scripts.EvaluarAudio import zero_crosing_rate_mean, spectral_flatness_mean, rms_energy_mean, ponderar_calidad
from utils.rangos_parametros_audio import parametros_audio


def generar_vecino(individuo: dict, desplazamiento: float):
    # Copia para no modificar el original
    vecino = individuo.copy()
    # Elegir parámetro aleatorio
    clave = random.choice(list(vecino.keys()))
    # Obtener límites
    inf = parametros_audio[clave]["inf"]
    sup = parametros_audio[clave]["sup"]
    # Calcular cambio proporcional a la temperatura
    rango = sup - inf
    cambio = random.uniform(-1, 1) * desplazamiento * rango / 100  # escala del %
    # Nuevo valor con límites
    nuevo_valor = vecino[clave] + cambio
    if isinstance(vecino[clave], int):
        nuevo_valor = int(round(nuevo_valor))
    nuevo_valor = max(min(nuevo_valor, sup), inf)
    # Asignar
    vecino[clave] = nuevo_valor
    return vecino










if __name__ == "__main__":
    elementos = {
        "low_cut": 125,
        "high_cut": 8524
     }

    print(elementos)
    for i in range(10):
        print(generar_vecino(elementos, 85))
