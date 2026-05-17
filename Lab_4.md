# Lab 4 FMR: Sensores con ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de esta actividad fue implementar la conexión de un sensor externo a ROS mediante una tarjeta de desarrollo Arduino. Para ello, se realizó el reconocimiento del sensor, la lectura de los datos obtenidos y la creación de un tópico en ROS, a través del cual se publicó la información adquirida para su posterior análisis y comparación con un patrón de referencia.

Debido a que el sensor seleccionado fue una Unidad de Medición Inercial (IMU), el patrón de comparación correspondió a los valores de orientación en yaw proporcionados por la IMU integrada del robot Kobuki. Estos valores fueron obtenidos durante la ejecución de movimientos programados en el robot, con el fin de contrastar las mediciones del sensor externo frente a una referencia conocida.

### Solución planteada
Se realizó la instalación de la libreria `rosserial` ya que este permite la comunicación entre el Arduino y el entorno ROS

#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 2
En esta actividad se integró una cámara web al workspace de ROS siguiendo el procedimiento descrito en la guía suministrada. Una vez configurado el dispositivo, se verificó su funcionamiento mediante la herramienta `rqt`, permitiendo visualizar la imagen capturada y validar su correcta incorporación al ecosistema ROS.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 3
El objetivo de esta actividad fue realizar el reconocimiento y la adquisición de datos del sensor RPLIDAR C1 mediante el paquete `rplidar_ros`. Para ello, se descargó y configuró la librería correspondiente en el workspace de ROS y posteriormente se ejecutó el nodo del sensor mediante el comando `roslaunch rplidar_ros rplidar_c1.launch`.

Una vez iniciado el nodo, se verificó el reconocimiento del dispositivo, la publicación de los tópicos asociados y la información suministrada por el sensor. Además, se revisó el tipo de mensaje generado, con el fin de identificar la estructura de los datos entregados por el RPLIDAR para su posterior procesamiento.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos

## Actividad 4
Una vez completada la configuración del RPLIDAR C1, se construyó un laberinto como entorno controlado para contrastar las mediciones generadas por el sensor con las dimensiones reales del escenario. Para ello, se ubicó un elemento de referencia dentro del laberinto, se extrajeron los datos crudos del LIDAR y se transformaron a coordenadas cartesianas para su posterior análisis y comparación con las medidas reales.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos
#### Código fuente

## Actividad 5
Una vez completada la configuración del RPLIDAR C1 y realizada la investigación sobre el paquete `hector_slam`, se construyó un nuevo laberinto para implementar el proceso de mapeo del entorno en ROS. Esta actividad permitió analizar el funcionamiento del paquete, su uso de la información del LIDAR y la generación de un mapa del escenario de prueba.

### Solución planteada
#### Análisis de Mensajes
#### Resultados obtenidos
#### Código fuente
