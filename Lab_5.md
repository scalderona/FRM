# Lab 5 FMR: Navegación basada en comportamientos
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Código 1: BUG
### Descripción del Código
### Diagrama de flujo 
### Algoritmo 
### Video de funcionamiento


## Código 2: MAZE
### Descripción del Código
El programa controla el robot LEGO EV3 para recorrer un laberinto siguiendo la **pared izquierda**. Para ello utiliza:

* Dos motores para el desplazamiento.
* Un sensor ultrasónico frontal para detectar obstáculos.
* Un sensor ultrasónico izquierdo para identificar paredes y aberturas.
* Un giroscopio para mantener el movimiento recto y realizar giros de 90°.

El robot mantiene una distancia aproximada de **15 cm** respecto a la pared izquierda mediante un control proporcional. También utiliza el giroscopio para corregir desviaciones durante el avance.

La navegación sigue el siguiente orden de prioridad:

1. Si detecta una pared frontal a menos de 120 mm, gira a la derecha.
2. Si detecta una abertura a la izquierda, avanza, gira a la izquierda e ingresa al nuevo pasillo.
3. Si existe una pared izquierda, la sigue manteniendo la distancia establecida.
4. Si no hay pared izquierda, continúa avanzando recto.

Las detecciones deben repetirse durante varios ciclos para evitar decisiones causadas por ruido en los sensores. El botón inferior permite detener el programa y el botón central muestra las lecturas de los sensores.

### Diagrama de flujo

```mermaid
flowchart TD
    A([Inicio]) --> B[Inicializar motores, sensores y parámetros]
    B --> C[Calibrar giroscopio]
    C --> D[Leer botones y sensores]

    D --> E{¿Botón inferior presionado?}
    E -- Sí --> F[Detener robot]
    F --> G([Fin])

    E -- No --> H{¿Pared frontal confirmada?}
    H -- Sí --> I[Girar 90° a la derecha]
    I --> D

    H -- No --> J{¿Está en el avance inicial?}
    J -- Sí --> K[Avanzar recto con giroscopio]
    K --> D

    J -- No --> L{¿Abertura izquierda confirmada?}
    L -- Sí --> M[Avanzar 160 mm]
    M --> N[Girar 90° a la izquierda]
    N --> O[Avanzar 90 mm]
    O --> D

    L -- No --> P{¿Hay pared izquierda?}
    P -- Sí --> Q[Seguir pared a 150 mm]
    P -- No --> R[Avanzar recto]

    Q --> D
    R --> D
```
### Algoritmo 
### Video de funcionamiento
