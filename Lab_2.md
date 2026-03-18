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
#### Diagrama de flujo
#### Resultados obtenidos
#### Código fuente


### Programa 2
### Programa 3
