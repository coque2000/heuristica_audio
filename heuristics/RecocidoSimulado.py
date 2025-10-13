import math
import random
from datetime import datetime

from scripts.Audio import Audio
from scripts.EvaluarAudio import zero_crosing_rate_mean, spectral_flatness_mean, rms_energy_mean, ponderar_calidad
from scripts.LimpiezaAudio import aplicar_filtros
from utils.FormatoFechaHora import FormatoFechaHora
from utils.Graficar import graficar_historial, graficar_metricas
from utils.audio_utils import generar_vecino
from utils.guardar_contenido_json import guardar_contenido_json
from utils.poblacion import generar_individuo, generar_poblacion


# --- Recocido Simulado ---
def recocido_simulado():
    print("Recocido Simulado")

    audio_original = Audio(".\\..\\audio\\audio_test.wav")
    audio_original.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    print(f"Soundrate: {audio_original.sound_rate}")
    audio_original.normalizar_audio()

    generaciones_total = 30
    # gen_sin_mejora_lim = 10
    # gen_sin_mejora_count = 0

    for i in range(generaciones_total):
        # Estado inicial
        # for gen_global in range(generaciones_total):
        historial = []
        mejor_evaluacion = {"puntuacion": 0}
        mejor_estado = {}
        se_mejoro_gen = False
        generacion = 0

        temp_inicial = 100.0  # Temperatura inicial
        temp_min = 0.01  # Temperatura mínima
        alfa = 0.95  # Factor de enfriamiento

        # Generar solución inicial
        individuo_actual = generar_individuo()
        print(f"Individuo inicial: {individuo_actual}")

        audio_filtrado = aplicar_filtros(audio_original,
                                         low_cut=individuo_actual["low_cut"],
                                         high_cut=individuo_actual["high_cut"],
                                         orden=individuo_actual["filtro_order"],
                                         prop_decrease=individuo_actual["prop_decrease"])

        evaluacion_actual = {
            "zcr": zero_crosing_rate_mean(audio_filtrado, audio_original.sound_rate),
            "flatness": spectral_flatness_mean(audio_filtrado, audio_original.sound_rate),
            "rms": rms_energy_mean(audio_filtrado, audio_original.sound_rate)
        }
        evaluacion_actual["puntuacion"] = ponderar_calidad(
            zcr=evaluacion_actual["zcr"],
            spectral_flatness=evaluacion_actual["flatness"],
            rms_energy=evaluacion_actual["rms"]
        )

        # Inicializar mejor solución
        mejor = individuo_actual.copy()
        mejor_evaluacion = evaluacion_actual.copy()

        while temp_inicial > temp_min:
            # Generar vecino
            x_vecino = generar_vecino(individuo_actual, desplazamiento=temp_inicial)
            audio_vecino = aplicar_filtros(audio_original,
                                           low_cut=x_vecino["low_cut"],
                                           high_cut=x_vecino["high_cut"],
                                           orden=x_vecino["filtro_order"],
                                           prop_decrease=x_vecino["prop_decrease"])

            evaluacion_vecino = {
                "zcr": zero_crosing_rate_mean(audio_vecino, audio_original.sound_rate),
                "flatness": spectral_flatness_mean(audio_vecino, audio_original.sound_rate),
                "rms": rms_energy_mean(audio_vecino, audio_original.sound_rate)
            }
            evaluacion_vecino["puntuacion"] = ponderar_calidad(
                zcr=evaluacion_vecino["zcr"],
                spectral_flatness=evaluacion_vecino["flatness"],
                rms_energy=evaluacion_vecino["rms"]
            )

            # Diferencia de puntuación respecto al actual
            delta = evaluacion_vecino["puntuacion"] - evaluacion_actual["puntuacion"]

            # Aceptar si mejora o con probabilidad si es peor
            if delta > 0 or random.random() < math.exp(delta / temp_inicial):
                individuo_actual = x_vecino
                evaluacion_actual = evaluacion_vecino

                # Actualizar mejor global
                if evaluacion_vecino["puntuacion"] > mejor_evaluacion["puntuacion"]:
                    mejor = x_vecino.copy()
                    mejor_evaluacion = evaluacion_vecino.copy()
                    mejor_estado = mejor

            # Debug
            print(f"T={temp_inicial:.4f} | Mejor puntuación: {mejor_evaluacion['puntuacion']:.4f} | Fitness actual: {evaluacion_actual['puntuacion']:.4f}")
            # Enfriar temperatura
            temp_inicial *= alfa
            generacion += 1

            historial.append({
                "iter": generacion,
                "estado": mejor_estado,
                "zcr": mejor_evaluacion["zcr"],
                "flatness": mejor_evaluacion["flatness"],
                "rms": mejor_evaluacion["rms"],
                "ponderacion": mejor_evaluacion["puntuacion"]
            })

        print(f"\nMejor individuo global: {mejor}")
        print(f"Evaluación: {mejor_evaluacion}")
        nombre = f".\\..\\output\\json\\recocido_{audio_original.nombre_archivo.split(".")[0]}_{FormatoFechaHora.formatear_fecha_hora(datetime.now(), formato=FormatoFechaHora.Ymd_HMS)}.json"
        guardar_contenido_json(nombre, historial)
        # graficar_historial(historial=historial)
        # graficar_metricas(historial=historial)


if __name__ == '__main__':
    print("heuristica")
    recocido_simulado()