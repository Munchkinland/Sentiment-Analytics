import librosa
import sounddevice as sd
import numpy as np
from transformers import pipeline
from transformers.pipelines.base import PipelineException
import tkinter as tk
from tkinter import filedialog
from moviepy.editor import VideoFileClip  # Importa moviepy

class AnalisisVoz:
    """Clase para el análisis de sentimientos en la voz."""

    def __init__(self, interfaz, tipo="video"):
        """Inicializa el clasificador de sentimientos y la interfaz gráfica."""
        self.interfaz = interfaz
        self.tipo = tipo
        try:
            self.clasificador = pipeline("audio-classification", model="superb/hubert-large-superb-er")
        except PipelineException as e:
            print(f"Error al cargar el modelo de clasificación de audio: {e}")
            self.clasificador = None

    def analizar_audio(self, audio):
        """Analiza el audio y devuelve el sentimiento."""
        if not self.clasificador:
            return "Error: Modelo no disponible"
        resultado = self.clasificador(audio)
        sentimiento = resultado[0]['label'] if resultado else "No detectado"
        return sentimiento

    def analizar_video(self):
        """Analiza el sentimiento en un video."""
        ruta_video = filedialog.askopenfilename()
        if not ruta_video:
            return

        # Extrae el audio del video
        with VideoFileClip(ruta_video) as video:
            audio_path = "audio_extracted.wav"
            video.audio.write_audiofile(audio_path)  # Guarda el audio en un archivo WAV

        # Carga el audio extraído
        audio, sr = librosa.load(audio_path, sr=16000)
        sentimiento = self.analizar_audio(audio)
        self.interfaz.actualizar_sentimiento_voz(sentimiento)

    def analizar_directo(self):
        """Analiza el sentimiento en la voz en directo."""
        fs = 44100  # Frecuencia de muestreo
        duracion = 5  # Duración de la grabación en segundos
        audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1)
        sd.wait()
        audio = np.squeeze(audio)
        sentimiento = self.analizar_audio(audio)
        self.interfaz.actualizar_sentimiento_voz(sentimiento)
