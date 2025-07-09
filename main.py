from cffi.cffi_opcode import PRIM_INT8

from scripts.Audio import Audio
from scripts import EvaluarAudio
from scripts.EvaluarAudio import ponderar_calidad

if __name__ == '__main__':
    sep = "-"
    n_sep = 50
    n_sep_medio = int(50 / 1.5)
    n_sep_75 = int(50 * .75)

    audio = Audio(".\\audio\\audio_test.wav")
    audio.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    audio.normalizar_audio()

    print(f"El audio se esta evaluando".center(n_sep, sep))
    print(f"ZCR".center(n_sep_medio, sep))
    zcr = EvaluarAudio.zero_crosing_rate_mean(audio.audio, audio.rate)
    print(zcr)
    print(f"SFM".center(n_sep_medio, sep))
    sfm = EvaluarAudio.spectral_flatness_mean(audio.audio, audio.rate)
    print(sfm)
    print(f"RMS".center(n_sep_medio, sep))
    rms = EvaluarAudio.rms_energy_mean(audio.audio, audio.rate)
    print(rms)
    print(f"Ponderacion: {ponderar_calidad(zcr, sfm, rms)}".center(n_sep_75, sep))





    