import FileUtils

import os
import pydub
from pydub import AudioSegment
import soundfile as sf
import numpy as np


class Audio:
    def __init__(self, path):
        self.ruta_archivo = path
        self.audio = None
        self._lib_lectura = None

    def leer_audio_pydub(self):
        try:
            FileUtils.comprobar_directorio(self.ruta_archivo)
        except Exception as e:
            print(f"Error al querer recuperar el audio: {e}")
        try:
            audio = AudioSegment.from_file(self.ruta_archivo)
            self.audio = audio
            self._lib_lectura = "pydub"
            """
            print(f"\n--- Información del archivo: {os.path.basename(self.ruta_archivo)} (con pydub) ---")
            print(f"Formato: {audio.export(format='wav').name.split('.')[-1].upper()} (estimado al exportar)")
            print(f"Canales: {'Mono' if audio.channels == 1 else 'Estéreo'}")
            print(f"Tasa de muestreo (Hz): {audio.frame_rate}")
            print(f"Profundidad de bits: {audio.sample_width * 8} bits")
            print(f"Duración: {len(audio) / 1000:.2f} segundos")
            """
            return audio
        except Exception as e:
            raise Exception(f"Error al leer el archivo con pydub: {e}")

    def leer_audio_




    @property
    def lib_lectura(self):
        return self._lib_lectura

