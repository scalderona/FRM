# Lab 4 FMR: Sensores con ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de esta actividad fue implementar la conexión de un sensor serial mediante una tarjeta de desarrollo Arduino. Posteriormente, se realizó el reconocimiento y lectura de datos, así como la creación de un tópico en ROS para publicar la información obtenida y compararla con un patrón de referencia.

Debido a que el sensor seleccionado fue una Unidad de Medición Inercial (IMU), el patrón de comparación correspondió a los valores de yaw proporcionados por la IMU del robot Kobuki, obtenidos a partir de la ejecución de movimientos programados en el robot.

### Solución planteada

#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 2
En esta actividad se realizó la integración de una cámara web al workspace de ROS. Para ello, se siguió el procedimiento descrito en la guía suministrada, permitiendo la implementación y visualización de la cámara mediante la herramienta `rqt`.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 3
El objetivo de esta actividad fue realizar el reconocimiento y adquisición de datos del sensor RPLIDAR C1 utilizando la librería `rplidar_ros`. Para ello, se descargó y ejecutó el paquete mediante el comando `roslaunch rplidar_ros rplidar_c1.launch`, verificando posteriormente el reconocimiento de los tópicos y la información suministrada por el sensor.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 4
Una vez completada la actividad 3, se construyó un laberinto con el fin de contrastar las mediciones generadas por el LIDAR con dimensiones reales del entorno. Para ello, se ubicó un elemento de referencia dentro del laberinto y se extrajeron los datos obtenidos por el sensor, aplicando posteriormente una transformación a coordenadas cartesianas para su análisis.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos
#### Código fuente

## Actividad 5
Una vez completada la actividad 3 y realizada la investigación correspondiente para responder las preguntas de la guía, se construyó un nuevo laberinto con el propósito de implementar el paquete `hector_slam` y llevar a cabo el proceso de mapeo del entorno.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos
#### Código fuente
