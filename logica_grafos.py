import networkx as nx
from collections import deque
import heapq

def construir_grafo_desde_datos(estado):
    G = nx.Graph()
    for n in estado.nodos:
        G.add_node(n['label'])
    for e in estado.aristas:
        G.add_edge(e['start'], e['end'], weight=e['weight'])
    return G

def generador_dfs(grafo, nodo_inicial):
    visitado, pila, aristas_arbol, recorrido = set(), [(nodo_inicial, None)], [], []
    
    while pila:
        nodo, padre = pila.pop(0)
        
        if nodo not in visitado:
            visitado.add(nodo)
            recorrido.append(nodo)
            if padre:
                aristas_arbol.append((padre, nodo))
            
            yield {'visited': visitado.copy(), 'current': nodo, 'tree_edges': aristas_arbol.copy(), 'recorrido': recorrido.copy()}
            
            vecinos = sorted(list(grafo.neighbors(nodo)), reverse=True)
            for vecino in vecinos:
                if vecino not in visitado:
                    pila.insert(0, (vecino, nodo))

def generador_bfs(grafo, nodo_inicial):
    visitado, cola, aristas_arbol, recorrido = {nodo_inicial}, deque([(nodo_inicial, None)]), [], [nodo_inicial]
    while cola:
        nodo, padre = cola.popleft()
        if padre:
            aristas_arbol.append((padre, nodo))
        yield {'visited': visitado.copy(), 'current': nodo, 'queue': {q[0] for q in cola}, 'tree_edges': aristas_arbol.copy(), 'recorrido': recorrido.copy()}
        for vecino in sorted(list(grafo.neighbors(nodo))):
            if vecino not in visitado:
                visitado.add(vecino)
                recorrido.append(vecino)
                cola.append((vecino, nodo))

def generador_kruskal(grafo):
    aristas_ordenadas = sorted(grafo.edges(data=True), key=lambda t: t[2].get('weight', 1))
    aristas_mst, padre = [], {nodo: nodo for nodo in grafo.nodes()}
    peso_total = 0
    
    def encontrar(v):
        return v if v == padre[v] else encontrar(padre[v])
        
    def unir(a, b):
        a, b = encontrar(a), encontrar(b)
        if a != b:
            padre[b] = a
            return True
        return False

    # Estado inicial para mostrar todas las aristas
    yield {'mst_edges': [], 'considered': None, 'status': 'starting', 'all_edges': aristas_ordenadas, 'peso_total': 0}

    for u, v, data in aristas_ordenadas:
        estado = 'accepted' if unir(u, v) else 'rejected'
        if estado == 'accepted':
            aristas_mst.append((u, v))
            peso_total += data.get('weight', 1)
        yield {'mst_edges': aristas_mst.copy(), 'considered': (u, v), 'status': estado, 'all_edges': aristas_ordenadas, 'peso_total': peso_total}
    
    # Estado final
    yield {'mst_edges': aristas_mst.copy(), 'considered': None, 'status': 'finished', 'all_edges': aristas_ordenadas, 'peso_total': peso_total}

def generador_prim(grafo, nodo_inicial):
    if not grafo.nodes:
        return

    if nodo_inicial not in grafo:
        nodo_inicial = list(grafo.nodes)[0]

    
    nodos_en_mst = {nodo_inicial}
    aristas_mst = []
    frontera = [] # Priority queue de aristas (peso, u, v)
    peso_total = 0

    # Llenar la frontera con las aristas del nodo inicial
    for vecino in grafo.neighbors(nodo_inicial):
        peso = grafo[nodo_inicial][vecino].get('weight', 1)
        heapq.heappush(frontera, (peso, nodo_inicial, vecino))

    # Estado inicial para la visualización
    yield {
        'mst_edges': [],
        'nodes_in_mst': nodos_en_mst.copy(),
        'frontier': frontera.copy(),
        'considered_edge': None,
        'status': 'starting',
        'peso_total': 0
    }

    while frontera and len(nodos_en_mst) < len(grafo.nodes):
        peso, u, v = heapq.heappop(frontera)

        if v in nodos_en_mst:
            # Si el nodo de destino ya está en el MST, ignorar esta arista
            yield {
                'mst_edges': aristas_mst.copy(),
                'nodes_in_mst': nodos_en_mst.copy(),
                'frontier': frontera.copy(),
                'considered_edge': (u, v),
                'status': 'rejected',
                'peso_total': peso_total
            }
            continue

        # Aceptar la arista y el nodo
        nodos_en_mst.add(v)
        aristas_mst.append((u, v))
        peso_total += peso

        yield {
            'mst_edges': aristas_mst.copy(),
            'nodes_in_mst': nodos_en_mst.copy(),
            'frontier': frontera.copy(),
            'considered_edge': (u, v),
            'status': 'accepted',
            'peso_total': peso_total
        }

        # Añadir nuevas aristas a la frontera desde el nuevo nodo 'v'
        for vecino_de_v in grafo.neighbors(v):
            if vecino_de_v not in nodos_en_mst:
                nuevo_peso = grafo[v][vecino_de_v].get('weight', 1)
                heapq.heappush(frontera, (nuevo_peso, v, vecino_de_v))

    # Estado final
    yield {
        'mst_edges': aristas_mst.copy(),
        'nodes_in_mst': nodos_en_mst.copy(),
        'frontier': [],
        'considered_edge': None,
        'status': 'finished',
        'peso_total': peso_total
    }
