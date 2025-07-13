from datetime import datetime


class FormatoFechaHora:

    Ymd_HMS = "%Y%m%d_%H%M%S"

    @staticmethod
    def formatear_fecha_hora(fecha_hora: datetime, formato: str) -> str:
        return fecha_hora.strftime(formato)

