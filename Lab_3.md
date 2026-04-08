h# Lab 3 FMR: El poder de ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de la actividad fue preparar el entorno de trabajo y verificar el correcto funcionamiento del robot Kobuki dentro del ecosistema ROS. Inicialmente, se configuró el workspace siguiendo la guía proporcionada. Posteriormente, se ejecutó el nodo principal del robot mediante el comando `roslaunch kobuki_node kobuki_node.launch`.

Una vez iniciado el sistema, se exploraron los tópicos activos en ROS, identificando los mensajes publicados por el robot. Se seleccionó un tópico para analizar la información transmitida y su tipo de mensaje asociado. Asimismo, se identificó el tópico encargado del control de velocidad, desde el cual se enviaron comandos para generar movimiento en el robot. De forma simultánea, se monitoreó el tópico `/odom` con el fin de analizar la estimación de la posición y orientación durante el desplazamiento.

Posteriormente, se evaluó el comportamiento de la odometría, observando que, incluso en trayectorias rectilíneas, se registraron variaciones en las variables reportadas en `/odom`. Estas discrepancias se atribuyeron principalmente a posibles deslizamientos de las ruedas y a limitaciones inherentes en la estimación odométrica, descartando en gran medida errores acumulativos de sensores debido al corto intervalo de operación.

Finalmente, se realizó una prueba de teleoperación mediante control por teclado. Durante esta etapa, se controló manualmente el robot, se observó nuevamente el comportamiento del tópico `/odom` y se analizaron los sensores cliff. Se evidenció que estos sensores detectan si las ruedas presenta contacto con el suelo, determinando diferenes estados según las condiciones en las que pueden estar las ruedas.

### Solución planteada

los topicos presentes en el robot kobuki son los siguientes:

<img width="901" height="862" alt="Captura de pantalla de 2026-03-11 17-27-46" src="https://github.com/user-attachments/assets/daeee78e-852a-44b9-8878-0af0d6979efc" />

uno de los topicos es el `/mobile_base/commands/velocity`, el cual nos permite publicar una velocidad para el robot kobuki, el tipo de mensaje es el siguiente : 

<img width="911" height="103" alt="Captura de pantalla de 2026-03-11 17-30-35" src="https://github.com/user-attachments/assets/a25b8e49-cb97-4c24-b0cb-2dbcb53bfcc0" />

Como se puede observar el tipo de mensaje es `geometry_msg/Twist` el cual tiene la siguiente estructura : 
```text
Vector3 linear 
Vector3 angular
```
Un ejemplo del mensaje que se puede publicar a traves de este topico es : 

`rostopic pub /mobile_base/commands/velocity geometry_msgs/Twist "{linear: {x: 0.1, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"`

Eso publica una velocidad lineal de 0.1 m/s y velocidad angular 0.0.

De forma simultánea, se monitoreó el tópico `/odom`  El mensaje publicado por el topico `/odom` es de la siguiente manera:

<img width="933" height="768" alt="Captura de pantalla de 2026-03-11 17-33-00" src="https://github.com/user-attachments/assets/a2aaa9e8-4502-44fe-9d2a-3c3d970d22e4" />

Finalmente se realizo una prueba con el topico `/mobile-base/events/cliff` el cual al escucharlo nos da la siguiente informacion:

<img width="113" height="623" alt="Captura de pantalla de 2026-03-11 17-50-58" src="https://github.com/user-attachments/assets/ca5a88ae-717b-4659-ab3a-1157512f7c61" />

su tipo de mensaje publicado es `kobuki_msgs/CliffEvent` el cual tiene la siguiente documentacion :

```text
# Provides a cliff sensor event.
# This message is generated whenever a particular cliff sensor signals that the
# robot approaches or moves away from a cliff.
# Note that, despite cliff field on SensorState messages, state field is not a
# bitmask, but the new state of a single sensor.

# cliff sensor
uint8 LEFT   = 0
uint8 CENTER = 1
uint8 RIGHT  = 2

# cliff sensor state
uint8 FLOOR = 0
uint8 CLIFF = 1

uint8 sensor
uint8 state

# distance to floor when cliff was detected
uint16 bottom
```
De manera que la variable sensor nos dice cual `sensor` activo el mensaje 0 si es el izquierdo, 1 si es el del centro y 2 si es el derecho, `state` nos dice si las ruedas se suspendieron, donde 0 nos dice que las ruedas siguen en el piso y 1 si hubo cliff o las ruedas quedaron suspendidas en el aire, por ultimo esta `bottom` que nos dice la distancia hasta el piso.

### Diagrama de Flujo

## Actividad 2
El objetivo de la actividad fue desarrollar un nodo propio en ROS que permitiera controlar el movimiento del robot Kobuki a partir de la información de odometría. En particular, se buscó generar trayectorias geométricas en el entorno, logrando que el robot describiera figuras simples como cuadrados o rectángulos.

Para ello, el nodo se implementó suscribiéndose al tópico `/odom`, con el fin de obtener en tiempo real la posición y orientación del robot. Adicionalmente, se configuró la publicación de comandos de velocidad en el tópico correspondiente al control del robot, permitiendo gobernar su desplazamiento.

A partir de la información de odometría, se estableció una lógica de control que permitió determinar cuándo el robot había recorrido la distancia requerida en cada segmento de la trayectoria y cuándo debía ejecutar giros para cambiar de dirección. De esta forma, se garantizó el seguimiento de la figura geométrica definida.

El programa fue diseñado para recibir como parámetros las dimensiones de la figura (por ejemplo, largo y ancho), lo que permitió generar trayectorias variables según los valores de entrada. Asimismo, se incorporó un mecanismo de interacción inicial, en el cual el nodo permanecía en espera hasta recibir una entrada del usuario antes de iniciar la ejecución de la trayectoria.

En conjunto, la actividad permitió integrar la suscripción a datos sensoriales, la publicación de comandos de control y la implementación de una lógica de navegación basada en odometría, consolidando el desarrollo de un sistema básico de control de movimiento para el robot.
### Programa
#### Solución planteada
Inicialmente, se definió la cabecera del script en Python 3 y se importaron las librerías necesarias para la implementación del nodo en ROS. En Python, se utilizaron las librerías `sys`, para gestionar la entrada desde el teclado, y `math`, para emplear funciones matemáticas como la raíz cuadrada y el valor de π.

En cuanto a ROS, se empleó rospy para la creación y gestión del nodo. El tipo de mensaje Odometry, proveniente de `nav_msgs.msg`, se utilizó para recibir la información de posición y orientación del robot. Por su parte, `Twist`, de `geometry_msgs.msg`, permitió la publicación de comandos de velocidad para el control del movimiento. Finalmente, la función `euler_from_quaternion`, del módulo `tf.transformations`, se utilizó para convertir la orientación del robot desde cuaterniones a ángulos de Euler, facilitando su interpretación y uso en el control.

En cuanto a la creación del nodo, este se implementó dentro de la clase `FiguraKobuki`. La inicialización se realizó en el método `__init__`, mediante la instrucción `rospy.init_node("figura_kobuki")`, con la cual se registra el nodo dentro del ecosistema ROS.

Posteriormente, se definieron los parámetros configurables del sistema, incluyendo el largo y ancho de la trayectoria, la velocidad lineal y angular del robot, así como los tópicos de odometría y de publicación de comandos. Estos parámetros se gestionaron mediante el servidor de parámetros de ROS, lo que permitió ajustar el comportamiento del nodo de manera flexible sin necesidad de modificar el código fuente.

Posteriormente, se definieron los parámetros configurables del sistema, incluyendo el largo y ancho de la trayectoria, la velocidad lineal y angular del robot, así como los tópicos de odometría y de publicación de comandos. Estos parámetros se gestionaron mediante el servidor de parámetros de ROS, lo que permitió modificar el comportamiento del nodo.

A continuación, se implementaron el publicador y el suscriptor. El publicador se configuró sobre el tópico de comandos de velocidad, permitiendo enviar señales de control al robot, mientras que el suscriptor se estableció sobre el tópico de odometría, con el fin de recibir información en tiempo real sobre la posición y orientación del sistema.

Seguidamente, se definieron las variables de estado del robot en el entorno, incluyendo su posición y orientación. Además, se inicializó la variable odom_ok = False, con el propósito de evitar el inicio del movimiento hasta confirmar la correcta recepción de datos de odometría. También se establecieron variables de referencia inicializadas en cero, utilizadas para medir desplazamientos y giros relativos durante la ejecución.

Finalmente, se definió la secuencia de movimiento correspondiente a los lados de la trayectoria a recorrer, junto con las variables de control del estado del sistema y el índice del segmento actual. Adicionalmente, se implementó un mecanismo de apagado seguro del nodo, garantizando la detención del robot al finalizar la ejecución o ante una interrupción.

##### *Funciones de apoyo*

La función `odom_callback(self, msg)` permite procesar la información recibida a través del suscriptor de odometría e incorporarla al estado interno del nodo. En ella, se extraen las componentes cartesianas de la posición del robot en el plano mediante `self.x = msg.pose.pose.position.x` y `self.y = msg.pose.pose.position.y`. Para la orientación, se obtiene el cuaternión asociado con `q = msg.pose.pose.orientation`, a partir del cual se construye el vector `quat = [q.x, q.y, q.z, q.w]` y se realiza la conversión a ángulos de Euler utilizando la función `euler_from_quaternion`, extrayendo específicamente el ángulo de yaw mediante `_, _, self.yaw = euler_from_quaternion(quat)`. Finalmente, se actualiza el estado del sistema estableciendo la variable `odom_ok = True`, indicando que la odometría ha sido recibida correctamente y que el nodo puede continuar con su ejecución. Adicionalmente, para ver

##### *Función de control*
#### Diagrama de flujo comportamiento del robot
#### Resultados obtenidos
#### Código fuente


Inicialización del nodo ROS, espera de la odometría y confirmación del usuario para iniciar la trayectoria.
<img width="1770" height="151" alt="image" src="https://github.com/user-attachments/assets/85b379e3-a207-43a5-9526-86fb20bf31fb" />



El robot avanza en línea recta mientras la distancia recorrida sea menor que la distancia objetivo del lado.
<img width="1010" height="626" alt="image" src="https://github.com/user-attachments/assets/05672c14-fa24-4757-9879-111fba2eefc8" />



El sistema decide si continuar la trayectoria o realizar un giro de 90°, actualizando el estado del recorrido.
<img width="480" height="495" alt="image" src="https://github.com/user-attachments/assets/997fbb57-46ab-4154-ab91-ac3ad443345e" />

<img width="340" height="727" alt="image" src="https://github.com/user-attachments/assets/affe31da-d55e-4d96-b54e-4617c90f8b8a" />



El robot finaliza la trayectoria, se detiene completamente y termina la ejecución del programa.
<img width="1125" height="212" alt="image" src="https://github.com/user-attachments/assets/7386030f-d73f-436f-bd7c-631181f9ef62" />

