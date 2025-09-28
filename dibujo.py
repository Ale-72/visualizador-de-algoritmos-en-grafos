import pygame
from collections import deque
import configuracion as cfg

# --- Funciones de Dibujo Auxiliares ---

def calcular_posiciones_arbol_bfs(nodo_inicial, aristas_arbol, nodos_app):
    if not nodo_inicial: return {}
    
    adj = {nodo['label']: [] for nodo in nodos_app}
    for u, v in aristas_arbol:
        adj[u].append(v)
        
    niveles = {}
    nodos_por_nivel = {}
    cola = deque([(nodo_inicial, 0)])
    visitado_para_layout = {nodo_inicial}
    
    while cola:
        etiqueta_nodo, nivel = cola.popleft()
        niveles[etiqueta_nodo] = nivel
        if nivel not in nodos_por_nivel: nodos_por_nivel[nivel] = []
        nodos_por_nivel[nivel].append(etiqueta_nodo)
        
        for vecino in adj.get(etiqueta_nodo, []):
            if vecino not in visitado_para_layout:
                visitado_para_layout.add(vecino)
                cola.append((vecino, nivel + 1))

    posiciones = {}
    num_niveles = len(nodos_por_nivel)
    espaciado_y = (cfg.ALTO_PANTALLA - 120) / max(1, num_niveles)

    for nivel, nodos_en_nivel in nodos_por_nivel.items():
        espaciado_x = cfg.ANCHO_PANEL_SOLUCION / (len(nodos_en_nivel) + 1)
        for i, etiqueta_nodo in enumerate(nodos_en_nivel):
            pos_x = cfg.ANCHO_CANVAS + (i + 1) * espaciado_x
            pos_y = 80 + nivel * espaciado_y
            posiciones[etiqueta_nodo] = (int(pos_x), int(pos_y))
            
    return posiciones

# --- Funciones de Dibujo Principales ---

def dibujar_panel_solucion(pantalla, estado):
    estado.altura_total_contenido = 0
    rect_panel = pygame.Rect(cfg.ANCHO_CANVAS, 0, cfg.ANCHO_PANEL_SOLUCION, cfg.ALTO_PANTALLA)
    pygame.draw.rect(pantalla, cfg.GRIS_OSCURO, rect_panel)
    pygame.draw.line(pantalla, cfg.NEGRO, (cfg.ANCHO_CANVAS, 0), (cfg.ANCHO_CANVAS, cfg.ALTO_PANTALLA), 2)

    titulo_texto = f"Solución {estado.algoritmo_actual.upper()}" if estado.algoritmo_actual else "Panel de Solución"
    surf_titulo = cfg.FUENTE_GRANDE.render(titulo_texto, True, cfg.BLANCO)
    pantalla.blit(surf_titulo, surf_titulo.get_rect(center=(cfg.ANCHO_CANVAS + cfg.ANCHO_PANEL_SOLUCION / 2, 40)))

    if not estado.estado_animacion: return

    # --- Lógica para dibujar DFS y BFS (como árbol) ---
    if estado.algoritmo_actual in ['dfs', 'bfs']:
        nodo_inicial = estado.nodo_inicial_algoritmo if estado.nodo_inicial_algoritmo else (estado.nodos[0]['label'] if estado.nodos else None)
        if not nodo_inicial: return

        posiciones = calcular_posiciones_arbol_bfs(nodo_inicial, estado.estado_animacion.get('tree_edges', []), estado.nodos)
        
        # Dibujar aristas del árbol
        for u, v in estado.estado_animacion.get('tree_edges', []):
            if u in posiciones and v in posiciones:
                pygame.draw.line(pantalla, cfg.BLANCO, posiciones[u], posiciones[v], 2)
        
        # Dibujar nodos del árbol
        for etiqueta_nodo, pos in posiciones.items():
            color = cfg.VERDE if etiqueta_nodo in estado.estado_animacion['visited'] else cfg.AZUL
            if etiqueta_nodo == estado.estado_animacion['current']: color = cfg.ROJO
            
            pygame.draw.circle(pantalla, color, pos, cfg.RADIO_NODO - 5)
            pygame.draw.circle(pantalla, cfg.BLANCO, pos, cfg.RADIO_NODO - 5, 1)
            surf_etiqueta = cfg.FUENTE_PEQUENA.render(etiqueta_nodo, True, cfg.BLANCO)
            pantalla.blit(surf_etiqueta, surf_etiqueta.get_rect(center=pos))
    
    elif estado.algoritmo_actual == 'kruskal':
        # Esta sección ahora dibujará el MST en el panel derecho
        offset_y = 80 + estado.scroll_offset_y
        espaciado_linea = 30
        
        if 'all_edges' in estado.estado_animacion:
            estado.altura_total_contenido = len(estado.estado_animacion['all_edges']) * espaciado_linea
            
            for i, (u, v, data) in enumerate(estado.estado_animacion['all_edges']):
                pos_y = offset_y + i * espaciado_linea
                if 60 < pos_y < cfg.ALTO_PANTALLA:
                    texto = f"Arista ({u}, {v}) - Peso: {data.get('weight', 1)}"
                    color_texto = cfg.GRIS
                    
                    # Resaltar la arista considerada actualmente
                    if estado.estado_animacion['considered'] == (u, v):
                        status = estado.estado_animacion['status']
                        if status == 'accepted': color_texto = cfg.VERDE
                        elif status == 'rejected': color_texto = cfg.ROJO
                        else: color_texto = cfg.AMARILLO # 'considering'
                    
                    # Marcar las aristas que ya están en el MST
                    if (u, v) in estado.estado_animacion['mst_edges'] or (v, u) in estado.estado_animacion['mst_edges']:
                         color_texto = cfg.VERDE

                    surf_texto = cfg.FUENTE_PEQUENA.render(texto, True, color_texto)
                    pantalla.blit(surf_texto, (cfg.ANCHO_CANVAS + 20, pos_y))

    elif estado.algoritmo_actual == 'prim':
        offset_y = 80 + estado.scroll_offset_y
        espaciado_linea = 30
        
        if 'frontier' in estado.estado_animacion:
            # La altura del contenido puede basarse en la frontera más las aristas del MST
            altura_contenido = (len(estado.estado_animacion.get('frontier', [])) + len(estado.estado_animacion.get('mst_edges', []))) * espaciado_linea
            estado.altura_total_contenido = altura_contenido

            # Mostrar aristas en el MST
            texto_mst = cfg.FUENTE_MEDIANA.render("Aristas en el MST:", True, cfg.VERDE)
            pantalla.blit(texto_mst, (cfg.ANCHO_CANVAS + 20, offset_y))
            offset_y += 40

            for i, (u, v) in enumerate(estado.estado_animacion['mst_edges']):
                pos_y = offset_y + i * espaciado_linea
                if 60 < pos_y < cfg.ALTO_PANTALLA:
                    texto = f"Arista ({u}, {v})"
                    surf_texto = cfg.FUENTE_PEQUENA.render(texto, True, cfg.VERDE)
                    pantalla.blit(surf_texto, (cfg.ANCHO_CANVAS + 30, pos_y))
            
            offset_y += len(estado.estado_animacion['mst_edges']) * espaciado_linea + 20

            # Mostrar aristas en la frontera
            texto_frontera = cfg.FUENTE_MEDIANA.render("Frontera (Cola de Prioridad):", True, cfg.AMARILLO)
            pantalla.blit(texto_frontera, (cfg.ANCHO_CANVAS + 20, offset_y))
            offset_y += 40

            frontera_ordenada = sorted(estado.estado_animacion.get('frontier', []))
            for i, (peso, u, v) in enumerate(frontera_ordenada):
                pos_y = offset_y + i * espaciado_linea
                if 60 < pos_y < cfg.ALTO_PANTALLA:
                    texto = f"({u}, {v}) - Peso: {peso}"
                    color = cfg.GRIS
                    
                    # Resaltar la arista considerada
                    if estado.estado_animacion['considered_edge'] == (u, v):
                        status = estado.estado_animacion['status']
                        if status == 'accepted': color = cfg.VERDE
                        elif status == 'rejected': color = cfg.ROJO
                        else: color = cfg.AMARILLO

                    surf_texto = cfg.FUENTE_PEQUENA.render(texto, True, color)
                    pantalla.blit(surf_texto, (cfg.ANCHO_CANVAS + 30, pos_y))

def dibujar_modal_ingreso_peso(pantalla, estado):
    overlay = pygame.Surface((cfg.ANCHO_CANVAS, cfg.ALTO_PANTALLA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    pantalla.blit(overlay, (0, 0))
    rect_caja = pygame.Rect(0, 0, 400, 150)
    rect_caja.center = (cfg.ANCHO_CANVAS / 2, cfg.ALTO_PANTALLA / 2)
    pygame.draw.rect(pantalla, cfg.GRIS, rect_caja, border_radius=15)
    pygame.draw.rect(pantalla, cfg.BLANCO, rect_caja, 3, border_radius=15)
    surf_titulo = cfg.FUENTE_GRANDE.render("Ingrese el Peso", True, cfg.BLANCO)
    pantalla.blit(surf_titulo, surf_titulo.get_rect(center=(rect_caja.centerx, rect_caja.top + 30)))
    caja_input = pygame.Rect(0, 0, 100, 40)
    caja_input.center = rect_caja.center
    pygame.draw.rect(pantalla, cfg.BLANCO, caja_input)
    surf_input = cfg.FUENTE_MEDIANA.render(estado.texto_entrada_peso, True, cfg.NEGRO)
    pantalla.blit(surf_input, surf_input.get_rect(center=caja_input.center))
    if int(pygame.time.get_ticks() / 500) % 2 == 0:
        pos_cursor = surf_input.get_rect(center=caja_input.center).right + 2
        pygame.draw.line(pantalla, cfg.NEGRO, (pos_cursor, caja_input.top + 10), (pos_cursor, caja_input.bottom - 10), 2)

def dibujar_elementos(pantalla, estado, botones):
    pantalla.fill(cfg.BLANCO)
    pygame.draw.rect(pantalla, cfg.GRIS, (0, 0, cfg.ANCHO_CANVAS, cfg.ALTO_PANEL_BOTONES))
    dibujar_panel_solucion(pantalla, estado)
    
    for btn in botones.values():
        pygame.draw.rect(pantalla, cfg.AZUL_CLARO, btn['rect'])
        surf_texto = cfg.FUENTE_MEDIANA.render(btn['text'], True, cfg.NEGRO)
        pantalla.blit(surf_texto, surf_texto.get_rect(center=btn['rect'].center))
        
    for arista in estado.aristas:
        nodo_inicio = next((n for n in estado.nodos if n['label'] == arista['start']), None)
        nodo_fin = next((n for n in estado.nodos if n['label'] == arista['end']), None)
        if nodo_inicio and nodo_fin:
            pygame.draw.line(pantalla, arista.get('color', cfg.NEGRO), nodo_inicio['pos'], nodo_fin['pos'], 2)
            pos_media = ((nodo_inicio['pos'][0] + nodo_fin['pos'][0]) / 2, (nodo_inicio['pos'][1] + nodo_fin['pos'][1]) / 2)
            surf_peso = cfg.FUENTE_PEQUENA.render(str(arista['weight']), True, cfg.PURPURA)
            pantalla.blit(surf_peso, (pos_media[0] + 5, pos_media[1] - 15))
            
    for nodo in estado.nodos:
        color = nodo.get('color', cfg.AZUL)
        if nodo == estado.nodo_seleccionado_para_arrastre: color = cfg.AMARILLO
        pygame.draw.circle(pantalla, color, nodo['pos'], cfg.RADIO_NODO)
        pygame.draw.circle(pantalla, cfg.NEGRO, nodo['pos'], cfg.RADIO_NODO, 2)
        surf_etiqueta = cfg.FUENTE_MEDIANA.render(nodo['label'], True, cfg.BLANCO)
        pantalla.blit(surf_etiqueta, surf_etiqueta.get_rect(center=nodo['pos']))
        
    surf_estado = cfg.FUENTE_MEDIANA.render(estado.texto_estado, True, cfg.NEGRO)
    pantalla.blit(surf_estado, (10, cfg.ALTO_CANVAS + 15))

    # --- Mostrar resultados de algoritmos ---
    if estado.algoritmo_actual and estado.recorrido_resultado:
        texto_recorrido = f"Recorrido {estado.algoritmo_actual.upper()}: {', '.join(estado.recorrido_resultado)}"
        surf_recorrido = cfg.FUENTE_PEQUENA.render(texto_recorrido, True, cfg.NEGRO)
        pantalla.blit(surf_recorrido, (10, cfg.ALTO_CANVAS + 50))
    
    if estado.algoritmo_actual in ['kruskal', 'prim'] and estado.peso_total_mst > 0:
        texto_peso = f"Peso Total del MST: {estado.peso_total_mst}"
        surf_peso = cfg.FUENTE_PEQUENA.render(texto_peso, True, cfg.NEGRO)
        pantalla.blit(surf_peso, (10, cfg.ALTO_CANVAS + 50))
    
    if estado.modo == 'GET_WEIGHT':
        dibujar_modal_ingreso_peso(pantalla, estado)
        
    pygame.display.flip()
