from scripts.FileUtils import *

import os
# import pydub
# from pydub import AudioSegment
import librosa
import numpy as np
import soundfile as sf


class Audio:
    def __init__(self, path):
        self._ruta_archivo = path
        self._audio = None
        self._lib_lectura = None
        self._rate = None

    """
    def leer_audio_pydub(self):
        try:
            comprobar_directorio(self._ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            audio = AudioSegment.from_file(self._ruta_archivo)
            self._audio = audio
            self._rate = audio.frame_rate
            self._lib_lectura = "pydub"
            \"""
            print(f"\n--- Información del archivo: {os.path.basename(self._ruta_archivo)} (con pydub) ---")
            print(f"Formato: {audio.export(format='wav').name.split('.')[-1].upper()} (estimado al exportar)")
            print(f"Canales: {'Mono' if audio.channels == 1 else 'Estéreo'}")
            print(f"Tasa de muestreo (Hz): {audio.frame_rate}")
            print(f"Profundidad de bits: {audio.sample_width * 8} bits")
            print(f"Duración: {len(audio) / 1000:.2f} segundos")
            \"""
            return audio, audio.frame_rate
        except Exception as e:
            raise Exception(f"Error al leer el archivo con pydub: {e}")
    """

    def leer_audio_soundfile(self):
        try:
            comprobar_directorio(self._ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            with sf.SoundFile(self._ruta_archivo, 'r') as f:
                """
                print(f"\n--- Información del archivo: {os.path.basename(self._ruta_archivo)} (con soundfile) ---")
                print(f"Formato: {f.format}")
                print(f"Subformato: {f.subtype}")
                print(f"Canales: {f.channels}")
                print(f"Tasa de muestreo (Hz): {f.samplerate}")
                print(f"Duración: {f.frames / f.samplerate:.2f} segundos")
                """
                data = f.read()
                # print(f"Shape de los datos de audio (frames, canales): {data.shape}")
                # return data, f.samplerate
                self._audio = data
                self._rate = f.samplerate
                self._lib_lectura = "soundfile"
                return data, f.samplerate
        except Exception as e:
            raise Exception(f"Error al leer el archivo con soundfile: {e}")

    def leer_audio_librosa(self, sample_rate: float, mono: bool = True):
        try:
            comprobar_directorio(self._ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            audio, sr = librosa.load(self._ruta_archivo, sr=sample_rate, mono=mono)
            self._audio = audio
            self._rate = sr
            return audio, sr
        except Exception as e:
            raise Exception(f"Error al leer el archivo con librosa: {e}")

    def convertir_canal_mono(self):
        if self._audio.ndim > 1:
            self._audio = np.mean(self._audio, axis=1)
        return self._audio, self._audio.sample_rate

    def normalizar_audio(self):
        """
            Normaliza la amplitud del audio entre -1.0 y 1.0 (peak normalization).
        """
        peak = np.max(np.abs(self._audio))
        if peak == 0:
            return self._audio  # Evita división por cero
        return self._audio / peak

    @property
    def ruta_archivo(self):
        return self._ruta_archivo

    @ruta_archivo.setter
    def ruta_archivo(self, ruta_archivo: str):
        self._ruta_archivo = ruta_archivo

    @property
    def audio(self):
        return self._audio

    @property
    def lib_lectura(self):
        return self._lib_lectura

    @property
    def rate(self):
        return self._rate

if __name__ == '__main__':
    print("main")