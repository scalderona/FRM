# Lab 2 FMR: Primeros pasos de ROS
## Grupo de trabajo con el EV3-2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Nombre 3

## Actividad 1
La práctica consiste en verificar el funcionamiento del modelo de comunicación distribuida de ROS mediante la interacción entre nodos ejecutados en diferentes equipos dentro de una misma red local. Para ello, se utilizan al menos dos computadores: en el primero se ejecuta el nodo turtlesim_node, encargado de simular el entorno gráfico de una tortuga, mientras que en el segundo se publican comandos de velocidad en el tópico `/turtle1/cmd_vel`.

Previo a la ejecución, es necesario configurar adecuadamente las variables de entorno `ROS_MASTER_URI` y `ROS_IP`, con el fin de garantizar la correcta comunicación entre los equipos. Una vez establecida la conexión, desde el segundo computador se envían velocidades lineales y angulares constantes, de manera que la tortuga describa una trayectoria circular, lo que permite evidenciar la relación entre estas variables cinemáticas.

Posteriormente, se evalúa la capacidad de ROS para manejar múltiples nodos dentro de una misma arquitectura distribuida, ejecutando dos instancias de turtlesim y controlando cada una de forma independiente. Con esto, se valida el funcionamiento del sistema en escenarios con múltiples agentes y su correcta gestión de la comunicación entre ellos.

### Solución planteada
La configuración de las variables de entorno `ROS_MASTER_URI` y `ROS_IP` se realizó siguiendo el link guía proporcionado por el monitor. La verificación del correcto funcionamiento de la comunicación se llevó a cabo mediante la ejecución de los nodos de prueba talker (publisher) y listener (subscriber) de ROS, confirmando así el intercambio de mensajes entre equipos.

Una vez verificada la correcta comunicación entre los equipos, se procede a ejecutar dos instancias del simulador turtlesim. Para evitar conflictos entre nodos y tópicos, cada instancia se lanza en un namespace diferente, asignando los nombres sim1 y sim2. Esto se realiza mediante el siguiente comando:

```
rosrun turtlesim turtlesim_node __ns:=sim1 & rosrun turtlesim turtlesim_node __ns:=sim2
```

De esta manera, cada simulación opera de forma independiente dentro de su propio espacio de nombres.

El control de cada tortuga se llevó a cabo desde distintos equipos, publicando comandos de velocidad en los respectivos tópicos asociados a cada namespace. En el computador externo se controló la tortuga correspondiente a `sim1`, mientras que en el computador local se controló la tortuga de `sim2`, como se muestra a continuación:

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

*Computador local:*
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
### Resultados obtenidos

**Imagenes y videos**

## Actividad 2
En esta actividad se propone la creación de un paquete dentro del workspace de ROS, el cual contiene un nodo desarrollado por el estudiante para controlar de manera autónoma el movimiento de la tortuga en turtlesim.

El nodo implementado publica comandos de velocidad en el tópico `/turtle1/cmd_vel` y se suscribe al `tópico /turtle1/pose`, con el fin de obtener la posición y orientación de la tortuga. A partir de esta información, se desarrolla una lógica de control que permite el desplazamiento continuo dentro del entorno, evitando colisiones con los límites de la ventana mediante ajustes automáticos en la trayectoria.

Adicionalmente, se hace uso del servicio `/turtle1/set_pen` para modificar el color del trazo de la tortuga de forma dinámica, en función de su posición dentro del entorno. Esto permite evidenciar la integración de publishers, subscribers y servicios dentro de un mismo nodo en ROS.

### Programa 1
#### Solución planteada
Inicialmente, se define la cabecera del script en Python 3 y se importan las librerías necesarias para la implementación del nodo en ROS. En particular, `rospy` permite la creación y gestión del nodo, `Twist` se utiliza para publicar comandos de velocidad en el tópico `/turtle1/cmd_vel`, Pose permite recibir la posición y orientación de la tortuga desde `/turtle1/pose`, y `SetPen` se emplea para interactuar con el servicio `/turtle1/set_pen`, encargado de modificar las características del trazo.

Se define la clase `Turtle`, dentro de la cual se inicializa el nodo de ROS en el método `__init__` mediante la instrucción `rospy.init_node("Turtle_controller", anonymous=False)`. El parámetro `anonymous=False` permite que el nodo conserve un nombre único y fijo dentro de la red de ROS, facilitando su identificación durante la ejecución.

Se configuran los parámetros ajustables mediante la función `rospy.get_param`, la cual permite definir valores configurables desde el servidor de parámetros de ROS. En este caso, se establecen la frecuencia de ejecución (`~rate_hz`), la velocidad lineal (`~lin_speed`), la velocidad angular (`~ang_speed`), la distancia de reacción frente a los bordes (`~margin`) y la posición en el eje x donde se realiza el cambio de color del trazo (`~x_split`).

Se definen los límites del entorno de simulación mediante los parámetros `x_min`, `x_max`, `y_min` y `y_max`, los cuales delimitan el área de movimiento de la tortuga. En este caso, se toma como referencia el entorno por defecto de `turtlesim`, que generalmente corresponde a una ventana cuadrada de 11 × 11 unidades.

Se inicializan algunas variables de estado del controlador. La variable `self.pose` guarda la posición actual de la tortuga, `self.last_side` registra el último lado de referencia en el eje x, y `self.pen_ready` indica la disponibilidad del servicio para modificar el color del trazo.

Se establece la comunicación con `turtle1` mediante la creación de un publicador y un suscriptor. El publicador se configura sobre el tópico `/turtle1/cmd_vel`, empleando mensajes del tipo `Twist`, con el fin de enviar comandos de velocidad lineal y angular. De manera complementaria, se crea un suscriptor al tópico `/turtle1/pose`, usando mensajes del tipo `Pose`, para recibir de forma continua la posición y orientación actual de la tortuga.

Se hace uso del servicio `/turtle1/set_pen` para controlar el color del trazo. Primero, se verifica la disponibilidad del servicio mediante `rospy.wait_for_service` y luego se crea un cliente con `rospy.ServiceProxy`. Se define la variable `self.pen_ready` para indicar que el servicio está listo para su uso. Además, se implementa la función `set_pen_safe`, la cual permite invocar el servicio de forma segura. Finalmente, se inicializa el color del lápiz en rojo.

Posteriormente, se implementa la función de control del movimiento denominada `control`, la cual constituye el núcleo del comportamiento autónomo del sistema. Esta función inicia verificando que se disponga de información de la pose de la tortuga; en caso contrario, no se ejecuta ninguna acción.

Una vez validada la información, se extraen las coordenadas actuales de la tortuga en los ejes `x` y `y`. A partir de la posición en el eje `x`, se determina el lado del entorno en el que se encuentra la tortuga, utilizando la condición `"L" if x < self.x_split else "R"`, donde `"L"` representa la región izquierda y `"R"` la región derecha.

Con base en esta clasificación, se evalúa si la tortuga ha cruzado la línea vertical de referencia (`x_split`). Si se detecta un cambio de lado respecto al estado anterior, se actualiza el color del trazo mediante el servicio `set_pen_safe: azul` cuando la tortuga se encuentra en la región izquierda y verde cuando se ubica en la región derecha. Finalmente, se actualiza la variable `self.last_side` para registrar la nueva posición relativa.

Posteriormente, se implementa la función `dist_borde`, la cual permite calcular la distancia de la tortuga respecto a los límites del entorno, considerando un margen de seguridad. Esta función no solo determina la cercanía a los bordes, sino que también genera valores positivos mientras la tortuga se encuentra dentro de la zona segura y valores negativos cuando se aproxima o sobrepasa el margen definido. De esta manera, estos indicadores permiten identificar de forma sencilla cuándo es necesario activar la lógica de corrección del movimiento.

Finalmente, se implementa la lógica de control del movimiento de la tortuga. En condiciones normales, el sistema mantiene un desplazamiento en línea recta con velocidad constante. Sin embargo, cuando se detecta cercanía a alguno de los bordes del entorno (es decir, cuando las distancias calculadas toman valores negativos), se activa un comportamiento de evasión.

En esta situación, se reduce la velocidad lineal y se introduce una velocidad angular con el fin de redirigir la trayectoria hacia el interior del entorno. A diferencia de una estrategia determinística, el sentido y la magnitud del giro incorporan un componente aleatorio, escalando la velocidad angular mediante un factor basado en una distribución normal.

Esta variabilidad en el giro evita que la tortuga quede atrapada en trayectorias circulares repetitivas o patrones cíclicos, permitiendo generar cambios de dirección más diversos y favoreciendo la salida efectiva de zonas cercanas a los bordes. De esta manera, el controlador logra un comportamiento más robusto frente a situaciones de confinamiento, manteniendo un movimiento autónomo continuo dentro del entorno de simulación.

#### Diagrama de flujo
#### Resultados obtenidos
#### Código fuente


### Programa 2
#### Solución planteada
#### Diagrama de flujo
#### Resultados obtenidos
#### Código fuente


### Programa 3
#### Solución planteada
#### Diagrama de flujo
#### Resultados obtenidos
#### Código fuente
