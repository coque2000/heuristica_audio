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

    generaciones_total = 1
    generaciones_local = 50
    gen_sin_mejora_lim = 10
    gen_sin_mejora_count = 0

    # Estado inicial
    tamanio_poblacion = 120
    tamanio_torneo = 3
    elitismo = 2

    for gen_global in range(generaciones_total):
        poblacion = generar_poblacion(tamanio_poblacion)
        cromosaomas = len(poblacion[0])
        porc_mutacion = (1 / cromosaomas) * 2
        nueva_poblacion = poblacion
        historial = []
        mejor_evaluacion = {"puntuacion": 0}
        mejor_estado = {}
        se_mejoro_gen = False

        for generacion in range(generaciones_local):
            print(f"\nGeneracion: {generacion}")
            audios = []
            fitness = []
            evaluacion = {}
            se_mejoro_gen = False


            # Limpiar y evaluar poblacion inicial
            for individuo in range(len(nueva_poblacion)):
                audio_filtrado = aplicar_filtros(audio_original, low_cut=nueva_poblacion[individuo]["low_cut"], high_cut=nueva_poblacion[individuo]["high_cut"], orden=nueva_poblacion[individuo]["filtro_order"], prop_decrease=nueva_poblacion[individuo]["prop_decrease"])
                audios.append(audio_filtrado)
                evaluacion: dict = {"zcr": zero_crosing_rate_mean(audio_filtrado, audio_original.sound_rate),
                                    "flatness": spectral_flatness_mean(audio_filtrado, audio_original.sound_rate),
                                    "rms": rms_energy_mean(audio_filtrado, audio_original.sound_rate)}
                evaluacion["puntuacion"] = ponderar_calidad(zcr=evaluacion["zcr"], spectral_flatness=evaluacion["flatness"], rms_energy=evaluacion["rms"])

                if mejor_evaluacion["puntuacion"] < evaluacion["puntuacion"]:
                    mejor_evaluacion = evaluacion
                    mejor_estado = nueva_poblacion[individuo]
                    se_mejoro_gen = True

                # Generaciones sin mejora
                fitness.append(evaluacion["puntuacion"])

            mejores = seleccionar_mejores(nueva_poblacion, fitness, num_mejores= int(tamanio_poblacion * .10), torneo_size=tamanio_torneo)

            # print(nueva_poblacion)
            print(f"Mejor individuo: Fitness: {mejor_evaluacion["puntuacion"]}")
            print(f"Parametros: {mejor_estado}")
            historial.append({
                "iter": generacion,
                "estado": mejor_estado,
                "zcr": mejor_evaluacion["zcr"],
                "flatness": mejor_evaluacion["flatness"],
                "rms": mejor_evaluacion["rms"],
                "ponderacion": mejor_evaluacion["puntuacion"]
            })

            if se_mejoro_gen:
                gen_sin_mejora_count = 0
            else:
                gen_sin_mejora_count += 1

            print(f"gen_sin_mejora_count: {gen_sin_mejora_count}")
            if gen_sin_mejora_count >= gen_sin_mejora_lim:
                porc_mutacion = min(porc_mutacion + 0.2, 1.0)
                gen_sin_mejora_count = 0

                emparejados = list(zip(nueva_poblacion, fitness))
                emparejados.sort(key=lambda x: x[1], reverse=True)
                mejor_actual = emparejados[0][0]
                nueva_poblacion = [mejor_actual] + nueva_poblacion[:len(nueva_poblacion) // 3]
                if len(nueva_poblacion) < tamanio_poblacion:
                    nueva_poblacion.extend(generar_poblacion(tamanio_poblacion - len(nueva_poblacion)))
                print(f"Se ha generado nueva poblacion. Mutacion: {porc_mutacion}")

            # Generar nueva poblacion
            nueva_poblacion = generar_nueva_poblacion(mejores, fitness, tamanio_poblacion, pase_directo=elitismo)
            # print(f"len(poblacion): {len(nueva_poblacion)}")

            for i_indvividuo in range(len(nueva_poblacion)):
                nueva_poblacion[i_indvividuo] = mutar_individuo(nueva_poblacion[i_indvividuo], prob_mutacion=porc_mutacion)


        print(f"Mejor individuo global: {mejor_evaluacion}")


        nombre = f".\\..\\output\\json\\genetico_{audio_original.nombre_archivo.split(".")[0]}_{FormatoFechaHora.formatear_fecha_hora(datetime.now(), formato=FormatoFechaHora.Ymd_HMS)}.json"
        guardar_contenido_json(nombre, historial)
        graficar_historial(historial=historial)
        graficar_metricas(historial=historial)


if __name__ == '__main__':
    print("heuristica")
    genetico_limpieza_audio()