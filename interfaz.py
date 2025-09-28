import pygame
import configuracion as cfg
from logica_grafos import construir_grafo_desde_datos, generador_dfs, generador_bfs, generador_kruskal, generador_prim
from manejo_archivos import guardar_grafo, cargar_grafo

# --- 1. Definición de Botones ---
botones = {
    # Fila 1: Edición del grafo
    'add_node': {'rect': pygame.Rect(10, 10, 140, 40), 'text': 'Añadir Nodo'},
    'add_edge': {'rect': pygame.Rect(160, 10, 140, 40), 'text': 'Añadir Arista'},
    'delete_last_node': {'rect': pygame.Rect(310, 10, 240, 40), 'text': 'Eliminar Último Nodo'},
    'delete_edge': {'rect': pygame.Rect(560, 10, 170, 40), 'text': 'Eliminar Arista'},
    'move_node': {'rect': pygame.Rect(740, 10, 140, 40), 'text': 'Mover Nodo'},
    
    # Fila 2: Algoritmos y utilidades
    'dfs': {'rect': pygame.Rect(10, 60, 100, 40), 'text': 'DFS'},
    'bfs': {'rect': pygame.Rect(120, 60, 100, 40), 'text': 'BFS'},
    'kruskal': {'rect': pygame.Rect(230, 60, 120, 40), 'text': 'Kruskal'},
    'prim': {'rect': pygame.Rect(360, 60, 100, 40), 'text': 'Prim'},
    'guardar': {'rect': pygame.Rect(cfg.ANCHO_CANVAS - 220, 10, 100, 40), 'text': 'Guardar'},
    'cargar': {'rect': pygame.Rect(cfg.ANCHO_CANVAS - 110, 10, 100, 40), 'text': 'Cargar'},
    'reset': {'rect': pygame.Rect(cfg.ANCHO_CANVAS - 110, 60, 100, 40), 'text': 'Reset'}
}

# --- 2. Manejo de Eventos ---

def manejar_eventos_teclado(evento, estado):
    if estado.modo == 'GET_WEIGHT':
        if evento.key == pygame.K_RETURN:
            peso = int(estado.texto_entrada_peso) if estado.texto_entrada_peso else 1
            estado.arista_activa_para_peso['weight'] = peso
            estado.aristas.append(estado.arista_activa_para_peso)
            estado.cambiar_modo('ADD_EDGE_START', "Arista añadida. Selecciona un nuevo nodo de inicio.")
        elif evento.key == pygame.K_BACKSPACE:
            estado.texto_entrada_peso = estado.texto_entrada_peso[:-1]
        elif evento.unicode.isdigit():
            estado.texto_entrada_peso += evento.unicode

def manejar_eventos_mouse(evento, estado):
    if evento.type == pygame.MOUSEWHEEL:
        # Ya no se necesita scroll específico para DFS, se puede quitar o generalizar
        pos = pygame.mouse.get_pos()
        if pos[0] > cfg.ANCHO_CANVAS:
            # Si se quiere mantener un scroll genérico para el panel derecho:
            estado.scroll_offset_y += evento.y * 20
            estado.scroll_offset_y = min(0, estado.scroll_offset_y)
            # El cálculo de max_scroll necesitaría ajustarse si otros algoritmos lo usan
            # max_scroll = max(0, estado.altura_total_contenido - (cfg.ALTO_PANTALLA - 100))
            # estado.scroll_offset_y = max(-max_scroll, estado.scroll_offset_y)
        return

    pos = evento.pos # Esto ahora solo se ejecuta para eventos que sí tienen 'pos'

    if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
        if pos[0] > cfg.ANCHO_CANVAS: return

        # Clic en botones
        for clave, btn in botones.items():
            if btn['rect'].collidepoint(pos):
                manejar_clic_boton(clave, estado)
                return

        # Clic en el lienzo
        if pos[1] > cfg.ALTO_PANEL_BOTONES:
            manejar_clic_lienzo(pos, estado)

    elif evento.type == pygame.MOUSEMOTION and estado.modo == 'MOVE_NODE' and estado.nodo_seleccionado_para_arrastre:
        estado.nodo_seleccionado_para_arrastre['pos'] = pos
        estado.nodo_seleccionado_para_arrastre['rect'].center = pos

    elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and estado.modo == 'MOVE_NODE':
        estado.nodo_seleccionado_para_arrastre = None

def manejar_clic_boton(clave, estado):
    if clave == 'add_node':
        estado.cambiar_modo('ADD_NODE', "Modo: Añadir Nodo. Haz clic para crear un nodo.")
    elif clave == 'add_edge':
        estado.cambiar_modo('ADD_EDGE_START', "Modo: Añadir Arista. Clic en el nodo de inicio.")
    elif clave == 'move_node':
        estado.cambiar_modo('MOVE_NODE', "Modo: Mover Nodo. Arrastra un nodo para moverlo.")
    elif clave == 'delete_last_node':
        estado.eliminar_ultimo_nodo()
    elif clave == 'delete_edge':
        estado.cambiar_modo('DELETE_EDGE', "Modo: Eliminar Arista. Haz clic en una arista.")
    elif clave == 'reset':
        estado.reiniciar_grafo()
    elif clave == 'guardar':
        guardar_grafo(estado)
    elif clave == 'cargar':
        cargar_grafo(estado)
    elif clave in ['dfs', 'bfs', 'prim']:
        if not estado.nodos:
            estado.cambiar_modo('IDLE', "Error: No hay nodos en el grafo.")
        else:
            estado.algoritmo_pendiente = clave
            estado.cambiar_modo('SELECT_START_NODE', f"Selecciona el nodo de inicio para {clave.upper()}.")
    elif clave == 'kruskal':
        if not estado.nodos:
            estado.cambiar_modo('IDLE', "Error: No hay nodos en el grafo.")
        else:
            iniciar_animacion(estado, 'kruskal', estado.nodos[0]['label']) # Kruskal no necesita nodo de inicio real

def iniciar_animacion(estado, algoritmo, nodo_inicial_label):
    G = construir_grafo_desde_datos(estado)
    estado.algoritmo_actual = algoritmo
    estado.nodo_inicial_algoritmo = nodo_inicial_label
    estado.estado_animacion = None

    if algoritmo == 'dfs':
        estado.generador_animacion = generador_dfs(G, nodo_inicial_label)
    elif algoritmo == 'bfs':
        estado.generador_animacion = generador_bfs(G, nodo_inicial_label)
    elif algoritmo == 'prim':
        estado.generador_animacion = generador_prim(G, nodo_inicial_label)
    elif algoritmo == 'kruskal':
        estado.generador_animacion = generador_kruskal(G)
    
    estado.cambiar_modo('ANIMATING', f"Iniciando animación de {algoritmo.upper()}...")
    estado.scroll_offset_y = 0
    estado.recorrido_resultado = []
    estado.peso_total_mst = 0
    estado.ultimo_tiempo_animacion = pygame.time.get_ticks()

def manejar_clic_lienzo(pos, estado):
    if estado.modo == 'ADD_NODE':
        estado.nodos.append({
            'pos': pos, 
            'label': str(estado.contador_nodos), 
            'rect': pygame.Rect(pos[0] - cfg.RADIO_NODO, pos[1] - cfg.RADIO_NODO, cfg.RADIO_NODO * 2, cfg.RADIO_NODO * 2)
        })
        estado.contador_nodos += 1
    
    elif estado.modo == 'MOVE_NODE':
        for nodo in estado.nodos:
            if nodo['rect'].collidepoint(pos):
                estado.nodo_seleccionado_para_arrastre = nodo
                break
    
    elif estado.modo == 'DELETE_EDGE':
        arista_a_eliminar = None
        for arista in estado.aristas:
            nodo_inicio = next((n for n in estado.nodos if n['label'] == arista['start']), None)
            nodo_fin = next((n for n in estado.nodos if n['label'] == arista['end']), None)
            if nodo_inicio and nodo_fin:
                if punto_en_segmento(pos, nodo_inicio['pos'], nodo_fin['pos']):
                    arista_a_eliminar = arista
                    break
        if arista_a_eliminar:
            estado.aristas.remove(arista_a_eliminar)
            estado.cambiar_modo('IDLE', f"Arista entre {arista_a_eliminar['start']} y {arista_a_eliminar['end']} eliminada.")

    elif estado.modo == 'SELECT_START_NODE':
        for nodo in estado.nodos:
            if nodo['rect'].collidepoint(pos):
                iniciar_animacion(estado, estado.algoritmo_pendiente, nodo['label'])
                estado.algoritmo_pendiente = None
                break

    elif estado.modo == 'ADD_EDGE_START':
        for nodo in estado.nodos:
            if nodo['rect'].collidepoint(pos):
                estado.nodo_inicio_arista_temporal = nodo
                estado.cambiar_modo('ADD_EDGE_END', f"Nodo '{nodo['label']}' seleccionado. Clic en el nodo de destino.")
                break
                
    elif estado.modo == 'ADD_EDGE_END':
        for nodo in estado.nodos:
            if nodo['rect'].collidepoint(pos) and nodo != estado.nodo_inicio_arista_temporal:
                existe = any(
                    (e['start'] == estado.nodo_inicio_arista_temporal['label'] and e['end'] == nodo['label']) or 
                    (e['start'] == nodo['label'] and e['end'] == estado.nodo_inicio_arista_temporal['label']) 
                    for e in estado.aristas
                )
                if not existe:
                    estado.arista_activa_para_peso = {'start': estado.nodo_inicio_arista_temporal['label'], 'end': nodo['label']}
                    estado.cambiar_modo('GET_WEIGHT', '')
                    estado.texto_entrada_peso = ''
                else:
                    estado.cambiar_modo('ADD_EDGE_START', "Error: La arista ya existe.")
                break

def punto_en_segmento(p, a, b, umbral=5):
    # Vector del segmento
    v = (b[0] - a[0], b[1] - a[1])
    # Vector desde el inicio del segmento al punto
    w = (p[0] - a[0], p[1] - a[1])
    
    # Proyección del punto sobre la línea del segmento
    c1 = w[0] * v[0] + w[1] * v[1]
    if c1 <= 0: # El punto está más allá de 'a'
        dist_sq = (p[0] - a[0])**2 + (p[1] - a[1])**2
        return dist_sq <= umbral**2
        
    c2 = v[0]**2 + v[1]**2
    if c2 <= c1: # El punto está más allá de 'b'
        dist_sq = (p[0] - b[0])**2 + (p[1] - b[1])**2
        return dist_sq <= umbral**2

    # El punto se proyecta dentro del segmento
    b_proj = c1 / c2
    px = a[0] + b_proj * v[0]
    py = a[1] + b_proj * v[1]
    dist_sq = (p[0] - px)**2 + (p[1] - py)**2
    
    return dist_sq <= umbral**2
