import time
from datetime import datetime

if __name__ == "__main__":
    unix_timestamp = time.time()
    print(f"Unix Timestamp (seconds): {unix_timestamp}")

    print(datetime.now())

    # 1. Obtener la fecha y hora actual
    ahora = datetime.now()

    # 2. Formatear la fecha y hora para el nombre del archivo
    # YYYYMMDD_HHMMSS (ej. 20250712_235600)
    timestamp_str = ahora.strftime("%Y%m%d_%H%M%S")
    print(timestamp_str)