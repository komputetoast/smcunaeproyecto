def procesar_listas(lista_n, lista_m):
    suma = 0

    # Recorrer la primera lista
    for elemento in lista_n:
        suma += elemento

    producto = 1

    # Recorrer la segunda lista
    for elemento in lista_m:
        producto *= elemento

    return suma, producto


# Prueba
lista1 = [1, 2, 3, 4, 5]
lista2 = [2, 3, 4]

suma, producto = procesar_listas(lista1, lista2)

print("Suma de la primera lista:", suma)
print("Producto de la segunda lista:", producto)