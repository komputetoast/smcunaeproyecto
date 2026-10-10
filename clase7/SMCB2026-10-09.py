"""Implementacion educativa de un arbol AVL.

Factor de equilibrio (FE) usado en este programa:
    FE = altura(subarbol_derecho) - altura(subarbol_izquierdo)

Interpretacion:
    FE == -2: subarbol izquierdo demasiado alto.
    FE == +2: subarbol derecho demasiado alto.

El programa muestra tres secuencias de ejemplo, indicando las rotaciones
aplicadas durante cada insercion.
"""


class Nodo:
    """Nodo de un arbol binario de busqueda AVL."""

    def __init__(self, valor):
        self.valor = valor
        self.izquierdo = None
        self.derecho = None
        self.altura = 1  # Un nodo hoja tiene altura 1.


class ArbolAVL:
    """Arbol AVL con insercion automatica y cuatro casos de rotacion."""

    def __init__(self):
        self.raiz = None
        self.rotaciones = []

    @staticmethod
    def altura(nodo):
        """Devuelve la altura; un subarbol vacio tiene altura 0."""
        return nodo.altura if nodo is not None else 0

    @classmethod
    def factor_equilibrio(cls, nodo):
        """FE = altura derecha - altura izquierda."""
        if nodo is None:
            return 0
        return cls.altura(nodo.derecho) - cls.altura(nodo.izquierdo)

    @classmethod
    def _actualizar_altura(cls, nodo):
        nodo.altura = 1 + max(cls.altura(nodo.izquierdo),
                              cls.altura(nodo.derecho))

    @classmethod
    def _rotacion_derecha(cls, y):
        """Rotacion simple a la derecha (caso LL)."""
        x = y.izquierdo
        subarbol = x.derecho

        # Ejecutar la rotacion.
        x.derecho = y
        y.izquierdo = subarbol

        # Actualizar primero el nodo que bajo y luego el nuevo padre.
        cls._actualizar_altura(y)
        cls._actualizar_altura(x)
        return x

    @classmethod
    def _rotacion_izquierda(cls, x):
        """Rotacion simple a la izquierda (caso RR)."""
        y = x.derecho
        subarbol = y.izquierdo

        # Ejecutar la rotacion.
        y.izquierdo = x
        x.derecho = subarbol

        # Actualizar primero el nodo que bajo y luego el nuevo padre.
        cls._actualizar_altura(x)
        cls._actualizar_altura(y)
        return y

    def _insertar(self, nodo, valor):
        """Inserta recursivamente como BST y rebalancea al regresar."""
        # 1. Insercion BST.
        if nodo is None:
            return Nodo(valor)
        if valor < nodo.valor:
            nodo.izquierdo = self._insertar(nodo.izquierdo, valor)
        elif valor > nodo.valor:
            nodo.derecho = self._insertar(nodo.derecho, valor)
        else:
            # Politica para duplicados: no se insertan valores repetidos.
            return nodo

        # 2. Actualizar la altura del nodo actual.
        self._actualizar_altura(nodo)

        # 3. Calcular el FE y detectar los cuatro casos AVL.
        fe = self.factor_equilibrio(nodo)

        # Caso LL: desequilibrio a la izquierda y el hijo izquierdo
        # tambien esta cargado hacia la izquierda o equilibrado.
        if fe < -1 and self.factor_equilibrio(nodo.izquierdo) <= 0:
            self.rotaciones.append(f"LL en el nodo {nodo.valor}: rotacion derecha")
            return self._rotacion_derecha(nodo)

        # Caso RR: desequilibrio a la derecha y el hijo derecho
        # tambien esta cargado hacia la derecha o equilibrado.
        if fe > 1 and self.factor_equilibrio(nodo.derecho) >= 0:
            self.rotaciones.append(f"RR en el nodo {nodo.valor}: rotacion izquierda")
            return self._rotacion_izquierda(nodo)

        # Caso LR: izquierda pesada, pero el hijo izquierdo esta cargado
        # hacia la derecha. Primero gira a la izquierda y luego a la derecha.
        if fe < -1 and self.factor_equilibrio(nodo.izquierdo) > 0:
            self.rotaciones.append(f"LR en el nodo {nodo.valor}: izquierda y luego derecha")
            nodo.izquierdo = self._rotacion_izquierda(nodo.izquierdo)
            return self._rotacion_derecha(nodo)

        # Caso RL: derecha pesada, pero el hijo derecho esta cargado
        # hacia la izquierda. Primero gira a la derecha y luego a la izquierda.
        if fe > 1 and self.factor_equilibrio(nodo.derecho) < 0:
            self.rotaciones.append(f"RL en el nodo {nodo.valor}: derecha y luego izquierda")
            nodo.derecho = self._rotacion_derecha(nodo.derecho)
            return self._rotacion_izquierda(nodo)

        return nodo

    def insertar(self, valor):
        """Inserta un valor y devuelve las rotaciones realizadas."""
        self.rotaciones = []
        self.raiz = self._insertar(self.raiz, valor)
        return self.rotaciones.copy()

    def inorden(self):
        """Devuelve los valores en orden ascendente (verifica la regla BST)."""
        resultado = []

        def recorrer(nodo):
            if nodo is not None:
                recorrer(nodo.izquierdo)
                resultado.append(nodo.valor)
                recorrer(nodo.derecho)

        recorrer(self.raiz)
        return resultado

    def mostrar_arbol(self):
        """Imprime el arbol de costado; cada linea incluye altura y FE.

        El hijo derecho aparece arriba y el izquierdo abajo.
        """
        if self.raiz is None:
            print("(arbol vacio)")
            return

        def imprimir(nodo, prefijo="", es_izquierdo=True):
            if nodo is None:
                return
            imprimir(nodo.derecho, prefijo + ("│   " if es_izquierdo else "    "), False)
            conector = "└── " if es_izquierdo else "┌── "
            fe = self.factor_equilibrio(nodo)
            print(f"{prefijo}{conector}{nodo.valor} (altura={nodo.altura}, FE={fe:+d})")
            imprimir(nodo.izquierdo, prefijo + ("    " if es_izquierdo else "│   "), True)

        imprimir(self.raiz)

    def esta_balanceado(self):
        """Comprueba que todos los nodos tengan FE entre -1 y +1."""
        def revisar(nodo):
            if nodo is None:
                return True
            fe = self.factor_equilibrio(nodo)
            return (-1 <= fe <= 1 and revisar(nodo.izquierdo)
                    and revisar(nodo.derecho))
        return revisar(self.raiz)


def ejecutar_secuencia(secuencia, numero):
    print("\n" + "=" * 68)
    print(f"SECUENCIA {numero}: {secuencia}")
    print("=" * 68)
    arbol = ArbolAVL()

    for valor in secuencia:
        rotaciones = arbol.insertar(valor)
        print(f"\nInsertar {valor}:")
        if rotaciones:
            for rotacion in rotaciones:
                print(f"  Rotacion aplicada: {rotacion}")
        else:
            print("  Rotacion aplicada: ninguna; el arbol sigue balanceado.")
        arbol.mostrar_arbol()
        print(f"  Recorrido inorden: {arbol.inorden()}")
        print(f"  ¿AVL balanceado?: {'Si' if arbol.esta_balanceado() else 'No'}")


if __name__ == "__main__":
    secuencias = [
        [10, 20, 30, 40, 50, 25],
        [30, 10, 40, 20, 15, 35],
        [50, 40, 30, 20, 10, 25],
    ]

    for indice, secuencia in enumerate(secuencias, start=1):
        ejecutar_secuencia(secuencia, indice)

    print("\nNOTA: FE = altura del subarbol derecho - altura del subarbol izquierdo.")
    print("Un arbol AVL correctamente balanceado mantiene FE en {-1, 0, +1}.")
