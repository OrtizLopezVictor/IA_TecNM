from collections import deque, defaultdict
import heapq
import math

class Nodo:
    def __init__(self, estado, padre=None, accion=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.accion = accion
        self.costo = costo
    
    def __lt__(self, otro):
        return self.costo < otro.costo
def busqueda_anchura(estado_inicial, es_objetivo, obtener_sucesores):
    frontera = deque([Nodo(estado_inicial)])
    visitados = set([estado_inicial])
    nodos_expandidos = 0
    
    while frontera:
        nodo_actual = frontera.popleft()
        nodos_expandidos += 1
        
        if es_objetivo(nodo_actual.estado):
            return reconstruir_camino(nodo_actual), nodos_expandidos
        
        for accion, estado_siguiente, costo in obtener_sucesores(nodo_actual.estado):
            if estado_siguiente not in visitados:
                visitados.add(estado_siguiente)
                nuevo_nodo = Nodo(estado_siguiente, nodo_actual, accion, nodo_actual.costo + costo)
                frontera.append(nuevo_nodo)
    
    return None, nodos_expandidos
def busqueda_profundidad(estado_inicial, es_objetivo, obtener_sucesores, limite_profundidad=float('inf')):
    frontera = [Nodo(estado_inicial)]
    visitados = set()
    nodos_expandidos = 0
    
    while frontera:
        nodo_actual = frontera.pop()
        nodos_expandidos += 1
        
        if es_objetivo(nodo_actual.estado):
            return reconstruir_camino(nodo_actual), nodos_expandidos
        
        if profundidad(nodo_actual) < limite_profundidad:
            if nodo_actual.estado not in visitados:
                visitados.add(nodo_actual.estado)
                
                sucesores = []
                for accion, estado_siguiente, costo in obtener_sucesores(nodo_actual.estado):
                    if estado_siguiente not in visitados:
                        nuevo_nodo = Nodo(estado_siguiente, nodo_actual, accion, nodo_actual.costo + costo)
                        sucesores.append(nuevo_nodo)
                frontera.extend(reversed(sucesores))
    
    return None, nodos_expandidos
def busqueda_costo_uniforme(estado_inicial, es_objetivo, obtener_sucesores):
    frontera = []
    heapq.heappush(frontera, (0, Nodo(estado_inicial)))
    visitados = {}
    nodos_expandidos = 0
    
    while frontera:
        costo_actual, nodo_actual = heapq.heappop(frontera)
        nodos_expandidos += 1
        
        if es_objetivo(nodo_actual.estado):
            return reconstruir_camino(nodo_actual), nodos_expandidos
        
        if nodo_actual.estado in visitados and visitados[nodo_actual.estado] <= nodo_actual.costo:
            continue
            
        visitados[nodo_actual.estado] = nodo_actual.costo
        
        for accion, estado_siguiente, costo in obtener_sucesores(nodo_actual.estado):
            nuevo_costo = nodo_actual.costo + costo
            if estado_siguiente not in visitados or nuevo_costo < visitados[estado_siguiente]:
                nuevo_nodo = Nodo(estado_siguiente, nodo_actual, accion, nuevo_costo)
                heapq.heappush(frontera, (nuevo_costo, nuevo_nodo))
    
    return None, nodos_expandidos
def busqueda_bidireccional(estado_inicial, estado_objetivo, obtener_sucesores):
    frontera_inicio = deque([Nodo(estado_inicial)])
    frontera_objetivo = deque([Nodo(estado_objetivo)])
    
    visitados_inicio = {estado_inicial: Nodo(estado_inicial)}
    visitados_objetivo = {estado_objetivo: Nodo(estado_objetivo)}
    
    while frontera_inicio and frontera_objetivo:
        nodo_actual = frontera_inicio.popleft()
        for _, estado_siguiente, costo in obtener_sucesores(nodo_actual.estado):
            if estado_siguiente in visitados_objetivo:
                camino_inicio = reconstruir_camino(nodo_actual)
                camino_objetivo = reconstruir_camino(visitados_objetivo[estado_siguiente], reverso=True)
                return camino_inicio + list(reversed(camino_objetivo[1:]))
            
            if estado_siguiente not in visitados_inicio:
                nuevo_nodo = Nodo(estado_siguiente, nodo_actual, None, nodo_actual.costo + costo)
                visitados_inicio[estado_siguiente] = nuevo_nodo
                frontera_inicio.append(nuevo_nodo)
    return None
def busqueda_profundidad_iterativa(estado_inicial, es_objetivo, obtener_sucesores, limite_maximo=100):
    for profundidad in range(limite_maximo + 1):
        resultado, nodos = busqueda_profundidad_limitada(estado_inicial, es_objetivo, obtener_sucesores, profundidad)
        if resultado is not None:
            return resultado, nodos
    return None, 0

def busqueda_profundidad_limitada(estado_inicial, es_objetivo, obtener_sucesores, limite_profundidad):
    return busqueda_profundidad(estado_inicial, es_objetivo, obtener_sucesores, limite_profundidad)
def reconstruir_camino(nodo, reverso=False):
    camino = []
    while nodo:
        if nodo.accion:
            camino.append((nodo.accion, nodo.estado))
        else:
            camino.append((None, nodo.estado))
        nodo = nodo.padre
    return list(reversed(camino)) if not reverso else camino

def profundidad(nodo):
    profundidad = 0
    while nodo.padre:
        profundidad += 1
        nodo = nodo.padre
    return profundidad
def heuristica_manhattan(estado_actual, estado_objetivo):
    """Heurística de distancia Manhattan para problemas de coordenadas 2D"""
    if hasattr(estado_actual, 'x') and hasattr(estado_actual, 'y'):
        return abs(estado_actual.x - estado_objetivo.x) + abs(estado_actual.y - estado_objetivo.y)
    return 0

def heuristica_euclidiana(estado_actual, estado_objetivo):
    """Heurística de distancia Euclidiana"""
    if hasattr(estado_actual, 'x') and hasattr(estado_actual, 'y'):
        return math.sqrt((estado_actual.x - estado_objetivo.x)**2 + 
                        (estado_actual.y - estado_objetivo.y)**2)
    return 0
def heuristica_puzzle(estado_actual, estado_objetivo):
    """Heurística para puzzles: cuenta piezas en posición incorrecta"""
    if isinstance(estado_actual, (list, tuple)) and isinstance(estado_objetivo, (list, tuple)):
        return sum(1 for a, b in zip(estado_actual, estado_objetivo) if a != b)
    return 0