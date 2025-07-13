import json
import os
from tkinter import filedialog

def seleccionar_archivo():
    ruta_archivo = filedialog.askopenfilename(title="Abrir archivo", filetypes=[("JSON (JavaScript Object Notation)", ".json")])
    return ruta_archivo

def seleccionar_directorio():
    ruta_directorio = filedialog.askdirectory()
    return ruta_directorio

def extraer_contenido_json(ruta_archivo=None):
    if ruta_archivo == None:
        try:
            ruta_archivo = seleccionar_archivo()
        except Exception as e:
            print(f"Incapaz de abrir archivo.\n{e}")
            return
    contenido = None
    # Verificar si la ruta es un archivo válido
    if os.path.isfile(ruta_archivo):
        # Leer el contenido del archivo
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            contenido = archivo.read()
        contenido = json.loads(contenido)  # Para convertir en un diccionario
    return contenido

if __name__ == "__main__":
    # Ejemplo de uso
    ruta_archivo = r"E:\Trabajos\ProyectoAnacual\Entrenamiento spaCy\code\data\raw_data\Día de Muertos - Wikipedia, la enciclopedia libre.json"
    contenido_archivo = extraer_contenido_json()
    print(contenido_archivo)