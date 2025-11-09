import numpy as np

from .NoteConverter import NoteConverter

class FFTAnalyzer:
    """
        Procesa el audio con FFT ´para encotrar la frecuencia fundamental
        y utiliza NoteConverter para determinar la nota
    """
    
    def __init__(self, rate:int=44100):
        self.rate = rate
        #Conversor de notas
        self.note_converter = NoteConverter()
        
    def analyze_frequency(self,audio_chunk:np.ndarray)->float:
        """
            Calcula la frecuencia fundamental (f0) del bloque de audio.
        """
        # Paso 1: Aplicar una ventana (ej:Hanning) para reducir la fuga de la señal
        # La ventana es crucial para precisión de la FFT en tiempo real
        window = np.hanning(len(audio_chunk))
        windowed_data = audio_chunk * window
        
        # Paso 2: Aplicar la Transformada Rápida de Fourier (FFT)
        # np.fft.rfft optimiza para datos reales (no complejos)
        fft_result = np.fft.rfft(windowed_data)
        
        # Paso 3: Calcular las magnitudes (amplitud)
        # np.abs convierte los número complejos a una magnitud real
        
        maginitude = np.abs(fft_result)
        
        # Paso 4: Encontrar el índice (bin) de frecuencia con la mayor magnitud
        # Excluimos el primir bin (DC offset) y los bins de ruido de baja frecuencia
        #USamos [2:] para evitar el ruido de las frecuencias muy bajas
        peak_index = np.argmax(maginitude[2:]) + 2
        
        # Paso 5: Convertir el índice (bin) a frencuencia real (Hz)
        # Fórmula: Frecuencia = indice_pico * (RATE / CHUNK_SIZE)
        f0 = peak_index * (self.rate/len(audio_chunk))
        
        #Filtro de seguridad: retornamos 0 si la frecuencia está fuera del rango musical típico (ej: < 50Hz)
        
        if f0 < 50:
            return 0.0
        
        return f0
    
    def get_tuning_info(self,audio_chunk:np.ndarray) -> dict:
        """
            Realiza el análisis completo retorna la nota musical
        """
        
        f0 = self.analyze_frequency(audio_chunk)
        
        if f0 == 0.0:
            return {'note_full':'Silence/Noise','cents':0}
        
        #Delegamos la conversión a la clase NoteConverter
        return self.note_converter.get_note_info(f0)
    
    