import heapq
import sys

class Grafo:
    def __init__(self):
        self.nodos = set()
        self.aristas = {}
        self.distancias = {}
    
    def agregar_nodo(self, nodo):
        self.nodos.add(nodo)
    
    def agregar_arista(self, desde_nodo, hasta_nodo, distancia):
        self.agregar_nodo(desde_nodo)
        self.agregar_nodo(hasta_nodo)
        
        if desde_nodo not in self.aristas:
            self.aristas[desde_nodo] = []
        self.aristas[desde_nodo].append(hasta_nodo)
        
        self.distancias[(desde_nodo, hasta_nodo)] = distancia

def dijkstra(grafo, inicio):
    # Inicializar distancias
    distancias = {nodo: float('infinity') for nodo in grafo.nodos}
    distancias[inicio] = 0
    
    # Cola de prioridad: (distancia, nodo)
    cola_prioridad = [(0, inicio)]
    
    # Diccionario para rastrear el camino
    camino_previo = {nodo: None for nodo in grafo.nodos}
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si encontramos un camino más corto a través de otro nodo, lo ignoramos
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        # Explorar vecinos
        if nodo_actual in grafo.aristas:
            for vecino in grafo.aristas[nodo_actual]:
                distancia = grafo.distancias[(nodo_actual, vecino)]
                nueva_distancia = distancia_actual + distancia
                
                # Si encontramos un camino más corto al vecino
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    camino_previo[vecino] = nodo_actual
                    heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
    
    return distancias, camino_previo

def obtener_camino(camino_previo, destino):
    camino = []
    nodo_actual = destino
    
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = camino_previo[nodo_actual]
    
    return camino[::-1]  # Invertir para obtener el camino desde el inicio

# Ejemplo de uso
def main():
    # Crear grafo
    g = Grafo()
    
    # Agregar aristas (origen, destino, peso)
    g.agregar_arista('A', 'B', 4)
    g.agregar_arista('A', 'C', 2)
    g.agregar_arista('B', 'C', 1)
    g.agregar_arista('B', 'D', 5)
    g.agregar_arista('C', 'D', 8)
    g.agregar_arista('C', 'E', 10)
    g.agregar_arista('D', 'E', 2)
    g.agregar_arista('D', 'F', 6)
    g.agregar_arista('E', 'F', 3)
    
    # Ejecutar Dijkstra desde el nodo 'A'
    inicio = 'A'
    distancias, camino_previo = dijkstra(g, inicio)
    
    # Mostrar resultados
    print("Distancias más cortas desde el nodo", inicio)
    print("-" * 40)
    for nodo in sorted(g.nodos):
        print(f"{nodo}: {distancias[nodo]}")
    
    print("\nCaminos más cortos:")
    print("-" * 40)
    for destino in sorted(g.nodos):
        if destino != inicio:
            camino = obtener_camino(camino_previo, destino)
            print(f"{inicio} -> {destino}: {' -> '.join(camino)} (Distancia: {distancias[destino]})")

# Versión simplificada para uso directo
def dijkstra_simplificado(grafo, inicio):
    """
    Versión simplificada que devuelve solo las distancias
    """
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[inicio] = 0
    cola = [(0, inicio)]
    
    while cola:
        distancia_actual, nodo_actual = heapq.heappop(cola)
        
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                heapq.heappush(cola, (distancia, vecino))
    
    return distancias

# Ejemplo con representación de grafo como diccionario
def ejemplo_simplificado():
    # Grafo representado como diccionario de diccionarios
    grafo = {
        'A': {'B': 4, 'C': 2},
        'B': {'C': 1, 'D': 5},
        'C': {'D': 8, 'E': 10},
        'D': {'E': 2, 'F': 6},
        'E': {'F': 3},
        'F': {}
    }
    
    distancias = dijkstra_simplificado(grafo, 'A')
    print("\nVersión simplificada:")
    for nodo, distancia in distancias.items():
        print(f"A -> {nodo}: {distancia}")

if __name__ == "__main__":
    main()
    ejemplo_simplificado()