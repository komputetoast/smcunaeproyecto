# Ecuaciones de Recurrencia y Divide y Vencerás

## Descripción

Este proyecto contiene la resolución de seis ecuaciones de recurrencia y la implementación en Python de un algoritmo que utiliza el paradigma **Divide y Vencerás**.

Para las ecuaciones de la consigna donde aparece `O[No]`, se interpreta que corresponde a **O(n)**.

---

# 1. Ecuaciones de Recurrencia

## Ecuación 1

**Recurrencia:**

```text
T(n) = 2T(n/2) + O(n)
```

Aplicando el Teorema Maestro:

- `a = 2`
- `b = 2`
- `f(n) = O(n)`
- `n^(log_b(a)) = n^(log_2(2)) = n`

Como `f(n) = Θ(n)`, corresponde al **Caso 2** del Teorema Maestro.

Por lo tanto:

```text
T(n) = Θ(n log n)
```

**Resultado: O(n log n)**

---

## Ecuación 2

**Recurrencia:**

```text
T(n) = 4T(n/2) + O(n)
```

Tenemos:

- `a = 4`
- `b = 2`
- `f(n) = O(n)`
- `n^(log_2(4)) = n^2`

Como `f(n)` crece más lentamente que `n²`, corresponde al **Caso 1**.

Por lo tanto:

```text
T(n) = Θ(n²)
```

**Resultado: O(n²)**

---

## Ecuación 3

**Recurrencia:**

```text
T(n) = 2T(n/2) + O(n²)
```

Tenemos:

- `a = 2`
- `b = 2`
- `f(n) = O(n²)`
- `n^(log_2(2)) = n`

Como `n²` crece más rápidamente que `n`, corresponde al **Caso 3** del Teorema Maestro.

Por lo tanto:

```text
T(n) = Θ(n²)
```

**Resultado: O(n²)**

---

## Ecuación 4

**Recurrencia:**

```text
T(n) = T(n-1) + O(n)
```

El Teorema Maestro no se aplica directamente porque el problema se reduce de `n` a `n-1`.

Desarrollando la recurrencia:

```text
T(n) = T(n-1) + n
T(n-1) = T(n-2) + (n-1)
```

Continuando:

```text
T(n) = T(1) + 2 + 3 + ... + n
```

La suma de los primeros `n` números es:

```text
n(n+1)/2
```

Por lo tanto:

```text
T(n) = Θ(n²)
```

**Resultado: O(n²)**

---

## Ecuación 5

**Recurrencia:**

```text
T(n) = T(n/3) + T(2n/3) + O(n)
```

En cada nivel del árbol de recurrencia, el tamaño total de los subproblemas continúa siendo aproximadamente `n`.

Por ejemplo:

```text
n/3 + 2n/3 = n
```

Por lo tanto, cada nivel tiene un costo total de `O(n)`.

La profundidad del árbol es `O(log n)`.

Entonces:

```text
T(n) = O(n log n)
```

**Resultado: O(n log n)**

---

## Ecuación 6

**Recurrencia:**

```text
T(n) = 3T(n/4) + O(n²)
```

Tenemos:

- `a = 3`
- `b = 4`
- `f(n) = O(n²)`
- `n^(log_4(3)) ≈ n^0.792`

Como:

```text
n² > n^0.792
```

`f(n)` crece más rápidamente que `n^(log_4(3))`.

Por lo tanto:

```text
T(n) = Θ(n²)
```

**Resultado: O(n²)**

---

# 2. Resumen

| Ecuación | Recurrencia | Complejidad |
|---|---|---|
| 1 | `2T(n/2) + O(n)` | **O(n log n)** |
| 2 | `4T(n/2) + O(n)` | **O(n²)** |
| 3 | `2T(n/2) + O(n²)` | **O(n²)** |
| 4 | `T(n-1) + O(n)` | **O(n²)** |
| 5 | `T(n/3) + T(2n/3) + O(n)` | **O(n log n)** |
| 6 | `3T(n/4) + O(n²)` | **O(n²)** |

---

# 3. Algoritmo Divide y Vencerás

Para la investigación se seleccionó **Merge Sort**, también conocido como ordenamiento por mezcla.

Merge Sort es un algoritmo clásico que utiliza el paradigma **Divide y Vencerás**.

## ¿Cómo funciona?

El algoritmo trabaja en tres etapas:

### 1. Dividir

La lista se divide aproximadamente en dos partes.

Por ejemplo:

```text
[38, 27, 43, 3, 9, 82, 10]

              ↓

[38, 27, 43]    [3, 9, 82, 10]
```

El proceso continúa hasta obtener listas de un solo elemento.

---

### 2. Vencer

Cada mitad se ordena utilizando recursión.

Una lista de un solo elemento ya está ordenada, por lo que constituye el **caso base**.

---

### 3. Combinar

Finalmente, las listas ordenadas se combinan para obtener una lista completamente ordenada.

Por ejemplo:

```text
[27, 38] + [3, 43]

        ↓

[3, 27, 38, 43]
```

---

# 4. Ecuación de recurrencia de Merge Sort

Merge Sort divide el problema en dos subproblemas de tamaño `n/2`.

Después de ordenar ambas partes, necesita `O(n)` operaciones para combinarlas.

Por lo tanto:

```text
T(n) = 2T(n/2) + O(n)
```

Esta es exactamente la **Ecuación 1** de este trabajo.

Aplicando el Teorema Maestro:

```text
a = 2
b = 2
f(n) = O(n)
```

Tenemos:

```text
n^(log_2 2) = n
```

Como `f(n) = Θ(n)`, obtenemos:

```text
T(n) = Θ(n log n)
```

Por lo tanto, la complejidad temporal de Merge Sort es:

**O(n log n)**

---

# 5. Ejemplo

Si tenemos:

```text
[38, 27, 43, 3, 9, 82, 10]
```

Merge Sort divide la lista y posteriormente combina las partes ordenadas.

Resultado:

```text
[3, 9, 10, 27, 38, 43, 82]
```

El programa incluido en `recurrencias.py` implementa este proceso utilizando funciones recursivas.

---

# 6. Complejidad de Merge Sort

### Complejidad temporal

```text
O(n log n)
```

Esto se mantiene en los casos típico, mejor y peor.

### Complejidad espacial

```text
O(n)
```

Se necesita espacio adicional para realizar la combinación de las listas.

---

# 7. Cómo ejecutar el programa

Tener Python instalado y ejecutar:

```bash
python recurrencias.py
```

El programa mostrará las seis recurrencias, sus complejidades y un ejemplo de Merge Sort.

---

# 8. Conclusión

Las ecuaciones de recurrencia permiten analizar cómo crece el tiempo de ejecución de algoritmos recursivos.

En este trabajo se analizaron seis recurrencias utilizando principalmente el **Teorema Maestro** y el análisis mediante árbol de recurrencia.

Como ejemplo del paradigma Divide y Vencerás se utilizó **Merge Sort**, ya que divide el problema en dos partes, resuelve recursivamente cada una y finalmente combina los resultados.

Su recurrencia es:

```text
T(n) = 2T(n/2) + O(n)
```

y su complejidad temporal es:

```text
O(n log n)
```

Esto demuestra cómo una recurrencia puede representar directamente el comportamiento de un algoritmo real.
