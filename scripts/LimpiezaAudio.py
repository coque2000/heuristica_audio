import noisereduce as nr
from scipy import signal
import numpy as np

from scripts.Audio import Audio


def aplicar_filtro_pasabanda(audio: Audio, low_cut: int = 80, high_cut: int = 8000, orden: int =4):
    nyquist = audio.sound_rate / 2
    low = low_cut / nyquist
    high = high_cut / nyquist
    b, a = signal.butter(orden, [low, high], btype='band')
    return signal.lfilter(b, a, audio.audio)

"""
def reducir_ruido(audio: Audio, prop_decrease: float = 1.0):
    return nr.reduce_noise(y=audio.audio, sr=audio.sound_rate, prop_decrease=prop_decrease)
"""

def reducir_ruido(audio: np.ndarray, sound_rate: int, prop_decrease: float = 1.0):
    return nr.reduce_noise(y=audio, sr=sound_rate, prop_decrease=prop_decrease)

def aplicar_filtros(audio: Audio, low_cut: int = 80, high_cut: int = 8000, orden: int = 4, sound_rate: int = 44100, prop_decrease: float = 1.0):
    audio_filtrado = aplicar_filtro_pasabanda(audio=audio, low_cut=low_cut, high_cut=high_cut, orden=orden)
    audio_limpio = reducir_ruido(audio=audio_filtrado, sound_rate=sound_rate, prop_decrease=prop_decrease)

    if not np.all(np.isfinite(audio_limpio)):
        print("⚠️ El audio contiene valores no finitos. Se limpiará.")
        audio_limpio = np.nan_to_num(audio_limpio, nan=0.0, posinf=1.0, neginf=-1.0)
    return audio_limpio
