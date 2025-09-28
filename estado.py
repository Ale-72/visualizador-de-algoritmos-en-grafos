class EstadoApp:
    def __init__(self):
        # --- Estructura de Datos del Grafo ---
        self.nodos = []
        self.aristas = []
        self.contador_nodos = 0

        # --- Estado de la Aplicación ---
        self.modo = 'IDLE'  # Modos: IDLE, ADD_NODE, ADD_EDGE_START, ADD_EDGE_END, MOVE_NODE, GET_WEIGHT, ANIMATING, DELETE_EDGE
        self.texto_estado = "Bienvenido. Selecciona una acción."
        
        # --- Nodos y Aristas Temporales ---
        self.nodo_seleccionado_para_arrastre = None
        self.nodo_inicio_arista_temporal = None
        self.arista_activa_para_peso = None
        self.texto_entrada_peso = ''

        # --- Animación ---
        self.generador_animacion = None
        self.estado_animacion = None
        self.algoritmo_actual = None
        self.ultimo_tiempo_animacion = 0

        # --- Desplazamiento del Panel de Solución ---
        self.scroll_offset_y = 0
        self.altura_total_contenido = 0

        # --- Resultados de Algoritmos ---
        self.recorrido_resultado = []
        self.peso_total_mst = 0

        # --- Algoritmo Pendiente ---
        self.algoritmo_pendiente = None

        # --- Nodo Inicial para Algoritmos ---
        self.nodo_inicial_algoritmo = None

    def reiniciar_grafo(self):
        self.nodos.clear()
        self.aristas.clear()
        self.contador_nodos = 0
        self.estado_animacion = None
        self.algoritmo_actual = None
        self.scroll_offset_y = 0
        self.recorrido_resultado = []
        self.peso_total_mst = 0
        self.nodo_inicial_algoritmo = None
        self.modo = 'IDLE'
        self.texto_estado = "Lienzo limpiado."

    def cambiar_modo(self, nuevo_modo, texto_estado):
        self.modo = nuevo_modo
        self.texto_estado = texto_estado

    def eliminar_ultimo_nodo(self):
        if not self.nodos:
            self.texto_estado = "No hay nodos para eliminar."
            return

        ultimo_nodo = self.nodos.pop()
        self.aristas = [a for a in self.aristas if a['start'] != ultimo_nodo['label'] and a['end'] != ultimo_nodo['label']]
        
        # Ajustar el contador para que el próximo nodo tenga el número correcto
        self.contador_nodos -= 1
        
        self.texto_estado = f"Nodo '{ultimo_nodo['label']}' eliminado."
        self.modo = 'IDLE'
