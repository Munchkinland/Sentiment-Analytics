# Archivo: main.py

from interfaz_grafica import InterfazGrafica
from analisis_expresiones import AnalisisExpresiones
from analisis_voz import AnalisisVoz

def main():
    """Función principal para ejecutar la aplicación."""

    # Inicializar la interfaz gráfica.
    interfaz = InterfazGrafica()

    # Inicializar los analizadores de expresiones y voz.
    analizador_expresiones = AnalisisExpresiones(interfaz)
    analizador_voz_video = AnalisisVoz(interfaz, tipo="video")
    analizador_voz_directo = AnalisisVoz(interfaz, tipo="directo")

    # Conectar los analizadores a la interfaz gráfica.
    interfaz.conectar_analizador_expresiones(analizador_expresiones)
    interfaz.conectar_analizador_voz_video(analizador_voz_video)
    interfaz.conectar_analizador_voz_directo(analizador_voz_directo)

    # Iniciar la interfaz gráfica.
    interfaz.iniciar()

if __name__ == "__main__":
    main()