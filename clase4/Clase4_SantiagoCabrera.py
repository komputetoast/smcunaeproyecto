"""
Resolución de ecuaciones de recurrencia
y ejemplo del paradigma Divide y Vencerás.

Las recurrencias se analizan usando el Teorema Maestro
cuando es aplicable y sustitución/árbol de recurrencia
cuando corresponde.
"""

from math import log2


def resolver_recurrencias():
    """
    Muestra el resultado de complejidad temporal de cada recurrencia.
    """

    recurrencias = {
        1: "T(n) = 2T(n/2) + O(n)",
        2: "T(n) = 4T(n/2) + O(n)",
        3: "T(n) = 2T(n/2) + O(n^2)",
        4: "T(n) = T(n-1) + O(n)",
        5: "T(n) = T(n/3) + T(2n/3) + O(n)",
        6: "T(n) = 3T(n/4) + O(n^2)",
    }

    resultados = {
        1: "O(n log n)",
        2: "O(n^2)",
        3: "O(n^2)",
        4: "O(n^2)",
        5: "O(n log n)",
        6: "O(n^2)",
    }

    print("=" * 65)
    print("ECUACIONES DE RECURRENCIA")
    print("=" * 65)

    for numero in recurrencias:
        print(f"\nEcuación {numero}:")
        print(f"  {recurrencias[numero]}")
        print(f"  Complejidad: {resultados[numero]}")

    print("\n" + "=" * 65)


def merge_sort(lista):
    """
    Implementación de Merge Sort.

    Divide la lista en dos partes, ordena recursivamente
    cada parte y finalmente combina los resultados.

    Complejidad temporal:
        O(n log n)

    Complejidad espacial:
        O(n)
    """

    # Caso base: una lista de 0 o 1 elementos ya está ordenada.
    if len(lista) <= 1:
        return lista

    # DIVIDIR
    mitad = len(lista) // 2

    izquierda = lista[:mitad]
    derecha = lista[mitad:]

    # VENCER: resolver recursivamente cada mitad.
    izquierda = merge_sort(izquierda)
    derecha = merge_sort(derecha)

    # COMBINAR
    return merge(izquierda, derecha)


def merge(izquierda, derecha):
    """
    Combina dos listas ordenadas en una única lista ordenada.
    """

    resultado = []

    i = 0
    j = 0

    while i < len(izquierda) and j < len(derecha):

        if izquierda[i] <= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    # Agregar elementos restantes.
    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


def demostrar_merge_sort():
    """
    Demuestra el funcionamiento de Merge Sort.
    """

    lista = [38, 27, 43, 3, 9, 82, 10]

    print("\n" + "=" * 65)
    print("ALGORITMO DIVIDE Y VENCERÁS: MERGE SORT")
    print("=" * 65)

    print(f"\nLista original: {lista}")

    resultado = merge_sort(lista)

    print(f"Lista ordenada:  {resultado}")

    print("\nRecurrencia de Merge Sort:")
    print("T(n) = 2T(n/2) + O(n)")
    print("Complejidad: O(n log n)")


if __name__ == "__main__":
    resolver_recurrencias()
    demostrar_merge_sort()
