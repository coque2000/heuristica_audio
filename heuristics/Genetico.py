from datetime import datetime

import numpy as np

from utils.poblacion import generar_individuo, generar_poblacion, seleccionar_mejores, generar_nueva_poblacion, \
    mutar_individuo
from utils.rangos_parametros_audio import parametros_audio
from scripts.Audio import Audio
from scripts.EvaluarAudio import zero_crosing_rate_mean, spectral_flatness_mean, rms_energy_mean, ponderar_calidad
from scripts.LimpiezaAudio import aplicar_filtro_pasabanda, reducir_ruido, aplicar_filtros
from utils.FormatoFechaHora import FormatoFechaHora
from utils.Graficar import graficar_historial, graficar_metricas
from utils.guardar_contenido_json import guardar_contenido_json




def genetico_limpieza_audio():
    print("Genetico")

    audio_original = Audio(".\\..\\audio\\audio_test.wav")
    audio_original.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    print(f"Soundrate: {audio_original.sound_rate}")
    audio_original.normalizar_audio()

    generaciones_total = 10
    generaciones_local = 10

    # Estado inicial
    tamanio_poblacion = 100
    poblacion = generar_poblacion(tamanio_poblacion)
    cromosaomas = len(poblacion[0])
    porc_mutacion = (1 / cromosaomas)
    elitismo = 1

    nueva_poblacion = poblacion
    historial = []
    mejor_evaluacion = {"puntuacion": 0}

    for generacion in range(generaciones_local):
        print(f"\nGeneracion: {generacion}")
        audios = []
        fitness = []
        evaluacion = {}

        # Limpiar y evaluar poblacion inicial
        for individuo in nueva_poblacion:
            audio_filtrado = aplicar_filtros(audio_original, low_cut=individuo["low_cut"], high_cut=individuo["high_cut"], orden=individuo["filtro_order"], prop_decrease=individuo["prop_decrease"])
            audios.append(audio_filtrado)
            evaluacion: dict = {"zcr": zero_crosing_rate_mean(audio_filtrado, audio_original.sound_rate),
                                "flatness": spectral_flatness_mean(audio_filtrado, audio_original.sound_rate),
                                "rms": rms_energy_mean(audio_filtrado, audio_original.sound_rate)}
            evaluacion["puntuacion"] = ponderar_calidad(zcr=evaluacion["zcr"], spectral_flatness=evaluacion["flatness"], rms_energy=evaluacion["rms"])
            if mejor_evaluacion["puntuacion"] < evaluacion["puntuacion"]:
                mejor_evaluacion["puntuacion"] = evaluacion["puntuacion"]

            fitness.append(evaluacion["puntuacion"])

        mejores = seleccionar_mejores(nueva_poblacion, fitness, num_mejores= int(tamanio_poblacion * .10), torneo_size=3)

        # print(nueva_poblacion)
        indice_mejor = fitness.index(max(fitness))
        print(f"Mejor individuo: Fitness: {fitness[indice_mejor]}")
        print(f"Parametros: {nueva_poblacion[indice_mejor]}")
        historial.append({
            "iter": generacion,
            "estado": nueva_poblacion[indice_mejor],
            "zcr": evaluacion["zcr"],
            "flatness": evaluacion["flatness"],
            "rms": evaluacion["rms"],
            "ponderacion": evaluacion["puntuacion"]
        })

        # Generar nueva poblacion
        nueva_poblacion = generar_nueva_poblacion(mejores, fitness, tamanio_poblacion, pase_directo=elitismo)
        print(f"len(poblacion): {len(nueva_poblacion)}")

        for i_indvividuo in range(len(nueva_poblacion)):
            nueva_poblacion[i_indvividuo] = mutar_individuo(nueva_poblacion[i_indvividuo], prob_mutacion=porc_mutacion)

    print(f"Mejor individuo: {mejor_evaluacion}")

    graficar_historial(historial=historial)
    graficar_metricas(historial=historial)







        


    """
    
    max_iteraciones = 1000
    max_iteraciones_general = 30
    iteraciones_sin_mejora = 0
    max_iteraciones_sin_mejora = 20
    historial = []

    for n_gen in range(max_iteraciones_general):

        for i in range(max_iteraciones):
            print(f"Iteracion: {i}")




            fitness = []
            for









            nuevo_estado = {
                "low_cut": max(20, min(estado["low_cut"] + np.random.randint(-20, 20), 1000)),
                "high_cut": max(estado["low_cut"] + 1000, min(estado["high_cut"] + np.random.randint(-200, 200), 16000)),
                "filtro_order": min(max(1, estado["filtro_order"] + np.random.choice([-1, 0, 1])), 8),
                "prop_de_noise": round(min(max(0.05, estado["prop_de_noise"] + np.random.uniform(-0.02, 0.02)), 0.5), 3)
            }

            audio_filtrado = aplicar_filtro_pasabanda(audio=audio_original, low_cut=nuevo_estado["low_cut"], high_cut=nuevo_estado["high_cut"], orden=nuevo_estado["filtro_order"])
            audio_limpio = reducir_ruido(audio=audio_filtrado, sound_rate=audio_original.sound_rate, prop_decrease=nuevo_estado["prop_de_noise"])

            if not np.all(np.isfinite(audio_limpio)):
                print("⚠️ El audio contiene valores no finitos. Se limpiará.")
                audio_limpio = np.nan_to_num(audio_limpio, nan=0.0, posinf=1.0, neginf=-1.0)

            # Evaluar
            evaluacion: dict = {"zcr": zero_crosing_rate_mean(audio_limpio, audio_original.sound_rate),
                                "flatness": spectral_flatness_mean(audio_limpio, audio_original.sound_rate),
                                "rms": rms_energy_mean(audio_limpio, audio_original.sound_rate)}
            evaluacion["puntuacion"] = ponderar_calidad(zcr=evaluacion["zcr"], spectral_flatness=evaluacion["flatness"], rms_energy=evaluacion["rms"])

            historial.append({
                "iter": i,
                "estado": nuevo_estado,
                "zcr": evaluacion["zcr"],
                "flatness": evaluacion["flatness"],
                "rms": evaluacion["rms"],
                "ponderacion": evaluacion["puntuacion"]
            })

            print(f"Ponderacion: {evaluacion["puntuacion"]}")

            if evaluacion["puntuacion"] > mejor_puntuaje:
                mejor_puntuaje = evaluacion["puntuacion"]
                mejor_audio = audio_limpio
                mejor_estado = nuevo_estado.copy()
                estado = nuevo_estado.copy()  # movernos a la nueva solución
                iteraciones_sin_mejora = 0
            else:
                iteraciones_sin_mejora += 1

            if iteraciones_sin_mejora >= max_iteraciones_sin_mejora:
                print(f"Iteraciones sin mejora superadas: {i}")
                break

    print("Mejor configuración encontrada:", mejor_estado)
    # graficar_historial(historial=historial)
    # graficar_metricas(historial=historial)
    nombre = f".\\..\\output\\{audio_original.nombre_archivo.split(".")[0]}_{FormatoFechaHora.formatear_fecha_hora(datetime.now(), formato=FormatoFechaHora.Ymd_HMS)}.json"
    guardar_contenido_json(nombre, historial)
    return mejor_audio, mejor_puntuaje, mejor_estado, historial
    """

if __name__ == '__main__':
    print("heuristica")
    genetico_limpieza_audio()