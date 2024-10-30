import cv2
from fer import FER  # Asegúrate de tener instalada la biblioteca fer
from transformers.pipelines.base import PipelineException

class AnalisisExpresiones:
    """Clase para el análisis de expresiones faciales."""

    def __init__(self, interfaz):
        """Inicializa el clasificador de expresiones y la interfaz gráfica."""
        self.interfaz = interfaz
        try:
            self.clasificador = FER()  # Inicializa el clasificador FER
        except Exception as e:
            print(f"Error al cargar el clasificador de emociones faciales: {e}")
            self.clasificador = None
            
        self.camara = cv2.VideoCapture(0)
        self.detector_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    def iniciar_analisis(self):
        """Inicia el análisis de expresiones en tiempo real."""
        self.analizar_frame()

    def analizar_frame(self):
        """Analiza un frame de la cámara y actualiza la interfaz."""
        ret, frame = self.camara.read()
        if ret:
            rostros = self.detector_rostros.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5)
            if rostros is not None and self.clasificador:
                for (x, y, w, h) in rostros:
                    rostro = frame[y:y+h, x:x+w]
                    resultado = self.clasificador.detect_emotions(rostro)  # Detectar emociones
                    if resultado:
                        # Obtener la emoción con la puntuación más alta
                        expresion = max(resultado[0]['emotions'], key=resultado[0]['emotions'].get)
                        self.interfaz.actualizar_expresion(expresion)  # Actualizar la interfaz con la emoción
            self.interfaz.actualizar_imagen(frame)
        self.interfaz.ventana.after(10, self.analizar_frame)

    def cerrar(self):
        """Libera la cámara al cerrar la aplicación."""
        self.camara.release()
