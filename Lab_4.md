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

#### Resultados obtenidos

##### Código Arduino - Lectura de IMU MPU6050
```cpp
#include <Wire.h>

const int MPU_ADDR = 0x68;  // Dirección I2C del MPU6050

int16_t AcX, AcY, AcZ, GyX, GyY, GyZ;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Despertar el MPU6050 (sale del modo sleep)
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);   // Registro PWR_MGMT_1
  Wire.write(0);      // Escribe 0 para despertarlo
  Wire.endTransmission(true);

  Serial.println("MPU6050 iniciado correctamente");
}

void loop() {
  // Leer 14 bytes seguidos desde ACCEL_XOUT_H
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

  // Conversión a unidades físicas
  // Acelerómetro en g (configuración por defecto: ±2g)
  float ax = AcX / 16384.0;
  float ay = AcY / 16384.0;
  float az = AcZ / 16384.0;

  // Giroscopio en °/s (configuración por defecto: ±250 °/s)
  float gx = GyX / 131.0;
  float gy = GyY / 131.0;
  float gz = GyZ / 131.0;

  // Temperatura aproximada
  float temperatura = Tmp / 340.0 + 36.53;

  // Cálculo aproximado de ángulos usando acelerómetro
  float roll  = atan2(ay, az) * 180.0 / PI;
  float pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / PI;

  Serial.print("Ax: "); Serial.println(ax, 3);
  //Serial.print(" g\tAy: "); Serial.print(ay, 3);
  //Serial.print(" g\tAz: "); Serial.print(az, 3);

  //Serial.print(" °/s\tGy: "); Serial.print(gy, 2);
  //Serial.print(" °/s\tGz: "); Serial.print(gz, 2);

  //Serial.print(" °/s\tRoll: "); Serial.print(roll, 2);
  //Serial.print(" °\tPitch: "); Serial.print(pitch, 2);

  delay(200);
}
```

##### Viedo con el Kobuki

## Actividad 2
En esta actividad se integró una cámara web al workspace de ROS siguiendo el procedimiento descrito en la guía suministrada. Una vez configurado el dispositivo, se verificó su funcionamiento mediante la herramienta `rqt`, permitiendo visualizar la imagen capturada y validar su correcta incorporación al ecosistema ROS.

### Solución planteada

Para la implementación de la cámara web se utilizó el tópico `/usb_cam/image_raw`, el cual permitió recibir la información visual capturada por el dispositivo dentro del ecosistema ROS. A partir de este tópico, se desarrolló un nodo en Python llamado `image_detector.py`, encargado de suscribirse a la imagen publicada por la cámara y procesarla mediante OpenCV.

El nodo empleó la librería `cv_bridge` para convertir los mensajes de imagen de ROS al formato compatible con OpenCV. De esta manera, cada frame recibido desde la cámara pudo ser procesado para realizar operaciones básicas de visión artificial, como conversión a escala de grises, umbralización, detección de contornos y detección de movimiento mediante sustracción de fondo.

El nodo se inicializó de la siguiente manera:

```python
rospy.init_node('image_detector', anonymous=True)
self.bridge = CvBridge()
rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
```

#### Análisis de Mensajes

El tópico utilizado para recibir la información de la cámara fue `/usb_cam/image_raw`. Este tópico publica mensajes de tipo `sensor_msgs/Image`, los cuales contienen la información visual capturada por la cámara web.

```python
from sensor_msgs.msg import Image
```

El nodo se suscribió al tópico de imagen mediante la siguiente instrucción:

```python
rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)
```

Cada vez que se recibe un mensaje, este es procesado dentro de la función `callback()`. Debido a que ROS maneja la imagen como un mensaje de tipo `sensor_msgs/Image`, fue necesario convertirlo a un formato compatible con OpenCV mediante `cv_bridge`:

```python
frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
```

Una vez realizada la conversión, la imagen fue transformada a escala de grises y posteriormente segmentada mediante un umbral. Esto permitió identificar los contornos presentes en la imagen:

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
```

Luego, los contornos detectados fueron dibujados sobre la imagen original para facilitar su visualización:

```python
frame_contours = frame.copy()
cv2.drawContours(frame_contours, contours, -1, (0, 255, 0), 2)
```

Adicionalmente, se implementó un sustractor de fondo para detectar movimiento en la escena. Esta herramienta permitió generar una máscara que resalta los cambios entre cuadros consecutivos:

```python
self.back_sub = cv2.createBackgroundSubtractorMOG2(
    history=100,
    varThreshold=50,
    detectShadows=True
)
```

La máscara de movimiento fue procesada mediante una operación morfológica de apertura, con el fin de reducir ruido en la imagen:

```python
fg_mask = self.back_sub.apply(frame)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
```

Finalmente, los resultados fueron visualizados mediante ventanas de OpenCV:

```python
cv2.imshow("Contornos en Imagen", frame_contours)
cv2.imshow("Máscara de Movimiento", fg_mask)
cv2.waitKey(1)
```

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
