# ============================================
# TAD PILA - DOBLE IMPLEMENTACIÓN
# 1. Arreglo dinámico
# 2. Lista enlazada
# ============================================


# ============================================
# IMPLEMENTACIÓN 1: PILA CON ARREGLO DINÁMICO
# ============================================

class PilaArreglo:
    """
    Implementación de una pila utilizando
    un arreglo dinámico creado manualmente.
    """

    def __init__(self, capacidad_inicial=4):
        self.capacidad = capacidad_inicial
        self.datos = [None] * self.capacidad
        self.tope = -1

    def apilar(self, elemento):
        """
        Agrega un elemento al tope de la pila.
        """

        # Si el arreglo está lleno, aumentar capacidad
        if self.tope + 1 == self.capacidad:
            self._redimensionar()

        self.tope += 1
        self.datos[self.tope] = elemento

    def _redimensionar(self):
        """
        Duplica la capacidad del arreglo.
        """

        nueva_capacidad = self.capacidad * 2
        nuevo_arreglo = [None] * nueva_capacidad

        i = 0

        while i <= self.tope:
            nuevo_arreglo[i] = self.datos[i]
            i += 1

        self.datos = nuevo_arreglo
        self.capacidad = nueva_capacidad

    def desapilar(self):
        """
        Elimina y devuelve el elemento del tope.
        """

        if self.esta_vacia():
            raise IndexError(
                "Error: no se puede desapilar porque la pila está vacía."
            )

        elemento = self.datos[self.tope]

        self.datos[self.tope] = None
        self.tope -= 1

        return elemento

    def esta_vacia(self):
        """
        Devuelve True si la pila está vacía.
        """

        return self.tope == -1

    def cima(self):
        """
        Devuelve el elemento del tope sin eliminarlo.
        """

        if self.esta_vacia():
            raise IndexError(
                "Error: no se puede consultar la cima porque la pila está vacía."
            )

        return self.datos[self.tope]

    # Alias por si la consigna anterior utiliza ver_tope()
    def ver_tope(self):
        return self.cima()

    def tamaño(self):
        """
        Devuelve la cantidad de elementos.
        """

        return self.tope + 1

    def mostrar(self):
        """
        Muestra los elementos desde el fondo hasta el tope.
        """

        if self.esta_vacia():
            print("Pila vacía.")
            return

        print("Fondo -> ", end="")

        i = 0

        while i <= self.tope:
            print(self.datos[i], end=" ")

            if i < self.tope:
                print("->", end=" ")

            i += 1

        print(" <- Tope")


# ============================================
# NODO PARA LA LISTA ENLAZADA
# ============================================

class Nodo:
    """
    Representa un nodo de una lista enlazada.
    """

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


# ============================================
# IMPLEMENTACIÓN 2: PILA CON LISTA ENLAZADA
# ============================================

class PilaLista:
    """
    Implementación de una pila utilizando
    una lista enlazada creada manualmente.
    """

    def __init__(self):
        self.tope = None
        self.cantidad = 0

    def apilar(self, elemento):
        """
        Agrega un elemento al tope de la pila.
        """

        nuevo_nodo = Nodo(elemento)

        nuevo_nodo.siguiente = self.tope
        self.tope = nuevo_nodo

        self.cantidad += 1

    def desapilar(self):
        """
        Elimina y devuelve el elemento del tope.
        """

        if self.esta_vacia():
            raise IndexError(
                "Error: no se puede desapilar porque la pila está vacía."
            )

        elemento = self.tope.dato

        self.tope = self.tope.siguiente
        self.cantidad -= 1

        return elemento

    def esta_vacia(self):
        """
        Devuelve True si la pila está vacía.
        """

        return self.tope is None

    def cima(self):
        """
        Devuelve el elemento del tope sin eliminarlo.
        """

        if self.esta_vacia():
            raise IndexError(
                "Error: no se puede consultar la cima porque la pila está vacía."
            )

        return self.tope.dato

    # Alias por si se utiliza el nombre ver_tope()
    def ver_tope(self):
        return self.cima()

    def tamaño(self):
        """
        Devuelve la cantidad de elementos.
        """

        return self.cantidad

    def mostrar(self):
        """
        Muestra los elementos desde el fondo hasta el tope.
        """

        if self.esta_vacia():
            print("Pila vacía.")
            return

        # Como no podemos utilizar una lista auxiliar,
        # usamos recursividad para mostrar desde el fondo.

        print("Fondo -> ", end="")
        self._mostrar_desde_fondo(self.tope)
        print(" <- Tope")

    def _mostrar_desde_fondo(self, nodo):

        if nodo is None:
            return

        self._mostrar_desde_fondo(nodo.siguiente)

        print(nodo.dato, end=" ")

        if nodo != self.tope:
            print("->", end=" ")


# ============================================
# PROGRAMA DE PRUEBAS
# ============================================

def probar_pilas():

    print("=" * 50)
    print("PRUEBA DEL TAD PILA")
    print("=" * 50)

    pila_arreglo = PilaArreglo()
    pila_lista = PilaLista()

    # ----------------------------------------
    # 1. ESTA VACÍA
    # ----------------------------------------

    print("\n1. Verificando si las pilas están vacías:")

    resultado_arreglo = pila_arreglo.esta_vacia()
    resultado_lista = pila_lista.esta_vacia()

    print("Arreglo:", resultado_arreglo)
    print("Lista enlazada:", resultado_lista)

    assert resultado_arreglo == resultado_lista

    # ----------------------------------------
    # 2. APILAR
    # ----------------------------------------

    print("\n2. Apilando elementos: 10, 20, 30")

    pila_arreglo.apilar(10)
    pila_lista.apilar(10)

    pila_arreglo.apilar(20)
    pila_lista.apilar(20)

    pila_arreglo.apilar(30)
    pila_lista.apilar(30)

    print("\nPila con arreglo:")
    pila_arreglo.mostrar()

    print("Pila con lista enlazada:")
    pila_lista.mostrar()

    # ----------------------------------------
    # 3. CIMA
    # ----------------------------------------

    print("\n3. Consultando la cima:")

    cima_arreglo = pila_arreglo.cima()
    cima_lista = pila_lista.cima()

    print("Cima arreglo:", cima_arreglo)
    print("Cima lista:", cima_lista)

    assert cima_arreglo == cima_lista

    # ----------------------------------------
    # 4. TAMAÑO
    # ----------------------------------------

    print("\n4. Consultando el tamaño:")

    tamaño_arreglo = pila_arreglo.tamaño()
    tamaño_lista = pila_lista.tamaño()

    print("Tamaño arreglo:", tamaño_arreglo)
    print("Tamaño lista:", tamaño_lista)

    assert tamaño_arreglo == tamaño_lista

    # ----------------------------------------
    # 5. DESAPILAR
    # ----------------------------------------

    print("\n5. Desapilando:")

    eliminado_arreglo = pila_arreglo.desapilar()
    eliminado_lista = pila_lista.desapilar()

    print("Elemento eliminado arreglo:", eliminado_arreglo)
    print("Elemento eliminado lista:", eliminado_lista)

    assert eliminado_arreglo == eliminado_lista

    # ----------------------------------------
    # 6. MOSTRAR
    # ----------------------------------------

    print("\n6. Estado final de ambas pilas:")

    print("Pila con arreglo:")
    pila_arreglo.mostrar()

    print("Pila con lista enlazada:")
    pila_lista.mostrar()

    # ----------------------------------------
    # VERIFICACIÓN FINAL
    # ----------------------------------------

    print("\nVerificación final:")

    assert pila_arreglo.tamaño() == pila_lista.tamaño()
    assert pila_arreglo.cima() == pila_lista.cima()

    print("✓ Ambas implementaciones producen los mismos resultados.")

    # ----------------------------------------
    # PRUEBA DE ERROR
    # ----------------------------------------

    print("\n7. Probando manejo de errores:")

    pila_vacia = PilaArreglo()

    try:
        pila_vacia.desapilar()

    except IndexError as error:
        print(error)


# ============================================
# EJECUCIÓN DEL PROGRAMA
# ============================================

if __name__ == "__main__":
    probar_pilas()