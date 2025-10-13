import matplotlib.pyplot as plt

from utils.extraer_contenido_json import extraer_contenido_json


def graficar_historial(historial):
    iteraciones = [h["iter"] for h in historial]
    puntuaciones = [h["ponderacion"] for h in historial]

    plt.figure(figsize=(10, 5))
    plt.plot(iteraciones, puntuaciones, marker='o', linestyle='-', color='teal')
    plt.title("Mejora en la calidad del audio durante ascenso en la montaña")
    plt.xlabel("Iteración")
    plt.ylabel("Puntuación de calidad (ponderación)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def graficar_metricas(historial):
    iteraciones = [h["iter"] for h in historial]
    zcr = [h["zcr"] for h in historial]
    flatness = [h["flatness"] for h in historial]
    rms = [h["rms"] for h in historial]

    plt.figure(figsize=(10, 6))
    plt.plot(iteraciones, zcr, label="ZCR", marker='o')
    plt.plot(iteraciones, flatness, label="Flatness", marker='x')
    plt.plot(iteraciones, rms, label="RMS Energy", marker='^')
    plt.title("Evolución de métricas del audio")
    plt.xlabel("Iteración")
    plt.ylabel("Valor")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graficar_historiales(historiales: list[dict], titulo: str = "Mejora en la calidad del audio"):

    iteraciones = [h for h in historiales[0]]

    plt.figure(figsize=(10, 5))

    for i, puntuaciones in enumerate(historiales):
        iteraciones = range(1, len(puntuaciones) + 1)
        plt.plot(iteraciones, puntuaciones, marker='o', linestyle='-', label=f'Historial {i + 1}')


    plt.title(titulo)
    plt.xlabel("Iteración")
    plt.ylabel("Puntuación de calidad (ponderación)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    base_dir = "D:\\Coque2000\\Repositorios\\heuristica_audio\\output\\json\\"
    """
    directorios = [
        "genetico_audio_test_20250814_134302.json",
        "genetico_audio_test_20250814_141112.json",
        "genetico_audio_test_20250814_143631.json",
        "genetico_audio_test_20250814_150153.json",
        "genetico_audio_test_20250814_153230.json",
        "genetico_audio_test_20250814_160020.json",
        "genetico_audio_test_20250814_162707.json",
        "genetico_audio_test_20250814_165246.json",
        "genetico_audio_test_20250814_171735.json",
        "genetico_audio_test_20250814_190656.json"
    ]
    """
    """
    directorios = [
        "recocido_audio_test_20250814_151711.json",
        "recocido_audio_test_20250814_151807.json",
        "recocido_audio_test_20250814_151902.json",
        "recocido_audio_test_20250814_151958.json",
        "recocido_audio_test_20250814_152055.json",
        "recocido_audio_test_20250814_152157.json",
        "recocido_audio_test_20250814_152345.json",
        "recocido_audio_test_20250814_152440.json",
        "recocido_audio_test_20250814_152533.json",
        "recocido_audio_test_20250814_152627.json"
    ]
    """

    directorios = [
        "wolf_audio_test_20250814_195849.json",
        "wolf_audio_test_20250814_200324.json",
        "wolf_audio_test_20250814_200819.json",
        "wolf_audio_test_20250814_201250.json",
        "wolf_audio_test_20250814_201733.json",
        "wolf_audio_test_20250814_202157.json",
        "wolf_audio_test_20250814_231859.json",
        "wolf_audio_test_20250814_232407.json",
        "wolf_audio_test_20250814_232806.json",
        "wolf_audio_test_20250814_233210.json",
    ]

    historiales = []

    for directorio in directorios:
        historial = []
        cont_json = extraer_contenido_json(base_dir + directorio)
        print(cont_json)
        for subcont_json in cont_json:
            historial.append(subcont_json["ponderacion"])
        historiales.append(historial)

    # for historial in historiales:
    #     print(historial)

    graficar_historiales(historiales=historiales, titulo="Mejora en la calidad del audio durante GWO")