import math

class NoteConverter:
    """
    Convierte una frecuencia (Hz) detectada en un nombre de nota musical 
    y calcula el desvío en 'cents' (afinación fina).
    Utiliza solo Python nativo (math).
    """
    
    # Constantes musicales estándar
    STANDARD_A4 = 440.0  # Frecuencia de la nota A4 (La 4)
    SEMITONES_PER_OCTAVE = 12
    # Nombres de las 12 notas cromáticas, empezando por C (Do)
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, a4_freq=STANDARD_A4):
        """Inicializa con una frecuencia base de referencia (por defecto 440 Hz)."""
        self.a4_freq = a4_freq

    def _frequency_to_midi(self, f: float) -> int:
        """
        Calcula el número MIDI (entero) de la nota más cercana a la frecuencia 'f'.
        El número MIDI para A4 (440 Hz) es 69.
        Fórmula: n = 12 * log2(f / A4) + 69
        """
        if f <= 0:
            return 0
        
        # 69 es el número MIDI de A4 (440 Hz)
        n = self.SEMITONES_PER_OCTAVE * math.log2(f / self.a4_freq) + 69
        
        # Redondeamos al número MIDI entero más cercano
        return round(n)

    def get_note_info(self, f: float) -> dict:
        """
        Retorna un diccionario con el nombre de la nota y su desvío en cents.
        """
        if f <= 0:
            return {'note': 'N/A', 'octave': 0, 'cents': 0}
        
        # 1. Obtener número MIDI entero de la nota más cercana
        midi_number = self._frequency_to_midi(f)
        
        # 2. Calcular el nombre de la nota (0=C, 1=C#, ..., 11=B)
        note_index = midi_number % self.SEMITONES_PER_OCTAVE
        note_name = self.NOTE_NAMES[note_index]
        
        # 3. Calcular la octava (Octava 4 = notas MIDI 60 a 71)
        # La nota C4 es MIDI 60. Octava = floor((midi_number / 12) - 1)
        octave = (midi_number // self.SEMITONES_PER_OCTAVE) - 1
        
        # 4. Calcular la frecuencia ideal (perfectamente afinada) de esa nota MIDI
        f_ideal = self.a4_freq * (2 ** ((midi_number - 69) / self.SEMITONES_PER_OCTAVE))
        
        # 5. Calcular el desvío en 'cents' (afinación fina).
        # Hay 100 cents en cada semitono.
        cents_offset = self.SEMITONES_PER_OCTAVE * 100 * math.log2(f / f_ideal)
        
        return {
            'note': note_name,
            'octave': octave,
            'note_full': f'{note_name}{octave}',
            'cents': round(cents_offset)
        }