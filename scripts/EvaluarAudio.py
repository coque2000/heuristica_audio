import librosa
# import webrtcvad

"""
    Se espera que los valores cumplan lo siguiente:
    zrc: limpio = 0.02 - 0.08, sucio = >= 0.1
    spectral_flatness: limpio = 0.1 - 0.3, sucio = >= 0.4
    rms_energy: limpio = 0.01 - 0.1, sucio = < 000.5 o > 0.15
"""
calidad_audio_referencia = {
    "ZCR": {
        "rango_bueno": (0.02, 0.08),
        "rango_malo": (0.1, float("inf")),
        "interpretacion": "Muy alto indica ruido impulsivo (estática, clics)."
    },
    "Spectral_Flatness": {
        "rango_bueno": (0.1, 0.3),
        "rango_malo": (0.4, float("inf")),
        "interpretacion": "Plano = ruido blanco. Bajo = voz con armónicos."
    },
    "RMS_Energy": {
        "rango_bueno": (0.01, 0.1),
        "rango_malo": [(0, 0.005), (0.15, float("inf"))],
        "interpretacion": "Bajo = silencio o señal débil. Alto = clipping o distorsión."
    },
    "VAD_Voice_Ratio": {
        "rango_bueno": (0.6, 1.0),
        "rango_malo": (0, 0.5),
        "interpretacion": "Proporción de voz detectada. Bajo = silencios o ruido dominante."
    }
}

def zero_crosing_rate_mean(audio, sr):
    """
    Evalua el número de veces que la señal cambia de signo (de positivo a negativo o viceversa) por segundo.
    """
    zrc = librosa.feature.zero_crossing_rate(audio)
    return zrc.mean()

def spectral_flatness_mean(audio, sr):
    """
    Evalua que tan plano es el espectro de frecuencias, una voz natural deberia tener valores bajos ya que es armonica
    """
    flatness = librosa.feature.spectral_flatness(y = audio)[0]
    return flatness.mean()

def rms_energy_mean(audio, sr):
    """
    Mide cuan fuerte es la señal en promedio, detecta problemas de volumen o distorsion
    """
    rms = librosa.feature.rms(y = audio)[0]
    return rms.mean()

def ponderar_calidad(zcr: float, spectral_flatness: float, rms_energy: float) -> float:
    """
    Pondera los valores de las métricas y proporciona un valor acumulado (0 a 3).
    """
    metrica = 0

    zcr_bueno = calidad_audio_referencia["ZCR"]["rango_bueno"]
    zcr_malo = calidad_audio_referencia["ZCR"]["rango_malo"]

    if zcr_bueno[0] <= zcr <= zcr_bueno[1]:
        metrica += 1
    elif zcr >= zcr_malo[0]:
        metrica += 0.5

    flat_bueno = calidad_audio_referencia["Spectral_Flatness"]["rango_bueno"]
    flat_malo = calidad_audio_referencia["Spectral_Flatness"]["rango_malo"]

    if flat_bueno[0] <= spectral_flatness <= flat_bueno[1]:
        metrica += 1
    elif spectral_flatness >= flat_malo[0]:
        metrica += 0.5

    rms_bueno = calidad_audio_referencia["RMS_Energy"]["rango_bueno"]
    rms_malo = calidad_audio_referencia["RMS_Energy"]["rango_malo"]

    if rms_bueno[0] <= rms_energy <= rms_bueno[1]:
        metrica += 1
    elif any(lower <= rms_energy <= upper for (lower, upper) in rms_malo):
        metrica += 0.5

    return round(metrica, 2)

"""
def vad_voice_ratio(audio, sr, frame_duration_ms=30):
    vad = webrtcvad.Vad()
    vad.set_mode(1)  # 0: menos agresivo, 3: muy agresivo

    # Convertir a formato 16-bit PCM
    import struct
    audio_int16 = (audio * 32768).astype('int16')
    audio_bytes = struct.pack('<' + 'h'*len(audio_int16), *audio_int16)

    frame_length = int(sr * frame_duration_ms / 1000)
    num_frames = len(audio_bytes) // (2 * frame_length)

    voiced = 0
    total = 0

    for i in range(num_frames):
        start = i * frame_length * 2
        end = start + frame_length * 2
        frame = audio_bytes[start:end]

        if len(frame) < frame_length * 2:
            break
        is_speech = vad.is_speech(frame, sr)
        voiced += int(is_speech)
        total += 1

    return voiced / total if total > 0 else 0.0
"""



if __name__ == "__main__":
    ponderacion = ponderar_calidad(zcr = 0.1, spectral_flatness = 0.1, rms_energy = 0.01)
    print(ponderacion)