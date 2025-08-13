from scripts.EvaluarAudio import ponderar_calidad

def calcular_fitness(parametros_audios: list[dict]):
    fitness = []
    for parametro in parametros_audios:
        # Si coupas algun otra metrica para ponderar la calidad reemplaza el algoritmo en "ponderar_calidad"
        fitness.append(ponderar_calidad(zcr=parametro["zcr"], spectral_flatness=parametro["flatness"], rms_energy=parametro["rms"]))
    return fitness


"""
zcr = zero_crosing_rate_mean(audio_limpio, audio_original.sound_rate)
            flatness = spectral_flatness_mean(audio_limpio, audio_original.sound_rate)
            rms = rms_energy_mean(audio_limpio, audio_original.sound_rate)
            puntuacion = ponderar_calidad(zcr=zcr, spectral_flatness=flatness, rms_energy=rms)
"""