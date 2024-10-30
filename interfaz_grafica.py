import tkinter as tk
from tkinter import ttk
import cv2

class InterfazGrafica:
    """Clase para la interfaz gráfica de la aplicación."""

    def __init__(self):
        """Inicializa la ventana principal y los elementos de la interfaz."""
        self.ventana = tk.Tk()
        self.ventana.title("Análisis de Sentimientos")
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)

        # Frame para la cámara.
        self.frame_camara = ttk.LabelFrame(self.ventana, text="Cámara")
        self.frame_camara.grid(row=0, column=0, padx=10, pady=10)
        self.label_video = tk.Label(self.frame_camara)
        self.label_video.pack()

        # Frame para los resultados del análisis de expresiones.
        self.frame_expresiones = ttk.LabelFrame(self.ventana, text="Expresiones")
        self.frame_expresiones.grid(row=1, column=0, padx=10, pady=10)
        self.label_expresion = tk.Label(self.frame_expresiones, text="Expresión: ")
        self.label_expresion.pack()

        # Frame para el análisis de voz.
        self.frame_voz = ttk.LabelFrame(self.ventana, text="Voz")
        self.frame_voz.grid(row=0, column=1, rowspan=2, padx=10, pady=10)

        # Botones para análisis de voz.
        self.boton_video = ttk.Button(self.frame_voz, text="Analizar Video")
        self.boton_video.pack(pady=5)
        self.boton_directo = ttk.Button(self.frame_voz, text="Analizar en Directo")
        self.boton_directo.pack(pady=5)

        # Label para mostrar los resultados del análisis de voz.
        self.label_sentimiento_voz = tk.Label(self.frame_voz, text="Sentimiento: ")
        self.label_sentimiento_voz.pack()

    def conectar_analizador_expresiones(self, analizador):
        """Conecta el analizador de expresiones a la interfaz."""
        self.analizador_expresiones = analizador
        self.analizador_expresiones.iniciar_analisis()

    def conectar_analizador_voz_video(self, analizador):
        """Conecta el analizador de voz de video a la interfaz."""
        self.analizador_voz_video = analizador
        self.boton_video.config(command=self.analizador_voz_video.analizar_video)

    def conectar_analizador_voz_directo(self, analizador):
        """Conecta el analizador de voz en directo a la interfaz."""
        self.analizador_voz_directo = analizador
        self.boton_directo.config(command=self.analizador_voz_directo.analizar_directo)

    def actualizar_imagen(self, imagen):
        """Actualiza la imagen en el frame de la cámara."""
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        imagen_tk = tk.PhotoImage(data=cv2.imencode('.png', imagen)[1].tobytes())
        self.label_video.config(image=imagen_tk)
        self.label_video.image = imagen_tk

    def actualizar_expresion(self, expresion):
        """Actualiza la etiqueta con la expresión detectada."""
        self.label_expresion.config(text=f"Expresión: {expresion}")

    def actualizar_sentimiento_voz(self, sentimiento):
        """Actualiza la etiqueta con el sentimiento detectado en la voz."""
        self.label_sentimiento_voz.config(text=f"Sentimiento: {sentimiento}")

    def cerrar(self):
        """Cierra la cámara y la aplicación de manera segura."""
        if hasattr(self, 'analizador_expresiones'):
            self.analizador_expresiones.cerrar()
        self.ventana.destroy()

    def iniciar(self):
        """Inicia el bucle principal de la interfaz gráfica."""
        self.ventana.mainloop()
