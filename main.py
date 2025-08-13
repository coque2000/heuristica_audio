from cffi.cffi_opcode import PRIM_INT8

from scripts.Audio import Audio
from scripts import EvaluarAudio
from scripts.EvaluarAudio import ponderar_calidad
from scripts.LimpiezaAudio import reducir_ruido

import copy

if __name__ == '__main__':
    sep = "-"
    n_sep = 50
    n_sep_medio = int(50 / 1.5)
    n_sep_75 = int(50 * .75)

    audio = Audio(".\\audio\\audio_test.wav")
    audio.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    print(f"Soundrate: {audio.sound_rate}")
    audio.normalizar_audio()


    print(f"El audio se esta evaluando".center(n_sep, sep))
    print(f"ZCR".center(n_sep_medio, sep))
    zcr = EvaluarAudio.zero_crosing_rate_mean(audio.audio, audio.sound_rate)
    print(zcr)
    print(f"SFM".center(n_sep_medio, sep))
    sfm = EvaluarAudio.spectral_flatness_mean(audio.audio, audio.sound_rate)
    print(sfm)
    print(f"RMS".center(n_sep_medio, sep))
    rms = EvaluarAudio.rms_energy_mean(audio.audio, audio.sound_rate)
    print(rms)
    print(f"Ponderacion: {ponderar_calidad(zcr, sfm, rms)}".center(n_sep_75, sep))

    prop_decrease = 0.05
    ponderacion_max = 0
    audio_np = audio.audio
    for i in range(100):
        audio_nuevo = audio_np
        audio_nuevo = reducir_ruido(audio_np, sound_rate= audio.sound_rate, prop_decrease=prop_decrease)
        print(f"El audio se esta evaluando".center(n_sep, sep))
        print(f"ZCR".center(n_sep_medio, sep))
        zcr = EvaluarAudio.zero_crosing_rate_mean(audio_nuevo, audio.sound_rate)
        print(zcr)
        print(f"SFM".center(n_sep_medio, sep))
        sfm = EvaluarAudio.spectral_flatness_mean(audio_nuevo, audio.sound_rate)
        print(sfm)
        print(f"RMS".center(n_sep_medio, sep))
        rms = EvaluarAudio.rms_energy_mean(audio_nuevo, audio.sound_rate)
        print(rms)

        ponderacion_val = ponderar_calidad(zcr, sfm, rms)
        if ponderacion_val > ponderacion_max:
            ponderacion_max = ponderacion_val
        print(f"Ponderacion: {ponderacion_val}".center(n_sep_75, sep))


        prop_decrease += .05


    print(f"Mejor ponderacion: {ponderacion_max}")







    