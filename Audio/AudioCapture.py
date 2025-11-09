import sounddevice as sd
import numpy as np

class AudioCapture:
    
    """
        Gestiona la captura de audio en tiempo real desd eel micrófono 
        utilizando la libreria sounddevice
    """
    
    def __init__(self,rate:int=44100, chunk_size: int=1024):
        #Constantes de audio
        self.RATE = rate #Frecuencia de muestreo (muestras por segundo)
        self.CHUNK_SIZE = chunk_size #Tamaño de los bloque de audio que hay que leer
        self.CHANNELS = 1 # Mono o Estero (Este caso MONO)
        self.DTYPE='int16' #Tipo de dato que maneja
        
        #Objeto stream (Propio de sounddevice)
        self.stream = None
        
        #Buffer (memoria) para almacenar los últimos datos leídos
        self.buffer = np.zeros(chunk_size,dtype=self.DTYPE)
        
        def callback(self,indata,frames,time,status):
            """
                Función que se llama automáticamente cuando hay nuevos datos de audio
            """
            
            if status:
                print(f"Error en el stream: {status}")
            
            #Almacena los nuevos datos en el buffer
            #Es crucial convertir los datos a int16 para el procesamiento
            self.buffer = indata[:,0]
            
        
        def start_stream(self):
            """
                Inicia la captura de audio en un hilo separado
            """
            # sd.InputStream utiliza la función 'callback' para leer datos asíncronos
            self.stream = sd.InputStream(
                samplerate=self.RATE,
                blocksize=self.CHUNK_SIZE,
                channels=self.CHANNELS,
                dtype=self.DTYPE,
                callback=self.callback
            )
            self.stream.start()
            print("Captura de audio iniciada- ")
            
        def read_chunk(self) -> np.ndarray:
            """
                Retorna el último bloque de audio capturado
            """
            return self.buffer
        
        def stop_Stream(self):
            """ 
                Detiene la captura de audio 
            """
            
            if self.stream and self.stream.is_active:
                self.stream.stop()
                self.stream.close()
                print("Captura de audio detenida")
                
                
            
            