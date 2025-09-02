from nodo import Nodo


class Arbol:
    def __init__(self):
        self.raiz = None

    def vacio(self):
        """Verifica si el árbol está vacío."""
        return self.raiz is None

    def insertar(self, nombre):
        """Inserta un nuevo nodo en el árbol."""
        nuevo = Nodo(nombre)  # Cambiado de nodo a Nodo
        if self.raiz is None:
            self.raiz = nuevo
        else:
            self._insertar_rec(self.raiz, nuevo)

    def _insertar_rec(self, actual, nuevo):
        if nuevo.nombre < actual.nombre:
            if actual.izquierdo is None:
                actual.izquierdo = nuevo
            else:
                self._insertar_rec(actual.izquierdo, nuevo)
        else:
            if actual.derecho is None:
                actual.derecho = nuevo
            else:
                self._insertar_rec(actual.derecho, nuevo)

    def buscarNodo(self, nombre):
        """Busca un nodo por nombre utilizando recorrido en profundidad."""
        return self._buscar_rec(self.raiz, nombre)

    def _buscar_rec(self, actual, nombre):
        if actual is None:
            return None
        if actual.nombre == nombre:
            return actual
        elif nombre < actual.nombre:
            return self._buscar_rec(actual.izquierdo, nombre)
        else:
            return self._buscar_rec(actual.derecho, nombre)


# Ejemplo de uso
arbol = Arbol()
arbol.insertar('jose')
arbol.insertar('Ana')
arbol.insertar('manuel')
print("¿Árbol vacío?:", arbol.vacio())

nodo_encontrado = arbol.buscarNodo("Ana")  # Cambiado el nombre de variable para evitar conflicto
if nodo_encontrado:
    print("Nodo encontrado:", nodo_encontrado.nombre)
else:
    print("Nodo no encontrado")