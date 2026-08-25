def busqueda_binaria(lista, objetivo):
    inicio = 0
    fin = len(lista) - 1

    while inicio <= fin:
        medio = (inicio + fin) // 2

        if lista[medio] == objetivo:
            return medio

        elif lista[medio] < objetivo:
            inicio = medio + 1

        else:
            fin = medio - 1

    return -1


# Prueba
numeros = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("Posición:", busqueda_binaria(numeros, 23))