from datetime import datetime
from random import random

from networkx import reverse

from scripts.Audio import Audio
from scripts.EvaluarAudio import calcular_fitness
from scripts.LimpiezaAudio import aplicar_filtros
from utils.FormatoFechaHora import FormatoFechaHora
from utils.Graficar import graficar_historial, graficar_metricas
from utils.guardar_contenido_json import guardar_contenido_json
from utils.poblacion import generar_poblacion
from utils.rangos_parametros_audio import parametros_audio


def grey_wold_optimizer():
    print("Grey Wolf Optimizer")

    audio_original = Audio(".\\..\\audio\\audio_test.wav")
    audio_original.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    print(f"Soundrate: {audio_original.sound_rate}")
    audio_original.normalizar_audio()

    generaciones_total = 3
    generaciones_local = 30
    n_wolves = 30

    for i in range(generaciones_total):
        historial = []
        mejor_evaluacion = {"puntuacion": 0}
        mejor_estado = {}

        wolves = generar_poblacion(n_wolves)
        fitness = []

        # Limpiar y evaluar poblacion inicial
        for individuo in range(len(wolves)):
            audio_filtrado = aplicar_filtros(audio_original, low_cut=wolves[individuo]["low_cut"],
                                             high_cut=wolves[individuo]["high_cut"],
                                             orden=wolves[individuo]["filtro_order"],
                                             prop_decrease=wolves[individuo]["prop_decrease"])
            fitness.append(calcular_fitness(audio_filtrado, audio_original.sound_rate))


        # Ordenar individuos ascendentemente  emparejados[0]: individuo, emparejados[1]: fitness
        emparejados = list(zip(wolves, fitness))
        emparejados.sort(key=lambda x: x[1]["puntuacion"], reverse=True)

        mejor_evaluacion = emparejados[0][1]
        mejor_estado = emparejados[0][0]
        # print(f"emparejados: {emparejados[0]}")

        """
        for emparejado in emparejados:
            print(f"Emparejado: {emparejado}")
            
        for fit in fitness:
            print(f"fitness: {fit}")
        """
        alpha, fit_alpha = emparejados[0]
        beta, fit_beta = emparejados[1]
        delta, fit_delta = emparejados[2]

        # Bucle principal de generaciones
        for generacion in range(generaciones_local):

            # Calcular parámetro 'a' que decrece linealmente
            a = 2 * (1 - generacion / generaciones_local)

            for i in range(n_wolves):
                lobo = wolves[i]

                # Evitar mover a los líderes directamente
                if lobo in [alpha, beta, delta]:
                    continue

                # Actualización de posición respecto a α, β y δ
                for clave in lobo.keys():
                    inf = parametros_audio[clave]["inf"]
                    sup = parametros_audio[clave]["sup"]

                    # Distancia y movimiento respecto a alpha
                    A1 = 2 * a * random() - a
                    C1 = 2 * random()
                    D_alpha = abs(C1 * alpha[clave] - lobo[clave])
                    X1 = alpha[clave] - A1 * D_alpha

                    # Beta
                    A2 = 2 * a * random() - a
                    C2 = 2 * random()
                    D_beta = abs(C2 * beta[clave] - lobo[clave])
                    X2 = beta[clave] - A2 * D_beta

                    # Delta
                    A3 = 2 * a * random() - a
                    C3 = 2 * random()
                    D_delta = abs(C3 * delta[clave] - lobo[clave])
                    X3 = delta[clave] - A3 * D_delta

                    # Nueva posición: promedio
                    nuevo_valor = (X1 + X2 + X3) / 3
                    # Ajustar a los límites
                    if clave == "prop_decrease":
                        lobo[clave] = max(min(nuevo_valor, sup), inf)
                    else:
                        lobo[clave] = round(max(min(nuevo_valor, sup), inf))

                # print(f"lobo: {lobo}")

            # Evaluar nueva población
            fitness = []
            for individuo in wolves:
                audio_filtrado = aplicar_filtros(audio_original,
                                                 low_cut=individuo["low_cut"],
                                                 high_cut=individuo["high_cut"],
                                                 orden=individuo["filtro_order"],
                                                 prop_decrease=individuo["prop_decrease"])
                fitness.append(calcular_fitness(audio_filtrado, audio_original.sound_rate))

            emparejados = list(zip(wolves, fitness))
            emparejados.sort(key=lambda x: x[1]["puntuacion"], reverse=True)
            alpha, fit_alpha = emparejados[0]
            beta, fit_beta = emparejados[1]
            delta, fit_delta = emparejados[2]

            # print(f"Wolves: {len(wolves)}")

            if emparejados[0][1]["puntuacion"] > mejor_evaluacion["puntuacion"]:
                mejor_evaluacion = emparejados[0][1]
                mejor_estado = emparejados[0][0]

            historial.append({
                "iter": generacion,
                "estado": alpha,
                "zcr": fit_alpha["zcr"],
                "flatness": fit_alpha["flatness"],
                "rms": fit_alpha["rms"],
                "ponderacion": fit_alpha["puntuacion"]
            })


            print(f"\nIter {generacion} | Mejor puntuación: {fit_alpha['puntuacion']:.4f}")
            print(f"Parametros: {alpha}")

        nombre = f".\\..\\output\\json\\wolf_{audio_original.nombre_archivo.split(".")[0]}_{FormatoFechaHora.formatear_fecha_hora(datetime.now(), formato=FormatoFechaHora.Ymd_HMS)}.json"
        guardar_contenido_json(nombre, historial)
        graficar_historial(historial=historial)
        graficar_metricas(historial=historial)





if __name__ == "__main__":
    grey_wold_optimizer()