def ultimo_elemento(arreglo):
    if len(arreglo) == 0:
        return None

    return arreglo[-1]


# Prueba
numeros = [10, 20, 30, 40, 50]
print("Último elemento:", ultimo_elemento(numeros))