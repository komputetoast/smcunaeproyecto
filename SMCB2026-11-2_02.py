"""Búsqueda lineal y binaria, con traza paso a paso."""


def busqueda_lineal(arr, objetivo, verbose=True):
    """Recorre el arreglo elemento por elemento. O(n)."""
    for i, valor in enumerate(arr):
        if verbose:
            print(f"  Paso {i + 1}: arr[{i}] = {valor}  ->  ¿{valor} == {objetivo}? ", end="")
        if valor == objetivo:
            if verbose:
                print("SÍ, encontrado")
            return i
        if verbose:
            print("no")
    return -1


def busqueda_binaria(arr, objetivo, verbose=True):
    """Divide el rango a la mitad en cada paso (requiere arreglo ordenado). O(log n)."""
    bajo, alto = 0, len(arr) - 1
    paso = 1
    while bajo <= alto:
        medio = (bajo + alto) // 2
        if verbose:
            print(f"  Paso {paso}: bajo={bajo}, alto={alto}, medio=({bajo}+{alto})//2={medio}, arr[{medio}]={arr[medio]}")
        if arr[medio] == objetivo:
            if verbose:
                print(f"           {arr[medio]} == {objetivo}  ->  encontrado")
            return medio
        elif arr[medio] < objetivo:
            if verbose:
                print(f"           {arr[medio]} < {objetivo}  ->  descartar izquierda, bajo = {medio + 1}")
            bajo = medio + 1
        else:
            if verbose:
                print(f"           {arr[medio]} > {objetivo}  ->  descartar derecha, alto = {medio - 1}")
            alto = medio - 1
        paso += 1
    return -1


if __name__ == "__main__":
    arreglo = [1, 3, 4, 6, 12, 15, 35, 44]
    objetivo = 12
    print("Arreglo :", arreglo)
    print("Objetivo:", objetivo)

    print("\n=== BÚSQUEDA LINEAL ===")
    pos = busqueda_lineal(arreglo, objetivo)
    print(f"Resultado: índice {pos}")

    print("\n=== BÚSQUEDA BINARIA ===")
    pos = busqueda_binaria(arreglo, objetivo)
    print(f"Resultado: índice {pos}")

    print("\n=== Caso no encontrado (objetivo = 10, búsqueda binaria) ===")
    pos = busqueda_binaria(arreglo, 10)
    print(f"Resultado: {pos} (no existe)")
