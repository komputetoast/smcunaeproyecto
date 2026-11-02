"""Comparación de Merge Sort vs Quick Sort."""
import random
import sys
import time

sys.setrecursionlimit(10000)


# ---------------- MERGE SORT (estable, O(n log n) siempre) ----------------
def merge_sort(arr, key=lambda x: x, cont=None):
    cont = cont if cont is not None else [0]
    if len(arr) <= 1:
        return arr[:]
    medio = len(arr) // 2
    izq = merge_sort(arr[:medio], key, cont)
    der = merge_sort(arr[medio:], key, cont)

    resultado, i, j = [], 0, 0
    while i < len(izq) and j < len(der):
        cont[0] += 1
        if key(izq[i]) <= key(der[j]):      # <= mantiene la estabilidad
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado


# ---------------- QUICK SORT (in-place, no estable) ----------------
def quick_sort(arr, key=lambda x: x, cont=None):
    cont = cont if cont is not None else [0]
    a = arr[:]

    def particionar(bajo, alto):
        # pivote aleatorio para evitar el peor caso en datos ya ordenados
        p = random.randint(bajo, alto)
        a[p], a[alto] = a[alto], a[p]
        pivote = key(a[alto])
        i = bajo
        for j in range(bajo, alto):
            cont[0] += 1
            if key(a[j]) < pivote:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[alto] = a[alto], a[i]
        return i

    # pila explícita: evita desbordar la recursión
    pila = [(0, len(a) - 1)]
    while pila:
        bajo, alto = pila.pop()
        if bajo < alto:
            p = particionar(bajo, alto)
            pila.append((bajo, p - 1))
            pila.append((p + 1, alto))
    return a


# ---------------- PRUEBAS ----------------
def medir(func, datos):
    cont = [0]
    t0 = time.perf_counter()
    res = func(datos, cont=cont)
    t = (time.perf_counter() - t0) * 1000
    return res, cont[0], t


if __name__ == "__main__":
    random.seed(42)

    print("=" * 60)
    print("1) CORRECTITUD (lista pequeña)")
    print("=" * 60)
    pequena = [38, 27, 43, 3, 9, 82, 10]
    print("Original   :", pequena)
    print("Merge Sort :", merge_sort(pequena))
    print("Quick Sort :", quick_sort(pequena))

    print("\n" + "=" * 60)
    print("2) COMPARACIÓN DE RENDIMIENTO (n = 5000)")
    print("=" * 60)
    n = 5000
    escenarios = {
        "Aleatorio":        random.sample(range(n * 10), n),
        "Ya ordenado":      list(range(n)),
        "Orden inverso":    list(range(n, 0, -1)),
        "Muchos repetidos": [random.randint(0, 10) for _ in range(n)],
    }
    print(f"{'Escenario':<18}{'Algoritmo':<12}{'Comparaciones':>15}{'Tiempo (ms)':>14}")
    print("-" * 59)
    for nombre, datos in escenarios.items():
        for alg, f in (("Merge Sort", merge_sort), ("Quick Sort", quick_sort)):
            res, comps, t = medir(f, datos)
            assert res == sorted(datos)
            print(f"{nombre:<18}{alg:<12}{comps:>15,}{t:>14.2f}")
        print("-" * 59)

    print("\n" + "=" * 60)
    print("3) PRUEBA DE ESTABILIDAD")
    print("=" * 60)
    # (nombre, edad): ordenamos por edad; Ana y Luis tienen 20, Ana va primero
    personas = [("Ana", 20), ("Bruno", 18), ("Luis", 20), ("Carla", 18), ("Diego", 20)]
    por_edad = lambda p: p[1]
    print("Original   :", personas)
    print("Merge Sort :", merge_sort(personas, key=por_edad))
    random.seed(1)
    print("Quick Sort :", quick_sort(personas, key=por_edad))
    print("(Si el orden relativo de Ana, Luis, Diego se mantiene => estable)")
