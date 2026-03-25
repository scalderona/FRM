# Lab 2 FMR: Primeros pasos de ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago
## Actividad 1
La práctica consiste en verificar el funcionamiento del modelo de comunicación distribuida de ROS mediante la interacción entre nodos ejecutados en diferentes equipos dentro de una misma red local. Para ello, se utilizan al menos dos computadores: en el primero se ejecuta el nodo turtlesim_node, encargado de simular el entorno gráfico de una tortuga, mientras que en el segundo se publican comandos de velocidad en el tópico `/turtle1/cmd_vel`.

En ROS, la comunicación entre nodos se basa en un modelo peer-to-peer coordinado por un nodo maestro (ROS Master), el cual se encarga de registrar los nodos activos y facilitar la conexión entre publishers y subscribers. Una vez establecida la conexión, el intercambio de mensajes se realiza de forma directa entre nodos, sin pasar nuevamente por el master, lo que mejora la eficiencia del sistema.

Previo a la ejecución, es necesario configurar adecuadamente las variables de entorno `ROS_MASTER_URI` y `ROS_IP`, con el fin de garantizar la correcta comunicación entre los equipos. Una vez establecida la conexión, desde el segundo computador se envían velocidades lineales y angulares constantes, de manera que la tortuga describa una trayectoria circular, lo que permite evidenciar la relación entre estas variables cinemáticas.

Posteriormente, se evalúa la capacidad de ROS para manejar múltiples nodos dentro de una misma arquitectura distribuida, ejecutando dos instancias de turtlesim y controlando cada una de forma independiente. Con esto, se valida el funcionamiento del sistema en escenarios con múltiples agentes y su correcta gestión de la comunicación entre ellos.

### Solución planteada
La configuración de las variables de entorno `ROS_MASTER_URI` y `ROS_IP` se realizó siguiendo el enlace guía proporcionado por el monitor, obteniendo como resultado los siguientes comandos para establecer la comunicación entre los computadores.

*Computador maestro:*
```
export ROS_MASTER_URI=http://192.168.1.10:11311
export ROS_IP=192.168.1.10
```

*Computador externo:*
```
export ROS_MASTER_URI=http://192.168.1.10:11311
export ROS_IP=192.168.1.20
```

La verificación de la comunicación se realizó ejecutando el nodo turtlesim en el computador maestro y el nodo de teleoperación por teclado (teleop key) en el computador externo. Los comandos utilizados se presentan a continuación, y la validación del correcto funcionamiento se evidencia en el primer video adjunto.

*Computador maestro:*
```
rosrun turtlesim turtlesim_node
```

*Computador externo:*
```
rosrun turtlesim turtle_teleop_key
```

Una vez verificada la correcta comunicación entre los equipos, se publicaron mensajes en el topico cmd_vel, el cual tiene la siguiente estructura:

<img width="658" height="207" alt="Captura de pantalla de 2026-03-25 17-42-48" src="https://github.com/user-attachments/assets/0c2008aa-eeb4-4421-be05-f1b0b8b623d1" />

se publico el siguiente mensaje en el computador externo:

```
rostopic pub -r 2 /turtle1/cmd_vel geometry_msgs/Twist "linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: -1.8"
```


Posteriorment se procede a ejecutar dos instancias del simulador turtlesim. Para evitar conflictos entre nodos y tópicos, cada instancia se lanza en un namespace diferente, asignando los nombres sim1 y sim2. Esto se realiza mediante el siguiente comando:

*Computador maestro:*
```
ROS_NAMESPACE=sim1 rosrun turtlesim turtlesim_node __name:=turtlesim
ROS_NAMESPACE=sim2 rosrun turtlesim turtlesim_node __name:=turtlesim
```

De esta manera, cada simulación opera de forma independiente dentro de su propio espacio de nombres.

El control de cada tortuga se llevó a cabo desde distintos equipos, publicando comandos de velocidad en los respectivos tópicos asociados a cada namespace. En el computador externo se controló la tortuga correspondiente a `sim1`, mientras que en el computador local se controló la tortuga de `sim2`, como se muestra a continuación:

*Computador maestro:*
```
rostopic pub -r 2 /sim2/turtle1/cmd_vel geometry_msgs/Twist "linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: -1.8"
```

*Computador externo:*
```
rostopic pub -r 2 /sim1/turtle1/cmd_vel geometry_msgs/Twist "linear:
  x: 2.0
  y: 0.0
  z: 0.0
angular:
  x: 0.0
  y: 0.0
  z: 1.8"
```

### Resultados obtenidos

En el primer caso operando desde un computador externo la tortuga, al enviar el mensaje por el topico se obtuvo el siguiente resultado:

https://github.com/user-attachments/assets/7358d690-6d32-49a8-904d-e6696d4f3662

## Actividad 2
En esta actividad se propone la creación de un paquete dentro del workspace de ROS, el cual contiene un nodo desarrollado por el estudiante para controlar de manera autónoma el movimiento de la tortuga en turtlesim.

El nodo implementado publica comandos de velocidad en el tópico `/turtle1/cmd_vel` y se suscribe al `tópico /turtle1/pose`, con el fin de obtener la posición y orientación de la tortuga. A partir de esta información, se desarrolla una lógica de control que permite el desplazamiento continuo dentro del entorno, evitando colisiones con los límites de la ventana mediante ajustes automáticos en la trayectoria.

Adicionalmente, se hace uso del servicio `/turtle1/set_pen` para modificar el color del trazo de la tortuga de forma dinámica, en función de su posición dentro del entorno. Esto permite evidenciar la integración de publishers, subscribers y servicios dentro de un mismo nodo en ROS.

### Programa
#### Solución planteada
Inicialmente, se define la cabecera del script en Python 3 y se importan las librerías necesarias para la implementación del nodo en ROS. En particular, `rospy` permite la creación y gestión del nodo; `Twist` se utiliza para publicar comandos de velocidad en el tópico `/turtle1/cmd_vel`; `Pose` permite recibir la posición y orientación de la tortuga desde `/turtle1/pose`; y `SetPen` se emplea para interactuar con el servicio `/turtle1/set_pen`, encargado de modificar las características del trazo.

Se define la clase `Turtle`, dentro de la cual se inicializa el nodo de ROS en el método `__init__` mediante la instrucción `rospy.init_node("Turtle_controller", anonymous=False)`. El parámetro `anonymous=False` permite que el nodo conserve un nombre único y fijo dentro de la red de ROS, facilitando su identificación durante la ejecución.

Posteriormente, se configuran los parámetros ajustables mediante la función `rospy.get_param`, la cual permite definir valores desde el servidor de parámetros de ROS. En este caso, se establecen la frecuencia de ejecución (`~rate_hz`), la velocidad lineal en condiciones normales (`~lin_speed_normal`), la velocidad lineal al aproximarse a los bordes (`~lin_speed_borde`), la velocidad angular aplicada cerca de los bordes (`~ang_speed_borde`), la distancia de reacción frente a los bordes (`~margin`) y la posición en el eje `x` donde se realiza el cambio de color del trazo (`~x_split`).

Se definen los límites del entorno de simulación mediante los parámetros `x_min`, `x_max`, `y_min` y `y_max`, los cuales delimitan el área de movimiento de la tortuga. Se toma como referencia el entorno por defecto de `turtlesim`, correspondiente a una ventana cuadrada de aproximadamente 11 × 11 unidades.

A continuación, se inicializan las variables de estado del controlador. La variable `self.pose` almacena la posición actual de la tortuga, `self.color_actual` registra el color del trazo actualmente asignado, y `self.pen_ready` indica la disponibilidad del servicio encargado de modificar el color del trazo.

Se establece la comunicación con `turtle1` mediante la creación de un publicador y un suscriptor. El publicador se configura sobre el tópico `/turtle1/cmd_vel`, utilizando mensajes de tipo `Twist`, con el fin de enviar comandos de velocidad lineal y angular. De manera complementaria, se crea un suscriptor al tópico `/turtle1/pose`, empleando mensajes de tipo `Pose`, para recibir de forma continua la posición y orientación de la tortuga.

Para el control del color del trazo, se utiliza el servicio `/turtle1/set_pen`. Primero, se verifica su disponibilidad mediante `rospy.wait_for_service`, y posteriormente se crea un cliente con `rospy.ServiceProxy`. Se emplea la variable `self.pen_ready` para indicar que el servicio está listo para su uso. Adicionalmente, se implementa la función `set_pen_safe`, la cual permite invocar el servicio de forma segura. Finalmente, se inicializa el color del lápiz en rojo.

##### *Funciones de apoyo*

La función `cerca_borde(self, x, y)` permite identificar si la tortuga se encuentra próxima a alguno de los límites del entorno de simulación. Para ello, compara las coordenadas actuales con los valores mínimos y máximos permitidos en cada eje, considerando una zona de seguridad definida por `self.margin`. Si la posición se encuentra dentro de esta franja cercana a cualquiera de los bordes, la función retorna `True`; en caso contrario, retorna `False`.

La función `actualizar_color(self, x)` se encarga de modificar el color del trazo de la tortuga en función de su posición sobre el eje `x`. Si la tortuga se encuentra a la izquierda del umbral `self.x_split`, el trazo se establece en color rojo; si se encuentra a la derecha o sobre dicho umbral, el color cambia a azul. La actualización solo se realiza cuando se detecta un cambio respecto al estado previo, evitando llamadas innecesarias al servicio `set_pen_safe`. Además, se actualiza la variable `self.color_actual` para registrar el estado vigente.

##### *Función de control*

La función `control(self)` implementa la lógica principal de movimiento de la tortuga. En primer lugar, verifica que la pose actual esté disponible; en caso contrario, la función finaliza sin ejecutar acciones. Luego, extrae las coordenadas actuales `x` y `y`, crea un mensaje de tipo `Twist` e inicializa un movimiento base con velocidad lineal constante (`self.lin_speed_normal`) y velocidad angular nula, generando un desplazamiento rectilíneo.

Posteriormente, si la tortuga se encuentra cerca de alguno de los bordes del entorno, según lo determinado por la función `cerca_borde`, se reduce la velocidad lineal (`self.lin_speed_borde`) y se introduce una velocidad angular distinta de cero (`self.ang_speed_borde`), induciendo un giro que evita la salida del área de trabajo.

Finalmente, se actualiza el color del trazo mediante la función `actualizar_color(x)` y se publica el comando de velocidad en el tópico correspondiente mediante `self.cmd_pub.publish(twist)`.


#### Diagrama de flujo comportamiento del robot
/>

#### Resultados obtenidos
#### Código fuente
