import json
from tkinter import filedialog, Tk
import pygame
import configuracion as cfg

def guardar_grafo(estado):
    """
    Abre un diálogo para guardar el estado actual del grafo (nodos y aristas)
    en un archivo JSON.
    """
    # Ocultar la ventana principal de Tkinter
    root = Tk()
    root.withdraw()

    # Abrir el diálogo para guardar archivo
    ruta_archivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
        title="Guardar grafo como..."
    )

    if not ruta_archivo:
        estado.texto_estado = "Guardado cancelado."
        return

    # Preparar los datos para guardar
    datos_grafo = {
        "nodos": [],
        "aristas": estado.aristas,
        "contador_nodos": estado.contador_nodos
    }
    # Guardar solo la posición y la etiqueta de los nodos
    for nodo in estado.nodos:
        datos_grafo["nodos"].append({
            "pos": nodo["pos"],
            "label": nodo["label"]
        })

    try:
        with open(ruta_archivo, 'w') as f:
            json.dump(datos_grafo, f, indent=4)
        estado.texto_estado = f"Grafo guardado en {ruta_archivo}"
    except Exception as e:
        estado.texto_estado = f"Error al guardar: {e}"

def cargar_grafo(estado):
    """
    Abre un diálogo para cargar un grafo desde un archivo JSON y actualiza
    el estado de la aplicación.
    """
    # Ocultar la ventana principal de Tkinter
    root = Tk()
    root.withdraw()

    # Abrir el diálogo para seleccionar archivo
    ruta_archivo = filedialog.askopenfilename(
        filetypes=[("Archivos JSON", "*.json"), ("Todos los archivos", "*.*")],
        title="Cargar grafo desde..."
    )

    if not ruta_archivo:
        estado.texto_estado = "Carga cancelada."
        return

    try:
        with open(ruta_archivo, 'r') as f:
            datos_grafo = json.load(f)
        
        # Reiniciar el estado actual antes de cargar
        estado.reiniciar_grafo()

        # Cargar los nuevos datos
        estado.aristas = datos_grafo.get("aristas", [])
        estado.contador_nodos = datos_grafo.get("contador_nodos", 0)
        
        # Reconstruir los nodos con sus rectángulos para la detección de clics
        nodos_cargados = datos_grafo.get("nodos", [])
        for nodo_data in nodos_cargados:
            pos = tuple(nodo_data["pos"])
            label = nodo_data["label"]
            estado.nodos.append({
                'pos': pos,
                'label': label,
                'rect': pygame.Rect(pos[0] - cfg.RADIO_NODO, pos[1] - cfg.RADIO_NODO, cfg.RADIO_NODO * 2, cfg.RADIO_NODO * 2)
            })

        estado.texto_estado = f"Grafo cargado desde {ruta_archivo}"

    except Exception as e:
        estado.texto_estado = f"Error al cargar: {e}"
        # Si hay un error, es mejor limpiar para no dejar un estado inconsistente
        estado.reiniciar_grafo()
