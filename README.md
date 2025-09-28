# 📊 Visualizador Interactivo de Algoritmos de Grafos

**Un entorno de escritorio potente y educativo para la creación, manipulación y visualización paso a paso de los algoritmos de grafos más importantes.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.5.2-green?style=for-the-badge&logo=pygame)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

---

![Demostración del Proyecto](demo.gif)

## 📜 Sobre el Proyecto

Este proyecto nace como una herramienta de aprendizaje interactiva para todos aquellos interesados en la teoría de grafos y la algoritmia. En lugar de solo leer teoría, esta aplicación permite **ver y experimentar** cómo los algoritmos recorren, analizan y transforman las estructuras de un grafo en tiempo real, facilitando la comprensión de conceptos que a menudo son abstractos.

La interfaz está diseñada para ser intuitiva, permitiendo a los usuarios enfocarse en la lógica del algoritmo en lugar de en la complejidad de la herramienta.

## ✨ Características Principales

* **🎨 Lienzo Interactivo:** Dibuja tus propios grafos directamente sobre un lienzo.
    * **🖱️ Gestión Dinámica:** Añade, elimina y arrastra nodos con total libertad.
    * **↔️ Aristas con Peso:** Conecta nodos asignando pesos numéricos a las aristas, esencial para algoritmos como Kruskal y Prim.
* **🧠 Visualización Detallada de Algoritmos:** Observa la ejecución de los algoritmos paso a paso, con un código de colores que resalta los nodos visitados, las aristas consideradas y el estado actual.
* **📊 Panel de Solución Dinámico:** Un panel lateral muestra información clave en tiempo real durante la ejecución de un algoritmo, como el recorrido, la cola de prioridad o las aristas del Árbol de Expansión Mínima (MST).
* **💾 Persistencia de Datos:** ¿Creaste un grafo complejo? ¡No lo pierdas! Guarda tu trabajo en un archivo `.json` y cárgalo más tarde para seguir donde lo dejaste.
* **🚀 Arquitectura Modular:** El código está organizado de forma limpia y desacoplada, separando la lógica, el estado, el dibujo y la interfaz, siguiendo las mejores prácticas de desarrollo.

## 🤖 Algoritmos Incluidos

El visualizador actualmente soporta la animación de los siguientes algoritmos:

| Algoritmo | Tipo | Descripción Breve |
| :--- | :--- | :--- |
| **Búsqueda en Profundidad (DFS)** | Recorrido | Explora tan profundo como sea posible a lo largo de cada rama antes de retroceder. |
| **Búsqueda en Anchura (BFS)** | Recorrido | Explora todos los vecinos de un nodo antes de moverse a los nodos del siguiente nivel. |
| **Algoritmo de Kruskal** | Árbol de Expansión Mínima | Construye un MST seleccionando las aristas de menor peso que no formen ciclos. |
| **Algoritmo de Prim** | Árbol de Expansión Mínima | Construye un MST expandiendo un único árbol a partir de un nodo inicial. |

## 🛠️ Tecnologías Utilizadas

Este proyecto fue construido utilizando un conjunto de tecnologías robustas y ampliamente reconocidas en el ecosistema de Python.

| Tecnología | Propósito |
| :--- | :--- |
| **Python** | Lenguaje principal de desarrollo. |
| **Pygame** | Biblioteca para la creación de la interfaz gráfica, el lienzo y la gestión de eventos. |
| **NetworkX** | Utilizado internamente para la lógica y la representación de grafos de los algoritmos. |
| **Tkinter** | Empleado para generar los diálogos nativos de "Guardar" y "Cargar" archivos. |

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local.

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/graph-algorithm-visualizer.git](https://github.com/TU_USUARIO/graph-algorithm-visualizer.git)
    cd graph-algorithm-visualizer
    ```
    2.  **Crea y activa un entorno virtual (muy recomendado):**
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activarlo (en Windows)
    venv\Scripts\activate

    # Activarlo (en macOS/Linux)
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    El archivo `requirements.txt` contiene todo lo necesario.
    ```bash
    pip install -r requirements.txt
    ```

4.  **¡Ejecuta la aplicación!**
    ```bash
    python main.py
    ```

## 🕹️ Modo de Uso

1.  **Panel de Botones (Superior):** Utiliza los botones para cambiar entre modos: `Añadir Nodo`, `Añadir Arista`, `Mover Nodo`, etc.
2.  **Lienzo Principal (Izquierda):** Haz clic en el lienzo para realizar la acción seleccionada (crear un nodo, seleccionar el inicio de una arista, etc.).
3.  **Selección de Algoritmo:** Elige un algoritmo (ej. `DFS`, `Kruskal`). Si el algoritmo lo requiere, la aplicación te pedirá que selecciones un nodo de inicio.
4.  **Panel de Solución (Derecha):** Observa cómo el panel se actualiza en cada paso de la animación, mostrando información relevante sobre el estado del algoritmo.
5.  **Guardar/Cargar:** Usa los botones correspondientes para guardar tu grafo.