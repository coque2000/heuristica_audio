import FileUtils

import os
import pydub
from pydub import AudioSegment
import soundfile as sf
import numpy as np


class Audio:
    def __init__(self, path):
        self.ruta_archivo = path
        self._audio = None
        self._lib_lectura = None
        self._rate = None

    def leer_audio_pydub(self):
        try:
            FileUtils.comprobar_directorio(self.ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            audio = AudioSegment.from_file(self.ruta_archivo)
            self._audio = audio
            self._rate = audio.frame_rate
            self._lib_lectura = "pydub"
            """
            print(f"\n--- Información del archivo: {os.path.basename(self.ruta_archivo)} (con pydub) ---")
            print(f"Formato: {audio.export(format='wav').name.split('.')[-1].upper()} (estimado al exportar)")
            print(f"Canales: {'Mono' if audio.channels == 1 else 'Estéreo'}")
            print(f"Tasa de muestreo (Hz): {audio.frame_rate}")
            print(f"Profundidad de bits: {audio.sample_width * 8} bits")
            print(f"Duración: {len(audio) / 1000:.2f} segundos")
            """
            return audio, audio.frame_rate
        except Exception as e:
            raise Exception(f"Error al leer el archivo con pydub: {e}")

    def leer_audio_soundfile(self):
        try:
            FileUtils.comprobar_directorio(self.ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            with sf.SoundFile(self.ruta_archivo, 'r') as f:
                """
                print(f"\n--- Información del archivo: {os.path.basename(self.ruta_archivo)} (con soundfile) ---")
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

    def convertir_canal_mono(self):
        if self._audio.ndim > 1:
            self._audio = np.mean(self._audio, axis=1)
        return self._audio, self._audio.sample_rate

    @property
    def audio(self):
        return self._audio

    @property
    def lib_lectura(self):
        return self._lib_lectura

    @property
    def rate(self):
        return self._rate
