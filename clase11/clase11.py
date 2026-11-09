#!/usr/bin/env python3
"""
Benchmark de algoritmos de ordenamiento
=======================================
Compara Selección, Inserción, Burbuja, Quicksort y Heapsort sobre LOS MISMOS
datos (cada algoritmo recibe una copia idéntica de la misma lista base) en
cuatro órdenes iniciales distintos, y relaciona los tiempos con la complejidad
teórica.

Uso:
    python benchmark_sorting.py                 # benchmark completo
    python benchmark_sorting.py --quick         # versión rápida (n pequeños)
    python benchmark_sorting.py --sizes 500 1000 2000 --reps 5
"""
import argparse
import csv
import gc
import math
import random
import sys
import time

SEMILLA = 12345


# =============================================================================
# 1. ALGORITMOS (todos ordenan IN-PLACE la lista recibida y la devuelven)
# =============================================================================
def seleccion(a):
    """Selección: busca el mínimo del resto y lo coloca en su sitio. Θ(n²)."""
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        if m != i:
            a[i], a[m] = a[m], a[i]
    return a


def insercion(a):
    """Inserción: inserta cada elemento en la parte ya ordenada. O(n²), mejor O(n)."""
    for i in range(1, len(a)):
        clave = a[i]
        j = i - 1
        while j >= 0 and a[j] > clave:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = clave
    return a


def burbuja(a):
    """Burbuja con bandera de parada temprana. O(n²), mejor caso O(n)."""
    n = len(a)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return a


def quicksort(a):
    """Quicksort in-place, pivote aleatorio (partición de Lomuto).
    Se recurre sobre la mitad menor y se itera sobre la mayor, así la
    profundidad de pila es O(log n) incluso en casos desfavorables."""

    def _qs(lo, hi):
        while lo < hi:
            p = random.randint(lo, hi)
            a[p], a[hi] = a[hi], a[p]
            pivote = a[hi]
            i = lo
            for j in range(lo, hi):
                if a[j] < pivote:
                    a[i], a[j] = a[j], a[i]
                    i += 1
            a[i], a[hi] = a[hi], a[i]
            if i - lo < hi - i:
                _qs(lo, i - 1)
                lo = i + 1
            else:
                _qs(i + 1, hi)
                hi = i - 1

    _qs(0, len(a) - 1)
    return a


def heapsort(a):
    """Heapsort con max-heap implícito en el arreglo. Θ(n log n) siempre."""
    n = len(a)

    def sift_down(i, fin):
        while True:
            izq = 2 * i + 1
            if izq >= fin:
                return
            der = izq + 1
            mayor = der if (der < fin and a[der] > a[izq]) else izq
            if a[mayor] > a[i]:
                a[i], a[mayor] = a[mayor], a[i]
                i = mayor
            else:
                return

    for i in range(n // 2 - 1, -1, -1):      # construir el heap: O(n)
        sift_down(i, n)
    for fin in range(n - 1, 0, -1):          # extraer el máximo n veces
        a[0], a[fin] = a[fin], a[0]
        sift_down(0, fin)
    return a


ALGORITMOS = {
    "Selección": seleccion,
    "Inserción": insercion,
    "Burbuja": burbuja,
    "Quicksort": quicksort,
    "Heapsort": heapsort,
}
CUADRATICOS = ("Selección", "Inserción", "Burbuja")
NLOGN = ("Quicksort", "Heapsort")

TEORIA = {
    #               mejor        promedio      peor
    "Selección": ("O(n²)",     "O(n²)",      "O(n²)"),
    "Inserción": ("O(n)",      "O(n²)",      "O(n²)"),
    "Burbuja":   ("O(n)*",     "O(n²)",      "O(n²)"),
    "Quicksort": ("O(n log n)", "O(n log n)", "O(n²)**"),
    "Heapsort":  ("O(n log n)", "O(n log n)", "O(n log n)"),
}


# =============================================================================
# 2. GENERACIÓN DE DATOS (órdenes iniciales)
# =============================================================================
def generar(escenario, n, rng):
    if escenario == "Aleatorio":
        return rng.sample(range(n * 10), n)
    if escenario == "Ordenado":
        return list(range(n))
    if escenario == "Inverso":
        return list(range(n, 0, -1))
    if escenario == "Casi ordenado":
        a = list(range(n))
        for _ in range(max(1, n // 20)):          # ~5 % de pares intercambiados
            i, j = rng.randrange(n), rng.randrange(n)
            a[i], a[j] = a[j], a[i]
        return a
    raise ValueError(escenario)


ESCENARIOS = ["Aleatorio", "Ordenado", "Inverso", "Casi ordenado"]


# =============================================================================
# 3. MEDICIÓN
# =============================================================================
def medir(func, base, reps, presupuesto=0.25, max_reps=200):
    """Mejor tiempo (mínimo) de varias ejecuciones sobre copias de `base`, en ms.

    - El mínimo es la medida estándar en microbenchmarks: el ruido del sistema
      solo puede AUMENTAR el tiempo, nunca reducirlo.
    - Si una ejecución es muy rápida (unos ms), el ruido pesa mucho; por eso se
      repite hasta acumular ~`presupuesto` segundos (entre `reps` y `max_reps`)."""
    esperado = sorted(base)
    mejor = float("inf")
    gc_estaba = gc.isenabled()
    gc.disable()
    try:
        i, objetivo = 0, reps
        while i < objetivo:
            copia = base[:]                       # copia fuera del cronómetro
            t0 = time.perf_counter()
            resultado = func(copia)
            dt = time.perf_counter() - t0
            assert resultado == esperado, f"{func.__name__} ordenó mal"
            mejor = min(mejor, dt)
            i += 1
            if i == 1:
                objetivo = max(reps, min(max_reps, int(presupuesto / max(dt, 1e-9))))
    finally:
        if gc_estaba:
            gc.enable()
    return mejor * 1000.0


def pendiente_loglog(ns, ts):
    """Pendiente de la recta log(t) = k·log(n) + c (mínimos cuadrados).
    k ≈ 2 → cuadrático; k ≈ 1.0–1.2 → n log n; k ≈ 1 → lineal."""
    xs = [math.log(n) for n in ns]
    ys = [math.log(t) for t in ts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    return num / den


def correr(sizes, reps, extra_sizes):
    rng = random.Random(SEMILLA)
    random.seed(SEMILLA)                         # pivotes de Quicksort reproducibles
    res = {}                                     # (escenario, algoritmo, n) -> ms
    total = len(ESCENARIOS) * len(sizes)
    k = 0
    for esc in ESCENARIOS:
        for n in sizes:
            k += 1
            base = generar(esc, n, rng)
            print(f"  [{k:>2}/{total}] {esc:<14} n={n:<6}", end="", flush=True)
            t_ini = time.perf_counter()
            for nombre, f in ALGORITMOS.items():
                res[(esc, nombre, n)] = medir(f, base, reps)
            print(f" ({time.perf_counter() - t_ini:.1f} s)")

    res_extra = {}
    if extra_sizes:
        print("\n  Parte B: O(n log n) con n grandes (datos aleatorios)")
        for n in extra_sizes:
            base = generar("Aleatorio", n, rng)
            print(f"    n={n:<8}", end="", flush=True)
            for nombre in NLOGN:
                res_extra[(nombre, n)] = medir(ALGORITMOS[nombre], base, max(1, reps - 1))
            print(" ok")
    return res, res_extra


# =============================================================================
# 4. REPORTES
# =============================================================================
def linea(c="-", n=92):
    print(c * n)


def reporte_teoria():
    print("\nCOMPLEJIDAD TEÓRICA")
    linea()
    print(f"{'Algoritmo':<12}{'Mejor':<14}{'Promedio':<14}{'Peor':<14}")
    linea()
    for nombre, (m, p, w) in TEORIA.items():
        print(f"{nombre:<12}{m:<14}{p:<14}{w:<14}")
    print("* con bandera de parada temprana   ** evitado con pivote aleatorio (esperado n log n)")


def reporte_tiempos(res, sizes):
    print("\n\nTIEMPOS (ms, mejor de varias repeticiones)")
    for esc in ESCENARIOS:
        print(f"\n▸ Orden inicial: {esc}")
        linea()
        print(f"{'Algoritmo':<12}" + "".join(f"{'n=' + str(n):>13}" for n in sizes))
        linea()
        for nombre in ALGORITMOS:
            print(f"{nombre:<12}" + "".join(f"{res[(esc, nombre, n)]:>13.3f}" for n in sizes))


def reporte_ganadores(res, sizes):
    print("\n\n1) MÁS RÁPIDO Y MÁS LENTO POR ORDEN INICIAL")
    linea()
    print(f"{'Orden inicial':<15}{'n':>7}   {'Más rápido':<22}{'Más lento':<22}{'Factor':>10}")
    linea()
    for esc in ESCENARIOS:
        for n in (sizes[0], sizes[-1]):
            t = {a: res[(esc, a, n)] for a in ALGORITMOS}
            rap = min(t, key=t.get)
            len_ = max(t, key=t.get)
            print(f"{esc:<15}{n:>7}   {rap + f' ({t[rap]:.2f} ms)':<22}"
                  f"{len_ + f' ({t[len_]:.0f} ms)':<22}{t[len_] / t[rap]:>9.0f}x")
        linea("·")


def reporte_duplicacion(res, sizes):
    print("\n\n2) EFECTO DE DUPLICAR n:  t(2n) / t(n)")
    print("   Esperado: cuadrático → 4,  n log n → 2·log₂(2n)/log₂(n) (algo más de 2)")
    pares = list(zip(sizes, sizes[1:]))
    for esc in ESCENARIOS:
        print(f"\n▸ Orden inicial: {esc}")
        linea()
        enc = f"{'Algoritmo':<12}" + "".join(f"{str(a) + '→' + str(b):>11}" for a, b in pares)
        print(enc + f"{'Media':>9}{'Teórico':>9}{'Pend.':>8}")
        linea()
        for nombre in ALGORITMOS:
            ratios = [res[(esc, nombre, b)] / res[(esc, nombre, a)] for a, b in pares]
            if nombre in CUADRATICOS:
                teor = 4.0
            else:
                teor = sum(2 * math.log2(b) / math.log2(a) for a, b in pares) / len(pares)
            pend = pendiente_loglog(sizes, [res[(esc, nombre, n)] for n in sizes])
            print(f"{nombre:<12}" + "".join(f"{r:>11.2f}" for r in ratios)
                  + f"{sum(ratios) / len(ratios):>9.2f}{teor:>9.2f}{pend:>8.2f}")
    print("\n   Pend. = pendiente de log(t) vs log(n): ≈2 cuadrático, ≈1.1 n log n, ≈1 lineal.")


def reporte_extra(res_extra, extra_sizes):
    if not res_extra:
        return
    print("\n\n   PARTE B – Quicksort vs Heapsort con n grandes (aleatorio)")
    linea()
    print(f"{'n':>9}{'Quicksort ms':>15}{'Heapsort ms':>14}{'Heap/Quick':>13}"
          f"{'Quick x2n':>12}{'Heap x2n':>11}{'Teórico':>10}")
    linea()
    previo = None
    for n in extra_sizes:
        q, h = res_extra[("Quicksort", n)], res_extra[("Heapsort", n)]
        if previo:
            pn, pq, ph = previo
            rq, rh, teor = f"{q / pq:.2f}", f"{h / ph:.2f}", f"{2 * math.log2(n) / math.log2(pn):.2f}"
        else:
            rq = rh = teor = "-"
        print(f"{n:>9}{q:>15.1f}{h:>14.1f}{h / q:>12.2f}x{rq:>12}{rh:>11}{teor:>10}")
        previo = (n, q, h)


def guardar_csv(res, res_extra, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["parte", "orden_inicial", "algoritmo", "n", "tiempo_ms"])
        for (esc, alg, n), t in sorted(res.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
            w.writerow(["A", esc, alg, n, f"{t:.4f}"])
        for (alg, n), t in sorted(res_extra.items()):
            w.writerow(["B", "Aleatorio", alg, n, f"{t:.4f}"])
    print(f"\nCSV guardado en: {ruta}")


def graficar(res, sizes, ruta):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib no está instalado: se omite el gráfico.")
        return
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    estilos = {"Selección": "o-", "Inserción": "s-", "Burbuja": "^-",
               "Quicksort": "D-", "Heapsort": "v-"}
    for ax, esc in zip(axes.flat, ESCENARIOS):
        for nombre in ALGORITMOS:
            ax.plot(sizes, [res[(esc, nombre, n)] for n in sizes], estilos[nombre], label=nombre)
        ax.set_xscale("log", base=2)
        ax.set_yscale("log")
        ax.set_title(f"Orden inicial: {esc}")
        ax.set_xlabel("n")
        ax.set_ylabel("tiempo (ms)")
        ax.grid(True, which="both", alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Benchmark de ordenamiento (escala log-log)")
    fig.tight_layout()
    fig.savefig(ruta, dpi=130)
    print(f"Gráfico guardado en: {ruta}")


# =============================================================================
# 5. MAIN
# =============================================================================
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    ap.add_argument("--sizes", type=int, nargs="+", default=[500, 1000, 2000, 4000, 8000])
    ap.add_argument("--extra", type=int, nargs="*", default=[25000, 50000, 100000, 200000, 400000],
                    help="tamaños grandes solo para Quicksort/Heapsort (vacío para omitir)")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--quick", action="store_true", help="n pequeños, para probar rápido")
    ap.add_argument("--out", default=".", help="carpeta de salida (CSV y PNG)")
    args = ap.parse_args()
    if args.quick:
        args.sizes, args.extra, args.reps = [250, 500, 1000, 2000], [10000, 20000, 40000], 2

    sizes = sorted(args.sizes)
    print(f"Python {sys.version.split()[0]} | semilla={SEMILLA} | repeticiones={args.reps} | n={sizes}")
    reporte_teoria()
    print("\n\nEJECUTANDO MEDICIONES...")
    res, res_extra = correr(sizes, args.reps, sorted(args.extra))

    reporte_tiempos(res, sizes)
    reporte_ganadores(res, sizes)
    reporte_duplicacion(res, sizes)
    reporte_extra(res_extra, sorted(args.extra))

    guardar_csv(res, res_extra, f"{args.out}/resultados.csv")
    graficar(res, sizes, f"{args.out}/resultados.png")


if __name__ == "__main__":
    main()
