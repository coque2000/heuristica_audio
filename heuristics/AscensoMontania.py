def ascenso_montania():
    print("ascenso")

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
2 sem
Responder
Roman Anselmo Mora Gutierrez
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