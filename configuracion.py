import pygame

# Inicialización de Pygame
pygame.init()

# --- 1. Configuración de la Pantalla y Paneles ---
ANCHO_CANVAS = 1120
ANCHO_PANEL_SOLUCION = 400
ANCHO_PANTALLA = ANCHO_CANVAS + ANCHO_PANEL_SOLUCION
ALTO_PANTALLA = 780
ALTO_PANEL_BOTONES = 110
ALTO_CANVAS = ALTO_PANTALLA - ALTO_PANEL_BOTONES

# Configuración de la pantalla principal
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Visualizador Interactivo de Algoritmos de Grafos")

# --- 2. Colores ---
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (200, 200, 200)
GRIS_OSCURO = (60, 60, 60)
AZUL_CLARO = (173, 216, 230)
ROJO = (255, 100, 100)
VERDE = (100, 255, 100)
AZUL = (100, 100, 255)
AMARILLO = (255, 255, 0)
PURPURA = (128, 0, 128)

# --- 3. Fuentes ---
FUENTE_PEQUENA = pygame.font.Font(None, 24)
FUENTE_MEDIANA = pygame.font.Font(None, 32)
FUENTE_GRANDE = pygame.font.Font(None, 40)

# --- 4. Control de Tiempo y Animación ---
reloj = pygame.time.Clock()
VELOCIDAD_ANIMACION_MS = 700

# --- 5. Propiedades del Grafo ---
RADIO_NODO = 20
