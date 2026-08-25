def divisiones_sucesivas(n):
    if n <= 0:
        return None

    contador = 0

    while n > 1:
        n = n // 2
        contador += 1

    return contador


# Prueba
print("Cantidad de divisiones:", divisiones_sucesivas(32))