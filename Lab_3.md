# Lab 3 FMR: El poder de ROS
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Actividad 1
El objetivo de la actividad fue preparar el entorno de trabajo y verificar el correcto funcionamiento del robot Kobuki dentro del ecosistema ROS. Inicialmente, se configuró el workspace siguiendo la guía proporcionada. Posteriormente, se ejecutó el nodo principal del robot mediante el comando `roslaunch kobuki_node kobuki_node.launch`.

Una vez iniciado el sistema, se exploraron los tópicos activos en ROS, identificando los mensajes publicados por el robot. Se seleccionó un tópico para analizar la información transmitida y su tipo de mensaje asociado. Asimismo, se identificó el tópico encargado del control de velocidad, desde el cual se enviaron comandos para generar movimiento en el robot. De forma simultánea, se monitoreó el tópico `/odom` con el fin de analizar la estimación de la posición y orientación durante el desplazamiento.

Posteriormente, se evaluó el comportamiento de la odometría, observando que, incluso en trayectorias rectilíneas, se registraron variaciones en las variables reportadas en `/odom`. Estas discrepancias se atribuyeron principalmente a posibles deslizamientos de las ruedas y a limitaciones inherentes en la estimación odométrica, descartando en gran medida errores acumulativos de sensores debido al corto intervalo de operación.

Finalmente, se realizó una prueba de teleoperación mediante control por teclado. Durante esta etapa, se controló manualmente el robot, se observó nuevamente el comportamiento del tópico `/odom` y se analizaron los sensores cliff. Se evidenció que estos sensores detectan si las ruedas presenta contacto con el suelo, determinando diferentes estados según las condiciones en las que pueden estar las ruedas.

Kobuki utiliza dos sensores para estimar su odometría de forma precisa: encoders ubicados en las ruedas para medir la rotación y calcular la distancia recorrida. El sistema calcula la posición (x, y) y la orientación (θ) del robot mediante su modelo de movimiento diferencial. También un giroscopio MEMS de 1 eje integrado para medir la orientación angular.

La odometría puede presentar errores por factores como el deslizamiento de ruedas, irregularidades en el suelo, diferencias de velocidad real en cada rueda o imprecisiones en los encoders. Estos factores provocan desviaciones acumulativas en la estimación de su posición y orientiación.

Los sensores cliff detectan cambios bruscos en la superficie, como bordes o huecos (por ejemplo, escaleras), mediante sensores infrarrojos. Su función es evitar que el robot caiga o sufra daños, deteniendo o modificando su movimiento cuando detectan un peligro.

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

La función `odom_callback(self, msg)` permite procesar la información recibida a través del suscriptor de odometría e incorporarla al estado interno del nodo. En ella, se extraen las componentes cartesianas de la posición del robot en el plano mediante `self.x = msg.pose.pose.position.x` y `self.y = msg.pose.pose.position.y`. Para la orientación, se obtiene el cuaternión asociado con `q = msg.pose.pose.orientation`, a partir del cual se construye el vector `quat = [q.x, q.y, q.z, q.w]` y se realiza la conversión a ángulos de Euler utilizando la función `euler_from_quaternion`, extrayendo específicamente el ángulo de yaw mediante `_, _, self.yaw = euler_from_quaternion(quat)`. Finalmente, se actualiza el estado del sistema estableciendo la variable `odom_ok = True`, indicando que la odometría ha sido recibida correctamente y que el nodo puede continuar con su ejecución. Adicionalmente, en la función se agrego `yaw_deg = math.degrees(self.yaw)` para poder visualizar los ángulos en grados. La función de visualización datos fue `rospy.loginfo_throttle(0.1, "x = %.3f m, y = %.3f m, yaw = %.3f rad (%.2f deg)", self.x, self.y, self.yaw, yaw_deg)`, donde la característica principal es que el 0.1 es cada cuantos segundos se publica el mensaje

La función `publicar_vel(self, v, w)` se encarga de construir y enviar los comandos de velocidad al robot mediante el publicador. Para ello, se crea un mensaje de tipo `Twist`, en el cual la componente lineal se asigna a través de `msg.linear.x`, mientras que la componente angular se define mediante `msg.angular.z`. Finalmente, el mensaje es enviado al tópico correspondiente utilizando la instrucción `self.pub_cmd.publish(msg)`, permitiendo así el control del movimiento del robot. 

La función detener_robot(self) se encarga de detener completamente el movimiento del robot mediante el envío repetido de comandos de velocidad nulos, utilizando la función publicar_vel(0.0, 0.0).

Las funciones `fijar_ref_pos(self)` y `fijar_ref_yaw(self)` se encargan de fijar los valores de referencia para comparar según el recorrido que se este haciendo. Siendo que las funciones que implementan esos valores fijados son: `distancia_recorrida(self)` y `angulo_girado(self)`, donde  el primero determina la distancia con Pitagoras y el segundo con la diferencia entre los ángulos. Adicionalmente, la diferencia entre ángulos se normaliza [- π, π] y se saca el valor absoluto.

La función `esperar_enter(self)` se encarga de mostrar el mensaje “Presiona ENTER una sola vez para iniciar toda la figura…”, finalizando con la declaración de que espera que se presione enter `sys.stdin.readline()`.

##### *Función de control*

La función principal de control se implementa en el método `run(self)`, el cual inicia definiendo una frecuencia de operación de 20 Hz mediante `rospy.Rate(20)`. Posteriormente, se muestra un mensaje indicando que el sistema se encuentra a la espera de la recepción de datos de odometría. Mientras la variable `odom_ok` no sea verdadera, el programa permanece en un bucle de espera controlado por `rate.sleep()`, evitando así que el robot inicie su movimiento sin contar con información válida de posición y orientación.

Una vez se confirma la recepción de la odometría, se notifica en consola y se muestran las dimensiones de la trayectoria a ejecutar, correspondientes a un rectángulo de `largo` y `ancho`. A continuación, el programa espera la interacción del usuario mediante la función `esperar_enter()`, permitiendo iniciar el recorrido de forma controlada.

Al comenzar la ejecución, se inicializa el índice del segmento actual `i_lado = 0`, se fija una referencia inicial de posición mediante `fijar_ref_pos()` y se establece el estado inicial como "AVANZAR". A partir de este punto, el control del movimiento se gestiona mediante una máquina de estados implementada en un ciclo `while`, con tres posibles estados: "AVANZAR", "GIRAR" y "FIN".

En el estado "AVANZAR", se define como objetivo la longitud del segmento actual de la trayectoria, obtenida a partir del arreglo `self.lados`. Se calcula la distancia recorrida mediante la función `distancia_recorrida()`, y mientras esta sea menor que el objetivo, se envían comandos de velocidad lineal constante (`self.vel_lineal`) y velocidad angular nula mediante `publicar_vel(self.vel_lineal, 0.0)`. Una vez alcanzada la distancia objetivo, el robot se detiene utilizando `detener_robot()` y se introduce una pausa de 0.3 segundos con `rospy.sleep(0.3)`. Si el segmento actual corresponde al último lado de la figura, el estado cambia a "FIN"; de lo contrario, se fija una referencia angular con `fijar_ref_yaw()` y se transita al estado "GIRAR".

En el estado "GIRAR", se evalúa el ángulo girado mediante la función `angulo_girado()`. Dado que la trayectoria corresponde a un rectángulo, el giro objetivo es de π/2 radianes. Mientras el ángulo girado sea menor a este valor, el robot rota sobre su eje enviando comandos con velocidad angular constante (`self.vel_angular`) y velocidad lineal nula mediante `publicar_vel(0.0, self.vel_angular)`. Al alcanzar el ángulo deseado, el robot se detiene, se incrementa el índice del lado (`self.i_lado += 1`), se actualiza la referencia de posición con `fijar_ref_pos()` y se retorna al estado "AVANZAR".

Finalmente, en el estado "FIN", se detiene completamente el robot, se muestra un mensaje indicando la finalización de la trayectoria y se termina la ejecución del ciclo principal.

#### Diagrama de flujo comportamiento del robot


Inicialización del nodo ROS y configuración de la suscripción a odometría y publicación de velocidad.
<img width="1588" height="212" alt="image" src="https://github.com/user-attachments/assets/ba04df05-addc-48a4-84a1-ce792787e2b6" />



Espera hasta recibir datos de odometría y confirmación del usuario para iniciar el proceso.
<img width="1820" height="381" alt="image" src="https://github.com/user-attachments/assets/1a63f696-3f53-4ac9-9bc2-bc4595f545e6" />



Definición de la posición inicial, inicialización del contador de lados y establecimiento del estado en AVANZAR.
<img width="1522" height="241" alt="image" src="https://github.com/user-attachments/assets/b1ebe9e0-8546-48f6-9cb0-ff6cd4e8e0b9" />


El robot avanza hasta alcanzar la distancia objetivo correspondiente a un lado del rectángulo.
<img width="1522" height="723" alt="image" src="https://github.com/user-attachments/assets/972b74c5-e15f-49a4-af56-87da79cd4d67" />



Verificación de si el robot ha completado el último lado para decidir si continúa o finaliza.
<img width="1790" height="552" alt="image" src="https://github.com/user-attachments/assets/05e6aee2-e463-42af-aa7d-85a0242cda7d" />



Ejecución del giro de 90°, actualización del contador de lados y preparación para el siguiente movimiento.
<img width="1847" height="285" alt="image" src="https://github.com/user-attachments/assets/5872e36c-eb5d-44f2-8b2e-51128bb26409" />




#### Resultados obtenidos

A continuacion se ve el robot kobuki generando la trayectoria cuadrada

[▶ Ver demo] (https://github.com/scalderona/FRM/blob/main/Varios/WhatsApp%20Video%202026-04-21%20at%208.01.06%20PM.mp4)







#### Código fuente
```
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion


class FiguraKobuki:

    def __init__(self):
        rospy.init_node("figura_kobuki")

        # Parámetros
        self.largo = rospy.get_param("~largo", 1.0)
        self.ancho = rospy.get_param("~ancho", 1.0)
        self.vel_lineal = rospy.get_param("~vel_lineal", 0.10)
        self.vel_angular = rospy.get_param("~vel_angular", 0.35)
        self.odom_topic = rospy.get_param("~odom_topic", "/odom")
        self.cmd_topic = rospy.get_param("~cmd_topic", "/mobile_base/commands/velocity")

        # Publicador y suscriptor
        self.pub_cmd = rospy.Publisher(self.cmd_topic, Twist, queue_size=10)
        self.sub_odom = rospy.Subscriber(self.odom_topic, Odometry, self.odom_callback)

        # Estado actual del robot
        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0
        self.odom_ok = False

        # Referencias para medir avance y giro
        self.x_ref = 0.0
        self.y_ref = 0.0
        self.yaw_ref = 0.0

        # Secuencia del rectángulo
        self.lados = [self.largo, self.ancho, self.largo, self.ancho]
        self.estado = "ESPERAR"
        self.i_lado = 0

        rospy.on_shutdown(self.detener_robot)

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        _, _, self.yaw = euler_from_quaternion(quat)

        self.odom_ok = True

        yaw_deg = math.degrees(self.yaw)
        
        rospy.loginfo_throttle(
            0.1,
            "x = %.3f m, y = %.3f m, yaw = %.3f rad (%.2f deg)",
            self.x, self.y, self.yaw, yaw_deg
        )


    def publicar_vel(self, v, w):
        msg = Twist()
        msg.linear.x = v
        msg.angular.z = w
        self.pub_cmd.publish(msg)

    def detener_robot(self):
        for _ in range(5):
            self.publicar_vel(0.0, 0.0)
            rospy.sleep(0.05)

    def fijar_ref_pos(self):
        self.x_ref = self.x
        self.y_ref = self.y

    def fijar_ref_yaw(self):
        self.yaw_ref = self.yaw

    def distancia_recorrida(self):
        return math.sqrt((self.x - self.x_ref) ** 2 + (self.y - self.y_ref) ** 2)

    def normalizar_angulo(self, ang):
        while ang > math.pi:
            ang -= 2.0 * math.pi
        while ang < -math.pi:
            ang += 2.0 * math.pi
        return ang

    def angulo_girado(self):
        return abs(self.normalizar_angulo(self.yaw - self.yaw_ref))

    def esperar_enter(self):
        print("\nPresiona ENTER una sola vez para iniciar toda la figura...")
        sys.stdin.readline()

    def run(self):
        rate = rospy.Rate(20)

        print("Esperando odometría en:", self.odom_topic)
        while not rospy.is_shutdown() and not self.odom_ok:
            rate.sleep()

        print("Odometría recibida correctamente.")
        print("Figura a recorrer: rectángulo")
        print("Largo =", self.largo, "m")
        print("Ancho =", self.ancho, "m")

        # Un solo Enter y arranca toda la figura
        self.esperar_enter()

        self.i_lado = 0
        self.fijar_ref_pos()
        self.estado = "AVANZAR"

        while not rospy.is_shutdown():

            if self.estado == "AVANZAR":
                objetivo = self.lados[self.i_lado]
                d = self.distancia_recorrida()

                if d < objetivo:
                    self.publicar_vel(self.vel_lineal, 0.0)
                else:
                    self.detener_robot()
                    rospy.sleep(0.3)

                    # Si ya terminó el último lado, finaliza
                    if self.i_lado == len(self.lados) - 1:
                        self.estado = "FIN"
                    else:
                        self.fijar_ref_yaw()
                        self.estado = "GIRAR"

            elif self.estado == "GIRAR":
                ang = self.angulo_girado()

                if ang < math.pi / 2.0:
                    self.publicar_vel(0.0, self.vel_angular)
                else:
                    self.detener_robot()
                    rospy.sleep(0.3)
                    self.i_lado += 1
                    self.fijar_ref_pos()
                    self.estado = "AVANZAR"

            elif self.estado == "FIN":
                self.detener_robot()
                print("Figura completada.")
                break

            rate.sleep()


if __name__ == "__main__":
    try:
        nodo = FiguraKobuki()
        nodo.run()
    except rospy.ROSInterruptException:
        pass
```
