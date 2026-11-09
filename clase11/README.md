# Benchmark de algoritmos de ordenamiento

Comparación de **Selección, Inserción, Burbuja, Quicksort y Heapsort** sobre *los mismos datos*, en cuatro órdenes iniciales, relacionando los tiempos medidos con la complejidad teórica.

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `benchmark_sorting.py` | Implementación de los 5 algoritmos y del benchmark |
| `salida_benchmark.txt` | Salida completa de la ejecución (todas las tablas) |
| `resultados.csv` | Tiempos crudos (parte A y parte B) |
| `resultados.png` | Gráfico log-log de tiempo vs. n |
| `requirements.txt` | Dependencia opcional (`matplotlib`, solo para el gráfico) |

## Cómo ejecutarlo

```bash
python benchmark_sorting.py            # completo (~1–2 min)
python benchmark_sorting.py --quick    # prueba rápida (~5 s)
python benchmark_sorting.py --sizes 500 1000 2000 --reps 5 --out .
```

Solo usa la biblioteca estándar; `matplotlib` es opcional.

## Metodología

- **Mismos datos:** para cada (orden inicial, n) se genera *una* lista base con semilla fija (`12345`) y cada algoritmo recibe una copia idéntica.
- **Órdenes iniciales:** aleatorio, ya ordenado, inverso y casi ordenado (≈5 % de pares intercambiados al azar).
- **Tamaños:** n = 500, 1000, 2000, 4000, 8000 (se duplica en cada paso). Parte B: Quicksort y Heapsort hasta n = 400 000.
- **Medición:** `time.perf_counter()`, recolector de basura desactivado durante la medición, copia de la lista fuera del cronómetro y **mínimo** de varias repeticiones (el ruido del sistema solo puede aumentar el tiempo). Las ejecuciones rápidas se repiten hasta acumular ~0,25 s (hasta 200 veces) para reducir el ruido.
- **Verificación:** cada resultado se compara con `sorted()`.
- **Variantes usadas:** Burbuja con bandera de parada temprana; Quicksort in-place con pivote aleatorio (partición de Lomuto) que recurre solo sobre la mitad menor; Heapsort con max-heap implícito.

### Complejidad teórica

| Algoritmo | Mejor | Promedio | Peor |
|---|---|---|---|
| Selección | O(n²) | O(n²) | O(n²) |
| Inserción | O(n) | O(n²) | O(n²) |
| Burbuja (con bandera) | O(n) | O(n²) | O(n²) |
| Quicksort (pivote aleatorio) | O(n log n) | O(n log n) | O(n²) (muy improbable) |
| Heapsort | O(n log n) | O(n log n) | O(n log n) |

## Resultados (n = 8000, tiempos en ms)

| Algoritmo | Aleatorio | Ordenado | Inverso | Casi ordenado |
|---|---:|---:|---:|---:|
| Selección | 924 | 967 | 1 194 | 841 |
| Inserción | 880 | **0,50** | 1 916 | 194 |
| Burbuja | **2 380** | **0,29** | **2 803** | **1 391** |
| Quicksort | **9,6** | 8,5 | **8,8** | **8,4** |
| Heapsort | 17,5 | 12,7 | 13,4 | 12,6 |

Negrita = más rápido o más lento de la columna. Las tablas completas para todos los n están en `salida_benchmark.txt`; el gráfico está en `resultados.png`.

![Gráfico](resultados.png)

---

# Análisis

## 1. Más rápido y más lento por orden inicial

| Orden inicial | Más rápido (n = 8000) | Más lento (n = 8000) |
|---|---|---|
| Aleatorio | Quicksort (9,6 ms) | Burbuja (2 380 ms, ≈ 250×) |
| Ordenado | Burbuja (0,29 ms) | Selección (967 ms, ≈ 3 300×) |
| Inverso | Quicksort (8,8 ms) | Burbuja (2 803 ms, ≈ 320×) |
| Casi ordenado | Quicksort (8,4 ms) | Burbuja (1 391 ms, ≈ 165×) |

**Aleatorio.** Quicksort gana porque es O(n log n) frente al O(n²) de los otros tres (con n = 8000, n² / (n·log₂n) ≈ 600 operaciones de diferencia en teoría; se midió ≈ 90×–250× según el rival, porque las constantes también cuentan). Entre los cuadráticos, Burbuja es el peor porque hace ≈ n²/2 comparaciones y ≈ n²/4 intercambios (cada uno con dos lecturas y dos escrituras). Inserción y Selección empatan (~900 ms) por razones opuestas: Inserción hace la mitad de comparaciones pero desplaza elementos; Selección hace el doble de comparaciones pero casi no mueve datos (a lo sumo n intercambios).

**Ordenado.** Aquí ganan los algoritmos *adaptativos*. Burbuja con bandera hace una sola pasada de n − 1 comparaciones sin intercambios y se detiene; Inserción también hace n − 1 comparaciones sin desplazamientos, pero con algo más de trabajo por elemento (~1,7× más lenta). El más lento es Selección porque **no es adaptativo**: siempre hace n(n − 1)/2 comparaciones, esté o no ordenado el arreglo. Quicksort y Heapsort (8,5 y 12,7 ms) no aprovechan el orden previo, pero siguen siendo ≈ 75–115× más rápidos que Selección. Ganar en datos ordenados no hace a Burbuja un buen algoritmo general: solo aprovecha un caso muy particular.

**Inverso.** Es el peor caso de Inserción y Burbuja: hay n(n − 1)/2 inversiones, así que Inserción hace ≈ n²/2 desplazamientos (≈ 2× el caso aleatorio) y Burbuja ≈ n²/2 intercambios (el doble que en el caso aleatorio). Burbuja es la más lenta por tener que hacer, además, todas las comparaciones. Selección sube un ~30 % respecto al caso aleatorio (probablemente porque la condición `a[j] < a[m]` se cumple casi siempre y se hacen más asignaciones). Quicksort sigue en ≈ 9 ms gracias al pivote aleatorio: un pivote fijo (primero/último) degeneraría a O(n²) en este caso.

**Casi ordenado.** Con n = 8000 vuelve a ganar Quicksort. Inserción es adaptativa (su costo es ≈ n + número de inversiones), y por eso tarda 194 ms frente a 880 ms en el caso aleatorio, pero el 5 % de intercambios entre posiciones lejanas aún deja millones de inversiones, así que no alcanza a Quicksort. Con n = 500 la situación se invierte levemente: Inserción (0,33 ms) empata con Quicksort (0,35 ms), el clásico motivo por el que algoritmos híbridos (Timsort, introsort) usan Inserción para subarreglos pequeños. Burbuja sigue siendo la peor: los elementos pequeños lejos de su sitio ("tortugas") avanzan solo una posición por pasada, así que la bandera de parada temprana casi no ayuda.

## 2. ¿Al duplicar n el tiempo se multiplica por ~4 (cuadráticos) y por algo más de 2 (Quicksort/Heapsort)?

Razón media t(2n)/t(n) sobre las cuatro duplicaciones (500→1000 … 4000→8000). Teórico: **4** para cuadráticos y **≈ 2,19** para n log n (en estos tamaños, 2·log₂(2n)/log₂(n)).

| Orden inicial | Selección | Inserción | Burbuja | Quicksort | Heapsort |
|---|---:|---:|---:|---:|---:|
| Aleatorio | 4,14 | 4,26 | 4,42 | 2,25 | 2,49 |
| Ordenado | 4,28 | **2,09** | **2,11** | 2,23 | 2,28 |
| Inverso | 4,39 | 4,39 | 4,36 | 2,23 | 2,52 |
| Casi ordenado | 4,27 | 5,00 | 4,45 | 2,22 | 2,28 |

La pendiente de la recta log(t) vs log(n) lleva a la misma conclusión: ≈ 2,0–2,3 para los cuadráticos, ≈ 1,06 para Inserción y Burbuja en datos ordenados, 1,14–1,16 para Quicksort y 1,18–1,33 para Heapsort (un n log n puro daría ≈ 1,1).

**Conclusiones:**

- **Cuadráticos: sí se cumple.** Cuando se encuentran en su caso promedio o peor, el tiempo se multiplica por ≈ 4,1–4,5. Lo hacen **siempre** en Selección (también con datos ordenados, porque no es adaptativa).
- **Excepción esperada:** Inserción y Burbuja con datos ordenados se multiplican por ≈ 2,1, porque ahí corren en su mejor caso O(n), es decir, lineal. La regla "×4" depende del caso, no solo del algoritmo.
- **En "casi ordenado"** el costo de Inserción crece algo más de ×4 (media 5,0, pendiente 2,28). El número de inversiones de ese conjunto sigue creciendo como n² (el 5 % de n intercambios entre posiciones lejanas), y además cada tamaño usa su propio sorteo de intercambios, lo que añade variabilidad.
- **Quicksort y Heapsort: sí, algo más de ×2.** Quicksort da 2,22–2,25 en los cuatro escenarios (teórico 2,19), muy estable. Heapsort da 2,28–2,52, ligeramente por encima, con algún valor atípico (p. ej. 3,74 en inverso 2000→4000, seguido de 1,56, lo que indica que el tiempo de n = 4000 salió inflado por ruido). En la **parte B**, con n hasta 400 000 y aleatorio, Quicksort da 2,15 / 2,43 / 2,27 / 2,34 por duplicación (teórico ≈ 2,12). Heapsort da 2,17 / 2,42 / 3,20 / 2,02, de modo que la tendencia se cumple aunque el 3,20 es un outlier.
- **Por qué "algo más de 2" y no exactamente 2:** si T(n) = c·n·log₂n, entonces T(2n)/T(n) = 2·(1 + 1/log₂n), que para n entre 500 y 8000 vale ≈ 2,15–2,22 y se acerca a 2 al crecer n.

> **Nota sobre el ruido.** Las mediciones se hicieron en un contenedor compartido de un solo núcleo, así que hay celdas con ruido de varios por ciento o más (por ejemplo, Selección en "casi ordenado" con n = 4000 y Heapsort con n = 8000 aleatorio). Por eso conviene mirar las **medias y pendientes** y no una celda aislada. Al ejecutarlo en tu equipo los números absolutos cambiarán, pero la forma de los resultados no.

## 3. ¿Por qué Quicksort suele superar a Heapsort si ambos son O(n log n)?

Con la misma complejidad asintótica, lo que difiere son las **constantes ocultas**. En este benchmark Heapsort fue entre ~1,2× y ~1,8× más lento (típicamente ≈ 1,4–1,5×), y en la parte B esa proporción se mantuvo o creció con n. Las razones:

1. **Menos comparaciones y movimientos.** Quicksort hace en promedio ≈ 1,39·n·log₂n comparaciones. Heapsort hace ≈ 2·n·log₂n: en cada nivel del `sift_down` compara los dos hijos entre sí y luego el mayor con el padre. Además, al extraer la raíz se coloca en ella el último elemento del heap (que es "pequeño"), y casi siempre debe bajar hasta el fondo, así que no hay salidas tempranas.
2. **Localidad de memoria (caché).** La partición de Quicksort recorre el arreglo de forma secuencial, que es lo que mejor aprovechan la caché y el prefetching. Heapsort salta de `i` a `2i+1`/`2i+2`, accediendo a posiciones cada vez más alejadas, con muchos más fallos de caché cuando el arreglo no cabe en caché. En Python el efecto se atenúa (la lista guarda punteros y el intérprete domina el tiempo), pero con n grande se nota que la brecha crece. En lenguajes compilados la diferencia suele ser mayor.
3. **Bucle interno más simple.** El recorrido de partición es un bucle corto y predecible; `sift_down` tiene más aritmética de índices y ramas más difíciles de predecir.

**Qué ofrece Heapsort a cambio:** garantiza O(n log n) en el peor caso con O(1) de memoria extra, mientras que Quicksort puede degradarse a O(n²) con malos pivotes (aquí se evita con pivote aleatorio). Por eso las implementaciones reales combinan ambos: **introsort** (usado en C++ `std::sort`) comienza con Quicksort y cambia a Heapsort si la recursión se hace demasiado profunda. Ninguno de los dos es estable.

## Conclusiones generales

- La complejidad teórica predice bien el comportamiento: pendientes ≈ 2 (cuadráticos), ≈ 1,1–1,3 (n log n) y ≈ 1 (algoritmos adaptativos en su mejor caso).
- Para datos generales y grandes, Quicksort (con pivote aleatorio) fue el más rápido en todos los escenarios con n = 8000, salvo en datos ya ordenados, donde Burbuja e Inserción lo superan.
- Inserción es excelente con datos casi ordenados o pequeños; Selección es la única de las tres cuadráticas que no se beneficia nunca del orden previo.
- Heapsort es la opción cuando se necesita garantía de peor caso con memoria constante; Quicksort cuando prima la velocidad en la práctica.

## Limitaciones

- Todo está en Python puro, por lo que el costo del intérprete domina; en C/C++/Java las proporciones (sobre todo Quicksort vs Heapsort) pueden diferir.
- n máximo de 8000 en la parte A por el costo de los algoritmos cuadráticos.
- Los resultados dependen del hardware y del ruido del sistema en el momento de la ejecución.
