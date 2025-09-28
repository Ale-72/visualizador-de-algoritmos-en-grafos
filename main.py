import pygame
from estado import EstadoApp
import configuracion as cfg
from dibujo import dibujar_elementos
from interfaz import botones, manejar_eventos_teclado, manejar_eventos_mouse

def procesar_animacion(estado):
    if pygame.time.get_ticks() - estado.ultimo_tiempo_animacion > cfg.VELOCIDAD_ANIMACION_MS:
        estado.ultimo_tiempo_animacion = pygame.time.get_ticks()
        try:
            estado.estado_animacion = next(estado.generador_animacion)
            
            # Resetear colores
            for n in estado.nodos: n['color'] = cfg.AZUL
            for e in estado.aristas: e['color'] = cfg.NEGRO

            if estado.algoritmo_actual in ['dfs', 'bfs']:
                for label in estado.estado_animacion['visited']:
                    next(n for n in estado.nodos if n['label'] == label)['color'] = cfg.VERDE
                if 'queue' in estado.estado_animacion:
                    for label in estado.estado_animacion['queue']:
                        next(n for n in estado.nodos if n['label'] == label)['color'] = cfg.AMARILLO
                next(n for n in estado.nodos if n['label'] == estado.estado_animacion['current'])['color'] = cfg.ROJO
                estado.recorrido_resultado = estado.estado_animacion.get('recorrido', [])
            
            elif estado.algoritmo_actual == 'kruskal':
                # Colorear aristas en el lienzo principal
                # 1. Poner todas las aristas en gris por defecto
                for e in estado.aristas:
                    e['color'] = cfg.GRIS
                
                # 2. Colorear las aristas del MST en verde
                for u_mst, v_mst in estado.estado_animacion['mst_edges']:
                    arista_mst = next((e for e in estado.aristas if (e['start'] == u_mst and e['end'] == v_mst) or (e['start'] == v_mst and e['end'] == u_mst)), None)
                    if arista_mst:
                        arista_mst['color'] = cfg.VERDE

                # 3. Resaltar la arista actualmente considerada
                if estado.estado_animacion['considered']:
                    u, v = estado.estado_animacion['considered']
                    arista_considerada = next((e for e in estado.aristas if (e['start'] == u and e['end'] == v) or (e['start'] == v and e['end'] == u)), None)
                    if arista_considerada:
                        status = estado.estado_animacion['status']
                        if status == 'rejected':
                            arista_considerada['color'] = cfg.ROJO
                        elif status == 'accepted':
                             arista_considerada['color'] = cfg.VERDE # Ya se colorea arriba, pero por claridad
                        else: # 'considering'
                            arista_considerada['color'] = cfg.AMARILLO
                estado.peso_total_mst = estado.estado_animacion.get('peso_total', 0)
            
            elif estado.algoritmo_actual == 'prim':
                # Colorear nodos y aristas para Prim
                for n in estado.nodos:
                    if n['label'] in estado.estado_animacion['nodes_in_mst']:
                        n['color'] = cfg.VERDE
                    else:
                        n['color'] = cfg.AZUL
                
                for e in estado.aristas:
                    e['color'] = cfg.GRIS

                for u_mst, v_mst in estado.estado_animacion['mst_edges']:
                    arista_mst = next((e for e in estado.aristas if (e['start'] == u_mst and e['end'] == v_mst) or (e['start'] == v_mst and e['end'] == u_mst)), None)
                    if arista_mst:
                        arista_mst['color'] = cfg.VERDE

                if estado.estado_animacion['considered_edge']:
                    u, v = estado.estado_animacion['considered_edge']
                    arista_considerada = next((e for e in estado.aristas if (e['start'] == u and e['end'] == v) or (e['start'] == v and e['end'] == u)), None)
                    if arista_considerada:
                        status = estado.estado_animacion['status']
                        if status == 'rejected':
                            arista_considerada['color'] = cfg.ROJO
                        elif status == 'accepted':
                            arista_considerada['color'] = cfg.VERDE
                        else:
                            arista_considerada['color'] = cfg.AMARILLO
                estado.peso_total_mst = estado.estado_animacion.get('peso_total', 0)


        except StopIteration:
            estado.cambiar_modo('IDLE', "Animación finalizada.")
            # Estado final de Kruskal y Prim: dejar solo el MST en verde
            if estado.algoritmo_actual in ['kruskal', 'prim'] and estado.estado_animacion:
                for e in estado.aristas:
                    e['color'] = cfg.GRIS
                for u, v in estado.estado_animacion['mst_edges']:
                    arista_final = next((e for e in estado.aristas if (e['start']==u and e['end']==v) or (e['start']==v and e['end']==u)), None)
                    if arista_final:
                        arista_final['color'] = cfg.VERDE
                if estado.algoritmo_actual == 'prim':
                    for n in estado.nodos:
                        if n['label'] in estado.estado_animacion['nodes_in_mst']:
                            n['color'] = cfg.VERDE
                estado.peso_total_mst = estado.estado_animacion.get('peso_total', 0)

def bucle_principal():
    estado = EstadoApp()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            
            if estado.modo == 'ANIMATING':
                continue

            if evento.type == pygame.KEYDOWN:
                manejar_eventos_teclado(evento, estado)
            
            if evento.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL]:
                manejar_eventos_mouse(evento, estado)

        if estado.modo == 'ANIMATING':
            procesar_animacion(estado)

        dibujar_elementos(cfg.pantalla, estado, botones)
        cfg.reloj.tick(60)

    pygame.quit()

bucle_principal()
