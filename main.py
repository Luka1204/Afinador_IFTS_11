import wave
import math
import struct
import cmath

""" 
Si pensamos el afinador como un plugin o un elemento adicionable a un sistema
de procesamiento de audio, este código puede ser la base para un afinador simple.
Si lo aplicamos a un paradigma POO, este archivo sería un scanner o analizador de audio.
Faltaria la posibilidad de analizar audio en tiempo real.

PASOS A SEGUIR PARA LECTURA EN TIEMPO REAL:
1. Capturar audio en tiempo real (p.ej., con pyaudio).
2. Dividir el audio en fragmentos (frames) de tamaño adecuado (p.ej., 1024 muestras).
3. Aplicar la FFT a cada fragmento para obtener el espectro de frecuencias. 
4. Identificar la frecuencia fundamental en cada espectro.
5. Convertir la frecuencia fundamental a una nota musical.
6. Mostrar la nota en tiempo real.


En el armado de clases se puede dividr:
- Clase AudioCapture: Maneja la captura de audio en tiempo real.
- Clase FFTAnalyzer: Realiza la FFT y analiza el espectro.
- Clase NoteConverter: Convierte frecuencias a notas musicales.

"""
# -----------------------
# FFT básica sin librerías externas
# -----------------------

def fft(signal): # => Transformada rápida de Fourier
    N = len(signal)
    if N <= 1:
        return signal
    even = fft(signal[0::2])
    odd = fft(signal[1::2])
    T = [cmath.exp(-2j * math.pi * k / N) * odd[k] for k in range(N // 2)]
    return [even[k] + T[k] for k in range(N // 2)] + \
    [even[k] - T[k] for k in range(N // 2)]
# -----------------------
# Convierte frecuencia en nota
# -----------------------
NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
def freq_to_note(freq): # En base a la frecuencia obtenida en la FFT, la divide por 440HZ (FREQ estandar en la música)
    if freq <= 0:
        return None
    n = round(12 * math.log2(freq / 440.0) + 69) # Utiliza la fórmula para convertir frecuencia a número MIDI (log2 para escala logarítmica) #*12 para semitonos y + 69 para la nota A4 (La cuarta) (440Hz)
    note_name = NOTES[n % 12] + str(n // 12 - 1) # MIDI → nota + octava # 12 por los semitonos en una octava, -1 para ajustar la octava
    return note_name
# -----------------------
# Procesar WAV
# -----------------------
def analyze_wav(filename):
    wav = wave.open(filename, "r") # Abrir archivo WAV
    nframes = wav.getnframes() # obtenemos el número de frecuencias
    framerate = wav.getframerate() # obtenemos la frecuencia de muestreo
    # Tomamos una muestra corta
    frames = wav.readframes(min(nframes, 4096)) # Leemos los frames (muestras de audio)
    wav.close()
    # Convertir bytes a enteros
    signal = struct.unpack("%dh" % (len(frames) // 2), frames)
    # FFT
    spectrum = fft(signal) #Calculamos la FFT de la señal
    magnitudes = [abs(x) for x in spectrum[:len(spectrum)//2]] # Magnitudes (valores absolutos) de la mitad del espectro (la otra mitad es simétrica)
    # Frecuencia fundamental = índice del máximo en el espectro
    peak_index = magnitudes.index(max(magnitudes))
    freq = peak_index * framerate / len(signal)
    note = freq_to_note(freq)
    4/4
    return freq, note
# -----------------------
# Uso
# -----------------------
freq, note = analyze_wav("waves/guitarra_MI_MENOR(Em).wav")
print(f"Frecuencia detectada: {freq:.2f} Hz → Nota: {note}")