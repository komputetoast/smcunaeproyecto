def iteracion_con_saltos(n):
    contador = 0

    for i in range(n + 1):
        j = 1

        while j < n:
            contador += 1
            j *= 2

    return contador


# Prueba
print("Cantidad de iteraciones:", iteracion_con_saltos(16))