import os

def comprobar_directorio(ruta_archivo: str) -> bool:
    if ruta_archivo is None or ruta_archivo == "":
        raise TypeError(f"La ruta del archivo no puede ser vacio")

    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"El archivo {ruta_archivo} no se encontro")

    return True