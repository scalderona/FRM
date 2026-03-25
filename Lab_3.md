# Lab 3 FMR: El poder de ROS
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
