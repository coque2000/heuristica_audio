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