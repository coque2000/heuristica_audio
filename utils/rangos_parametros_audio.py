parametros_audio = {
    "low_cut": {
        "inf": 60,
        "sup": 150
    },
    "high_cut": {
        "inf": 6000,
        "sup": 9000
    },
    "filtro_order": {
        "inf": 1,
        "sup": 6
    },
    "prop_decrease": {
        "inf": 0.05,
        "sup": 0.5  # 0.25
    }
}


def cumple_rango_low_cut(low_cut: int, rango_inf: int = parametros_audio["low_cut"]["inf"], rango_sup: int = parametros_audio["low_cut"]["sup"]):
    return rango_inf <= low_cut <= rango_sup

def cumple_rango_high_cut(high_cut: int, rango_inf: int = parametros_audio["high_cut"]["inf"], rango_sup: int = parametros_audio["high_cut"]["sup"]):
    return rango_inf <= high_cut <= rango_sup

def cumple_rango_filtro_order(filtro_order: int, rango_inf: int = parametros_audio["filtro_order"]["inf"], rango_sup: int = parametros_audio["filtro_order"]["sup"]):
    return rango_inf <= filtro_order <= rango_sup

def cumple_rango_prop_de_noise(prop_de_noise: float, rango_inf: float = parametros_audio["prop_decrease"]["inf"], rango_sup: float = parametros_audio["prop_decrease"]["sup"]):
    return rango_inf <= prop_de_noise <= rango_sup


if __name__ == '__main__':
    print(cumple_rango_low_cut(50))
    print(cumple_rango_filtro_order(5))
    print(cumple_rango_low_cut(189))
    print(cumple_rango_low_cut(60))