import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import read

def graficar_audio(audio_0: str):
    if audio_0 is None or audio_0 == "":
        raise TypeError("Nombres de audio no pueden ser vacios")

    try:
        # (samplerate, data) = read(file)
        audio_wave = read(audio_0)
    except FileNotFoundError:
        raise FileNotFoundError("No se ha proporcionado un archivo")

    amplitud = amplitud_tiempo_audio(audio_wave[0], audio_wave[1])

    plt.plot(amplitud, audio_wave[1])
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud")
    plt.title(f"Forma de onda del audio: {audio_0}")
    plt.legend("onda audio")
    plt.show()



def amplitud_tiempo_audio(samplerate, data):
    if samplerate is None or data is None:
        raise TypeError("Los datos son no pueden ser vacios")

    # Obtener la amplitud y el tiempo
    if len(data.shape) > 1:  # Si es audio estéreo
        print(f"Hay {data.shape} canales")
        print(data)
        data = data[:, 0]  # Tomar solo un canal
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])
    return time



if __name__ == "__main__":
    graficar_audio("../audio/audio_test.wav")
    graficar_audio("../audio/limpio.wav")