import datetime
import json
import os
import numpy as np
from tkinter import filedialog

def seleccionar_ruta_guardar():
    ruta_guardar = filedialog.asksaveasfilename(title="Guardar archivo", filetypes=[("JSON (JavaScript Object Notation)", ".json"), ("Todos los archivos", "*.*")], defaultextension=".json")
    return ruta_guardar

def guardar_contenido_json(ruta_guardar=None, contenido=None):
    if ruta_guardar == None:
        try:
            ruta_guardar = seleccionar_ruta_guardar()
            if ruta_guardar == None or ruta_guardar == "":
                return  # No se asigno una ruta
        except Exception as e:
            print(f"No se puede guardar en esa direccion.\n{e}")
            return
    # Guardar el contenido del archivo
    with open(ruta_guardar, 'w', encoding='utf-8') as archivo:
        json.dump(contenido, archivo, indent=4, default=convertir_numpy_a_nativos)
        # json.dump(contenido, archivo, indent=4)

def convertir_numpy_a_nativos(obj):
    """
    Función auxiliar para json.dump que convierte tipos de NumPy
    a tipos nativos de Python.
    """
    # Manejar tipos enteros de NumPy
    if isinstance(obj, (np.integer)): # np.integer cubre todos los tipos int de NumPy
        return int(obj)
    # Manejar tipos flotantes de NumPy
    elif isinstance(obj, (np.floating)): # np.floating cubre todos los tipos float de NumPy
        return float(obj)
    # Manejar booleanos de NumPy
    elif isinstance(obj, (np.bool_)):
        return bool(obj)
    # Manejar arrays de NumPy
    elif isinstance(obj, np.ndarray):
        return obj.tolist() # Convierte arrays de NumPy a listas de Python
    # Manejar objetos datetime (si los tienes)
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat() # Formato ISO 8601 para fechas
    # Si ningún tipo específico de NumPy o datetime coincide, lanza un TypeError
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


if __name__ == "__main__":
    # Ejemplo de uso
    data = {"nombre": "John", "edad": 30, "ciudad": "New York"}
    ruta_archivo = "C:\\Users\\INTERNA_0\\Desktop\\datos.json"
    guardar_contenido_json(ruta_guardar=None, contenido=data)