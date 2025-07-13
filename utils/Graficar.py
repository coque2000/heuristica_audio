import matplotlib.pyplot as plt

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