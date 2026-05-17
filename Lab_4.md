# Lab 4 FMR: Sensores con ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de esta actividad fue implementar la conexión de un sensor externo a ROS mediante una tarjeta de desarrollo Arduino. Para ello, se realizó el reconocimiento del sensor, la lectura de los datos obtenidos y la creación de un tópico en ROS, a través del cual se publicó la información adquirida para su posterior análisis y comparación con un patrón de referencia.

Debido a que el sensor seleccionado fue una Unidad de Medición Inercial (IMU), el patrón de comparación correspondió a los valores de orientación en yaw proporcionados por la IMU integrada del robot Kobuki. Estos valores fueron obtenidos durante la ejecución de movimientos programados en el robot, con el fin de contrastar las mediciones del sensor externo frente a una referencia conocida.

### Solución planteada
Para la integración del sensor externo se utilizó una Unidad de Medición Inercial MPU6050 conectada a una tarjeta Arduino mediante comunicación I2C. El código implementado en la tarjeta permitió inicializar la comunicación con el sensor, configurar su dirección de operación y leer los registros correspondientes al acelerómetro y giroscopio.

Posteriormente, los datos crudos obtenidos desde el sensor fueron convertidos a unidades físicas. En el caso del acelerómetro, las mediciones fueron expresadas en unidades de gravedad, mientras que las velocidades angulares del giroscopio fueron convertidas a grados por segundo. Adicionalmente, a partir de las componentes de aceleración se calcularon los ángulos de inclinación `roll` y `pitch`.

Para establecer la comunicación entre Arduino y ROS se utilizó la librería `rosserial`, la cual permitió conectar la tarjeta de desarrollo con el ecosistema ROS mediante el puerto serial. De esta manera, la información adquirida por la IMU pudo ser enviada desde Arduino hacia el computador y publicada en un tópico de ROS. En este caso, el patrón utilizado correspondió a los valores de orientación obtenidos por la IMU integrada del robot Kobuki durante la ejecución de movimientos programados.

#### Análisis de Mensajes
La comunicación entre Arduino y ROS se realizó mediante comunicación serial, siguiendo el enfoque propuesto por `rosserial` para la integración de tarjetas de desarrollo dentro del ecosistema ROS. Este procedimiento permitió transmitir la información adquirida por la IMU desde la tarjeta Arduino hacia el computador mediante el puerto serial.

En el código implementado, la tarjeta Arduino realizó la lectura del sensor MPU6050 a través del protocolo I2C. Para ello, se incluyó la librería `Wire`, la cual permite establecer la comunicación con dispositivos I2C, y se definió la dirección del sensor:

```cpp
#include <Wire.h>

const int MPU_ADDR = 0x68;
```

Posteriormente, en la función `setup()` se inicializó la comunicación serial y se configuró el sensor para salir del modo de reposo. Esto permitió que el MPU6050 comenzara a entregar datos desde sus registros internos:

```cpp
void setup() {
  Serial.begin(9600);
  Wire.begin();

  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);
}
```

La adquisición de datos se realizó solicitando la lectura de los registros del sensor a partir de la dirección `0x3B`. Desde este punto se obtuvieron los valores crudos correspondientes al acelerómetro, temperatura y giroscopio:

```cpp
Wire.beginTransmission(MPU_ADDR);
Wire.write(0x3B);
Wire.endTransmission(false);
Wire.requestFrom(MPU_ADDR, 14, true);

AcX = Wire.read() << 8 | Wire.read();
AcY = Wire.read() << 8 | Wire.read();
AcZ = Wire.read() << 8 | Wire.read();
GyX = Wire.read() << 8 | Wire.read();
GyY = Wire.read() << 8 | Wire.read();
GyZ = Wire.read() << 8 | Wire.read();
```

Estos valores crudos fueron convertidos a unidades físicas para facilitar su interpretación. Las aceleraciones se expresaron en unidades de gravedad `g`, mientras que las velocidades angulares se expresaron en grados por segundo:

```cpp
float ax = AcX / 16384.0;
float ay = AcY / 16384.0;
float az = AcZ / 16384.0;

float gx = GyX / 131.0;
float gy = GyY / 131.0;
float gz = GyZ / 131.0;
```

Adicionalmente, a partir de las componentes de aceleración se calcularon los ángulos de inclinación `roll` y `pitch`, los cuales permiten describir parcialmente la orientación del sensor:

```cpp
float roll  = atan2(ay, az) * 180.0 / PI;
float pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;
```

Finalmente, la información adquirida fue enviada mediante instrucciones de impresión serial. Esto permitió que los datos pudieran ser leídos desde ROS y posteriormente publicados en un tópico para su análisis:

```cpp
Serial.print("Ax: ");
Serial.println(ax, 3);

delay(200);
```

La frecuencia de actualización estuvo determinada por el retardo definido en el código mediante `delay(200)`, lo cual equivale aproximadamente a una lectura cada `0.2 s`, es decir, una frecuencia cercana a `5 Hz`.

De acuerdo con las variables leídas y procesadas en el código, la información disponible para el análisis fue la siguiente:

| Variable | Descripción | Unidad |
|---|---|---|
| `AcX` | Valor crudo de aceleración en el eje X | bits |
| `AcY` | Valor crudo de aceleración en el eje Y | bits |
| `AcZ` | Valor crudo de aceleración en el eje Z | bits |
| `GyX` | Valor crudo del giroscopio en el eje X | bits |
| `GyY` | Valor crudo del giroscopio en el eje Y | bits |
| `GyZ` | Valor crudo del giroscopio en el eje Z | bits |
| `ax` | Aceleración convertida en el eje X | g |
| `ay` | Aceleración convertida en el eje Y | g |
| `az` | Aceleración convertida en el eje Z | g |
| `gx` | Velocidad angular en el eje X | °/s |
| `gy` | Velocidad angular en el eje Y | °/s |
| `gz` | Velocidad angular en el eje Z | °/s |
| `roll` | Ángulo de inclinación respecto al eje longitudinal | grados |
| `pitch` | Ángulo de inclinación respecto al eje lateral | grados |

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
