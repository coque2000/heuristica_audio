import librosa
import noisereduce as nr
import scipy.signal as signal
import soundfile as sf

# 1. Cargar audio
audio, sr = librosa.load("../audio/audio_test.wav", sr=None)

# 2. Aplicar filtro pasa banda
low = 80 / (sr / 2)
high = 8000 / (sr / 2)
b, a = signal.butter(4, [low, high], btype='band')
filtered = signal.lfilter(b, a, audio)

# 3. Reducir ruido
cleaned = nr.reduce_noise(y=filtered, sr=sr)

# 4. Guardar resultado
sf.write("../audio/limpio_0.wav", cleaned, sr)
