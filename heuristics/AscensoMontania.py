from datetime import datetime

import numpy as np

from scripts.Audio import Audio
from scripts.EvaluarAudio import zero_crosing_rate_mean, spectral_flatness_mean, rms_energy_mean, ponderar_calidad
from scripts.LimpiezaAudio import aplicar_filtro_pasabanda, reducir_ruido
from utils.FormatoFechaHora import FormatoFechaHora
from utils.Graficar import graficar_historial, graficar_metricas
from utils.guardar_contenido_json import guardar_contenido_json




def ascenso_montania_limpieza_audio():
    print("Ascenso montania")
    # Estado inicial
    estado = {
        "low_cut": 113,
        "high_cut": 7912,
        "filtro_order": 7,
        "prop_de_noise": 0.077
    }
    """
    estado = {
        "low_cut": 80,
        "high_cut": 8000,
        "filtro_order": 4,
        "prop_de_noise": 0.1
    }
    """

    audio_original = Audio(".\\..\\audio\\audio_test.wav")
    audio_original.leer_audio_librosa(44100, True)
    print(f"El audio fue leido")
    print(f"Soundrate: {audio_original.sound_rate}")
    audio_original.normalizar_audio()

    mejor_puntuaje = -1
    mejor_audio = None
    mejor_estado: dict = {}
    iteraciones_sin_mejora = 0
    max_iteraciones = 1000
    max_iteraciones_sin_mejora = 20
    historial = []



    for i in range(max_iteraciones):
        print(f"Iteracion: {i}")
        nuevo_estado = {
            "low_cut": max(20, min(estado["low_cut"] + np.random.randint(-20, 20), 1000)),
            "high_cut": max(estado["low_cut"] + 1000, min(estado["high_cut"] + np.random.randint(-200, 200), 16000)),
            "filtro_order": min(max(1, estado["filtro_order"] + np.random.choice([-1, 0, 1])), 8),
            "prop_de_noise": round(min(max(0.05, estado["prop_de_noise"] + np.random.uniform(-0.02, 0.02)), 0.5), 3)
        }

        audio_filtrado = aplicar_filtro_pasabanda(audio=audio_original, low_cut=nuevo_estado["low_cut"], high_cut=nuevo_estado["high_cut"], orden=nuevo_estado["filtro_order"])
        audio_limpio = reducir_ruido(audio=audio_filtrado, sound_rate=audio_original.sound_rate, prop_decrease=nuevo_estado["prop_de_noise"])

        if not np.all(np.isfinite(audio_limpio)):
            print("⚠️ El audio contiene valores no finitos. Se limpiará.")
            audio_limpio = np.nan_to_num(audio_limpio, nan=0.0, posinf=1.0, neginf=-1.0)

        # Evaluar
        zcr = zero_crosing_rate_mean(audio_limpio, audio_original.sound_rate)
        flatness = spectral_flatness_mean(audio_limpio, audio_original.sound_rate)
        rms = rms_energy_mean(audio_limpio, audio_original.sound_rate)
        puntuacion = ponderar_calidad(zcr=zcr, spectral_flatness=flatness, rms_energy=rms)

        historial.append({
            "iter": i,
            "estado": nuevo_estado,
            "zcr": zcr,
            "flatness": flatness,
            "rms": rms,
            "ponderacion": puntuacion
        })

        print(f"Ponderacion: {puntuacion}")

        if puntuacion > mejor_puntuaje:
            mejor_puntuaje = puntuacion
            mejor_audio = audio_limpio
            mejor_estado = nuevo_estado.copy()
            estado = nuevo_estado.copy()  # movernos a la nueva solución
            iteraciones_sin_mejora = 0
        else:
            iteraciones_sin_mejora += 1

        if iteraciones_sin_mejora >= max_iteraciones_sin_mejora:
            print(f"Iteraciones sin mejora superadas: {i}")
            break

    print("Mejor configuración encontrada:", mejor_estado)
    # graficar_historial(historial=historial)
    # graficar_metricas(historial=historial)
    nombre = f".\\..\\output\\{audio_original.nombre_archivo.split(".")[0]}_{FormatoFechaHora.formatear_fecha_hora(datetime.now(), formato=FormatoFechaHora.Ymd_HMS)}.json"
    guardar_contenido_json(nombre, historial)
    return mejor_audio, mejor_puntuaje, mejor_estado, historial




"""
%%%%
%%%%Asenso_montaña ackley
%%%
%%% entrada
%%%
%% Problema
clear all
close all
a=20;
b=.2;
c=2*pi();
dimenciones=2;
%%% parametros metodo
n_iteraciones_cambio=1000;
epsilon=.000000001;
vecinos=20;
distancia_max=1;
corridas=30;
NEFO=zeros(corridas,1);
for corrida=1:corridas
    %%%% generar una solucion inial
    for j=1:dimenciones
        sol(corrida,j)=-100+rand()*200;
    end
    objetivo(corrida,1)=evaluar(sol(corrida,:),dimenciones,a,b,c);
    NEFO(corrida,1)=NEFO(corrida,1)+1;
    %%%%%
    % vecinos
    mejora=0;
    while mejora < n_iteraciones_cambio
        sol_vecionos=[];
        objetivo_vecino=[];
        for v=1:vecinos
            sol_vecionos(v,:)=sol(corrida,:);
            cambio=-distancia_max+rand(1,dimenciones)*(2*distancia_max);
            sol_vecionos(v,:)=sol_vecionos(v,:)+cambio;
            for k=1:dimenciones
                if sol_vecionos(v,k)<-100
                    sol_vecionos(v,k)=-100;
                end
                if sol_vecionos(v,k)>100
                    sol_vecionos(v,k)=100;
                end
            end
            objetivo_vecino(v,1)=evaluar(sol_vecionos(v,:),dimenciones,a,b,c);
            NEFO(corrida,1)=NEFO(corrida,1)+1;
        end
        [a1,a2]=min(objetivo_vecino);
        if a1<objetivo(corrida,1)
            %%% remplazo
            sol(corrida,:)=sol_vecionos(a2,:);
            objetivo(corrida,1)=objetivo_vecino(a2,1);
            if objetivo(corrida,1)-a1<epsilon
                mejora=mejora+1;
            else
                mejora=0;
            end
        else
            mejora=1+mejora;
        end
    end
end
function [ob]=evaluar(sol,dimenciones,a,b,c)
ob=-a*(exp(-b*sqrt((1/dimenciones)*sum(sol.^2))))-exp((1/dimenciones)*sum(cos(c*sol)))+a+exp(1);
end

%%%%
%%%%Asenso_montaña ackley
%%%
%%% entrada
%%%
%% Problema
clear all
close all
a=20;
b=.2;
c=2*pi();
dimenciones=2;
%%% parametros metodo
n_iteraciones_cambio=1000;
epsilon=.000000001;
vecinos=20;
distancia_max=1;
corridas=30;
NEFO=zeros(corridas,1);
for corrida=1:corridas
    %%%% generar una solucion inial
    for j=1:dimenciones
        sol(corrida,j)=-100+rand()*200;
    end
    objetivo(corrida,1)=evaluar(sol(corrida,:),dimenciones,a,b,c);
    NEFO(corrida,1)=NEFO(corrida,1)+1;
    %%%%%
    % vecinos
    for movimientos=1:5
        sol_movida=-10+20*rand(1,dimenciones)+sol(corrida,:);
        objetivo_movida=evaluar(sol_movida,dimenciones,a,b,c);
        NEFO(corrida,1)=NEFO(corrida,1)+1;
        mejora=0;
        while mejora < n_iteraciones_cambio
            sol_vecionos=[];
            objetivo_vecino=[];
            for v=1:vecinos
                sol_vecionos(v,:)=sol_movida;
                cambio=-distancia_max+rand(1,dimenciones)*(2*distancia_max);
                sol_vecionos(v,:)=sol_vecionos(v,:)+cambio;
                for k=1:dimenciones
                    if sol_vecionos(v,k)<-100
                        sol_vecionos(v,k)=-100;
                    end
                    if sol_vecionos(v,k)>100
                        sol_vecionos(v,k)=100;
                    end
                end
                objetivo_vecino(v,1)=evaluar(sol_vecionos(v,:),dimenciones,a,b,c);
                NEFO(corrida,1)=NEFO(corrida,1)+1;
            end
            [a1,a2]=min(objetivo_vecino);
            if a1<objetivo_movida
                %%% remplazo
                sol_movida=sol_vecionos(a2,:);
                objetivo_movida=objetivo_vecino(a2,1);
                mejora=0;
            else
                mejora=1+mejora;
            end
        end
        if objetivo_movida<objetivo(corrida,1)
            objetivo(corrida,1)=objetivo_movida;
            sol(corrida,:)=sol_movida;
        end
    end
end
function [ob]=evaluar(sol,dimenciones,a,b,c)
ob=-a*(exp(-b*sqrt((1/dimenciones)*sum(sol.^2))))-exp((1/dimenciones)*sum(cos(c*sol)))+a+exp(1);
end
"""


if __name__ == '__main__':
    print("heuristica")
    ascenso_montania_limpieza_audio()

