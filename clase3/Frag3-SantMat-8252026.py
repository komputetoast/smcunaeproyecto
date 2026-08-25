def busqueda_lineal(lista, objetivo):
    for i in range(len(lista)):
        if lista[i] == objetivo:
            return i

    return -1


# Prueba
numeros = [7, 15, 3, 20, 9]
print("Posición:", busqueda_lineal(numeros, 20))