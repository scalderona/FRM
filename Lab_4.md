# Lab 4 FMR: Sensores con ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de esta actividad fue implementar la conexión de un sensor externo a ROS mediante una tarjeta de desarrollo Arduino. Para ello, se implementó un programa en Arduino para adquirir la velocidad angular del eje z desde el sensor MPU6050 integrado en el módulo GY-87. La comunicación con el sensor se realizó mediante protocolo I2C, utilizando la librería Wire.h y la dirección 0x68. Durante la inicialización, se escribió el valor 0x00 en el registro 0x6B para sacar al sensor del modo de suspensión. Posteriormente, en cada iteración del ciclo principal, se leyeron los dos bytes correspondientes al registro GYRO_ZOUT_H, reconstruyendo así la medición cruda de 16 bits del giroscopio en z. Esta señal se convirtió primero a grados por segundo usando la sensibilidad por defecto del MPU6050 (131 LSB/(∘/s)), y luego a radianes por segundo para adecuarla al formato utilizado en ROS. Finalmente, el dato se publicó en el tópico /gz mediante rosserial, usando un mensaje de tipo std_msgs/Float32 con una frecuencia aproximada de 20 Hz.

Debido a que el sensor seleccionado fue una Unidad de Medición Inercial (IMU), el patrón de comparación correspondió a los valores de velocidad angular proporcionados por la IMU integrada del robot Kobuki. Estos valores fueron obtenidos durante la ejecución de movimientos programados en el robot, con el fin de contrastar las mediciones del sensor externo frente a una referencia conocida.

### Solución planteada
Para la integración del sensor externo se utilizó una Unidad de Medición Inercial MPU6050 conectada a una tarjeta Arduino mediante comunicación I2C. El código implementado en la tarjeta permitió inicializar la comunicación con el sensor, configurar su dirección de operación y leer los registros correspondientes al acelerómetro y giroscopio.

Posteriormente, los datos crudos obtenidos desde el sensor fueron convertidos a unidades físicas. En este caso para que las medidas de la IMU MPU6050 y la del kobuki tuvieran las mismas unidades se pasaron a radianes por segundo.

Para establecer la comunicación entre Arduino y ROS se utilizó la librería `rosserial`, la cual permitió conectar la tarjeta de desarrollo con el ecosistema ROS mediante el puerto serial. De esta manera, la información adquirida por la IMU pudo ser enviada desde Arduino hacia el computador y publicada en un tópico de ROS. En este caso, el patrón utilizado correspondió a los valores de velocidad angular obtenidos por la IMU integrada del robot Kobuki.

La prueba fue muy sencilla se utilizo el topico del kobuki `/mobile_base/commands/velocity`, en el se publico el siguiente mensaje : 

`rostopic pub -r 10 /mobile_base/commands/velocity geometry_msgs/Twist \
'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.4}}'`

Esto generaba una velocidad angular de 0.4 radianes por segundo, con el comando 

`rostopic echo /mobile_base/sensors/imu_data/angular_velocity/z`

Se obtuvo la velocidad angular con la imu del kobuki y con el comando: 

`rostopic echo /gz`

Se obtuvo la velocidad angular con la imu conectada a arduino.

#### Resultados obtenidos

El terminal que mostraba los datos obtenidos por la imu de arduino eran los siguientes:

<img width="814" height="971" alt="Captura de pantalla de 2026-04-15 17-59-12" src="https://github.com/user-attachments/assets/d7467174-6a2d-460d-be85-a39cba4c7b8f" />

Los resultads obtenidos por el kobuki nos daba un valor muy cercano a 0.4 rad/s, mientras que los tomados por la imu tenian una variacion entre 0.38 y 0.43 demostrando las diferencias entre los sensores, estas pueden ser debidas a que el sensor estaba sobre una protoboard encima del robot, el cual como se ve en el video no tenia un movimiento constante sino que tenia ciertas iercias al arranque de las ruedas lo que derivo en errores en la imu conectada al arduino sin embargo el objetivo de realizar la conexion de sensores mediante arduino se logro satisfactoriamente.


##### Código Arduino - Lectura de IMU MPU6050
```cpp
#include <Wire.h>
#include <ros.h>
#include <std_msgs/Float32.h>

const uint8_t MPU_ADDR = 0x68;

// Al menos 1 subscriber y 1 publisher
typedef ros::NodeHandle_<ArduinoHardware, 1, 1, 96, 96> NodeHandle;
NodeHandle nh;

std_msgs::Float32 gz_msg;
ros::Publisher pub_gz("gz", &gz_msg);

void writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(reg);
  Wire.write(value);
  Wire.endTransmission();
}

bool readGyroZ(float &gz_rad_s) {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x47);   // GYRO_ZOUT_H
  if (Wire.endTransmission(false) != 0) return false;

  Wire.requestFrom(MPU_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return false;

  int16_t raw = (Wire.read() << 8) | Wire.read();

  float gz_deg_s = raw / 131.0;          // ±250 deg/s
  gz_rad_s = gz_deg_s * PI / 180.0;      // rad/s
  return true;
}

void setup() {
  Wire.begin();

  // Despertar MPU6050
  writeRegister(0x6B, 0x00);

  nh.getHardware()->setBaud(57600);
  nh.initNode();
  nh.advertise(pub_gz);
}

void loop() {
  float gz;
  if (readGyroZ(gz)) {
    gz_msg.data = gz;
    pub_gz.publish(&gz_msg);
  }

  nh.spinOnce();
  delay(50);   // ~20 Hz
}

```
##### Viedo con el Kobuki

https://github.com/user-attachments/assets/e7307927-239c-469a-bf8c-8f208bb38310


## Actividad 2
En esta actividad se integró una cámara web al workspace de ROS siguiendo el procedimiento descrito en la guía suministrada. Una vez configurado el dispositivo, se verificó su funcionamiento mediante la herramienta `rqt`, permitiendo visualizar la imagen capturada y validar su correcta incorporación al ecosistema ROS.

### Solución planteada

Para la implementación de la cámara web se utilizó el tópico `/usb_cam/image_raw`, el cual permitió recibir la información visual capturada por el dispositivo. A partir de este tópico, se desarrolló un nodo en Python llamado `image_detector.py`, encargado de suscribirse a la imagen publicada por la cámara y procesarla mediante OpenCV.

El nodo empleó la librería `cv_bridge` para convertir los mensajes de imagen de ROS al formato compatible con OpenCV.

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

##### Codígo

```python
#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageDetector:
    def __init__(self):
        rospy.init_node('image_detector', anonymous=True)
        self.bridge = CvBridge()
        rospy.Subscriber("/usb_cam/image_raw", Image, self.callback)

        # Sustractor de fondo para detectar movimiento
        self.back_sub = cv2.createBackgroundSubtractorMOG2(
            history=100,
            varThreshold=50,
            detectShadows=True
        )

        rospy.loginfo("Nodo de detección de imagen con contornos y movimiento iniciado.")
        rospy.spin()

    def callback(self, msg):
        try:
            # Convertir mensaje a imagen OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            # Detección de contornos en escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(
                thresh,
                cv2.RETR_TREE,
                cv2.CHAIN_APPROX_SIMPLE
            )

            # Dibujar contornos sobre la imagen original
            frame_contours = frame.copy()
            cv2.drawContours(frame_contours, contours, -1, (0, 255, 0), 2)

            # Generar máscara de movimiento
            fg_mask = self.back_sub.apply(frame)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)

            # Mostrar resultados
            cv2.imshow("Contornos en Imagen", frame_contours)
            cv2.imshow("Máscara de Movimiento", fg_mask)
            cv2.waitKey(1)

        except Exception as e:
            rospy.logerr("Error procesando la imagen: %s", str(e))

if __name__ == "__main__":
    try:
        ImageDetector()
    except rospy.ROSInterruptException:
        pass
```
##### Captura de pantalla con la imagen de la cámara

<img width="1812" height="1036" alt="Captura de pantalla de 2026-04-22 16-46-39" src="https://github.com/user-attachments/assets/9fb94f72-96ad-436e-80bf-574d4036923c" />


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
