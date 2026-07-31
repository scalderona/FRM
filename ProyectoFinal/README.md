Para mas informacion de funcionamiento revisar la siguiente presentacion.
https://canva.link/tbacu6k4ax0a5vr

<img width="1200" height="1600" alt="WhatsApp Image 2026-07-31 at 1 11 23 PM" src="https://github.com/user-attachments/assets/0e966752-b4f4-45f9-80a5-75af0ea87409" />

# Robot EV3 Ackermann con ROS 2 Jazzy

Este proyecto implementa el control, mapeo, localización y navegación autónoma de un robot tipo Ackermann construido sobre una plataforma EV3.

El sistema utiliza:

* ROS 2 Jazzy.
* `slam_toolbox` para construir el mapa.
* `Nav2` y AMCL para localizar y navegar el robot.
* RPLIDAR C1 para medir el entorno.
* BNO08x para obtener información de orientación y movimiento.
* `ros2_laser_scan_matcher` para estimar odometría a partir del LiDAR.
* Un controlador de dirección tipo bicicleta para manejar el robot Ackermann.
* Un puente de velocidad para convertir mensajes `Twist` en `TwistStamped`.

---

## 1. Arquitectura general

El flujo principal del sistema es:

```text
RPLIDAR C1
    |
    v
  /scan
    |
    +----------------------+
    |                      |
    v                      v
Laser Scan Matcher    SLAM Toolbox / AMCL
    |                      |
    v                      v
/odom/laser          Mapa o localización
                           |
                           v
                         Nav2
                           |
                           v
                        /cmd_vel
                           |
                           v
               ev3_cmd_vel_bridge
                           |
                           v
/bicycle_steering_controller/reference
                           |
                           v
                 Controlador Ackermann
                           |
                           v
                         Robot
```

Durante el mapeo, el robot también puede controlarse manualmente mediante `teleop_twist_keyboard`.

---

# 2. Estructura de workspaces

El proyecto utiliza dos workspaces:

```text
~/Proyecto_Final/AckermanEv3/src_aev3
~/ros2_ws
```

El primer workspace contiene principalmente el sistema base del robot Ackermann.

El segundo workspace contiene los paquetes relacionados con:

* SLAM.
* Navegación.
* Configuración de Nav2.
* Parámetros de `slam_toolbox`.
* Drivers y nodos auxiliares.

---

# 3. Compilación del proyecto

## 3.1 Compilar el workspace del robot Ackermann

Abrir una terminal y ejecutar:

```bash
source /opt/ros/jazzy/setup.bash

cd ~/Proyecto_Final/AckermanEv3/src_aev3

rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install
```

Después de compilar:

```bash
source ~/Proyecto_Final/AckermanEv3/src_aev3/install/setup.bash
```

---

## 3.2 Compilar el workspace principal

Primero se debe cargar ROS 2 y el workspace del robot:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Proyecto_Final/AckermanEv3/src_aev3/install/setup.bash
```

Después:

```bash
cd ~/ros2_ws

rosdep install --from-paths src --ignore-src -r -y

colcon build --symlink-install
```

Finalmente:

```bash
source ~/ros2_ws/install/setup.bash
```

---

## 3.3 Orden correcto para cargar los workspaces

En cada terminal nueva se deben ejecutar los siguientes comandos, en este orden:

```bash
source /opt/ros/jazzy/setup.bash
source ~/Proyecto_Final/AckermanEv3/src_aev3/install/setup.bash
source ~/ros2_ws/install/setup.bash
```

El orden es importante porque:

1. Se carga primero la instalación base de ROS 2 Jazzy.
2. Se carga el workspace del controlador Ackermann.
3. Se carga el workspace principal como último overlay.

Opcionalmente, estos comandos pueden agregarse al archivo `~/.bashrc`:

```bash
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc
echo "source ~/Proyecto_Final/AckermanEv3/src_aev3/install/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
```

Después se recarga el archivo:

```bash
source ~/.bashrc
```

---

# 4. Modo de mapeo con SLAM Toolbox

En este modo el robot utiliza el LiDAR para construir un mapa mientras es conducido manualmente.

Se recomienda abrir una terminal diferente para cada proceso.

---

## Terminal 1: iniciar el robot Ackermann

```bash
ros2 launch mi_ackermann_bringup carlikebot.launch.xml
```

Este launch inicia la configuración principal del robot, incluyendo los nodos y controladores necesarios para manejar la plataforma Ackermann.

También debe publicar las transformaciones principales del robot, por ejemplo:

```text
base_link
chassis_link
laser
ruedas
```

---

## Terminal 2: iniciar el RPLIDAR C1

```bash
ros2 launch sllidar_ros2 sllidar_c1_launch.py
```

Este comando inicia el driver del RPLIDAR C1.

El LiDAR debe publicar las mediciones en:

```text
/scan
```

Se puede verificar con:

```bash
ros2 topic echo /scan --once
```

También puede verificarse la frecuencia:

```bash
ros2 topic hz /scan
```

---

## Terminal 3: iniciar la IMU BNO08x

```bash
ros2 run bno08x_driver bno08x_driver
```

Este nodo lee la información de la IMU BNO08x y publica datos relacionados con:

* Orientación.
* Velocidad angular.
* Aceleración lineal.

Para identificar los topics publicados:

```bash
ros2 topic list | grep imu
```

---

## Terminal 4: iniciar la odometría basada en LiDAR

```bash
ros2 run ros2_laser_scan_matcher laser_scan_matcher \
  --ros-args \
  -r scan:=/scan \
  -p base_frame:=base_link \
  -p fixed_frame:=odom \
  -p laser_frame:=laser \
  -p publish_tf:=false \
  -p use_odom:=false \
  -p use_imu:=false \
  -p use_vel:=false \
  -p publish_odom:=/odom/laser
```

Este nodo compara escaneos consecutivos del LiDAR para estimar el movimiento del robot.

Parámetros principales:

| Parámetro                   | Descripción                                        |
| --------------------------- | -------------------------------------------------- |
| `scan:=/scan`               | Utiliza el topic publicado por el RPLIDAR.         |
| `base_frame:=base_link`     | Frame principal del robot.                         |
| `fixed_frame:=odom`         | Frame de referencia para la odometría.             |
| `laser_frame:=laser`        | Frame donde se encuentra instalado el LiDAR.       |
| `publish_tf:=false`         | Evita publicar una transformación TF duplicada.    |
| `use_odom:=false`           | No utiliza odometría previa del robot.             |
| `use_imu:=false`            | No utiliza directamente la IMU en el scan matcher. |
| `use_vel:=false`            | No utiliza una estimación externa de velocidad.    |
| `publish_odom:=/odom/laser` | Publica la estimación de odometría del LiDAR.      |

La odometría generada puede verificarse con:

```bash
ros2 topic echo /odom/laser --once
```

---

## Terminal 5: iniciar SLAM Toolbox

```bash
ros2 launch slam_toolbox online_async_launch.py \
  slam_params_file:=/home/frm/ros2_ws/src/ev3_slam/config/ev3_mapper_params.yaml \
  use_sim_time:=false
```

Este comando inicia `slam_toolbox` en modo asíncrono.

El archivo:

```text
/home/frm/ros2_ws/src/ev3_slam/config/ev3_mapper_params.yaml
```

contiene la configuración del sistema de mapeo, incluyendo parámetros como:

* Frames utilizados.
* Topic del LiDAR.
* Resolución del mapa.
* Frecuencia de actualización.
* Distancia mínima de movimiento.
* Umbrales del scan matcher.
* Configuración del solver de SLAM.

El parámetro:

```text
use_sim_time:=false
```

indica que se utiliza el reloj real del computador y no el reloj de una simulación.

---

## Terminal 6: controlar manualmente el robot

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard \
  --ros-args \
  --remap cmd_vel:=/bicycle_steering_controller/reference \
  -p stamped:=true
```

Este nodo permite conducir el robot utilizando el teclado.

El remapeo:

```text
cmd_vel:=/bicycle_steering_controller/reference
```

envía directamente los comandos de velocidad al controlador Ackermann.

El parámetro:

```text
stamped:=true
```

hace que el nodo publique mensajes de tipo:

```text
geometry_msgs/msg/TwistStamped
```

Esto es necesario porque el controlador de dirección tipo bicicleta recibe comandos con marca de tiempo.

Controles principales del teclado:

```text
u    i    o
j    k    l
m    ,    .
```

Normalmente:

* `i`: avanzar.
* `,`: retroceder.
* `j`: girar hacia la izquierda.
* `l`: girar hacia la derecha.
* `k`: detener el robot.

---

# 5. Guardar el mapa

Cuando el mapa esté completo, se puede guardar con:

```bash
mkdir -p ~/maps
```

Luego:

```bash
ros2 run nav2_map_server map_saver_cli \
  -f $HOME/maps/ev3_lab_final
```

Esto debe generar los archivos:

```text
~/maps/ev3_lab_final.yaml
~/maps/ev3_lab_final.pgm
```

El archivo YAML contiene la configuración del mapa y el archivo PGM contiene la imagen del entorno.

---

# 6. Modo de localización y navegación con Nav2

Para navegar sobre un mapa previamente creado, no se debe ejecutar `slam_toolbox`.

En su lugar, se utilizan:

* El robot Ackermann.
* El LiDAR.
* La odometría.
* AMCL.
* Nav2.
* El puente entre `/cmd_vel` y el controlador Ackermann.

---

## Terminal 1: iniciar el robot Ackermann

```bash
ros2 launch mi_ackermann_bringup carlikebot.launch.xml
```

---

## Terminal 2: iniciar el LiDAR

```bash
ros2 launch sllidar_ros2 sllidar_c1_launch.py
```

---

## Terminal 3: iniciar la IMU

```bash
ros2 run bno08x_driver bno08x_driver
```

---

## Terminal 4: iniciar el Laser Scan Matcher

```bash
ros2 run ros2_laser_scan_matcher laser_scan_matcher \
  --ros-args \
  -r scan:=/scan \
  -p base_frame:=base_link \
  -p fixed_frame:=odom \
  -p laser_frame:=laser \
  -p publish_tf:=false \
  -p use_odom:=false \
  -p use_imu:=false \
  -p use_vel:=false \
  -p publish_odom:=/odom/laser
```

Este nodo proporciona la estimación de movimiento que necesita el sistema de localización.

---

## Terminal 5: iniciar el puente de velocidad

```bash
ros2 run ev3_cmd_vel_bridge twist_to_stamped \
  --ros-args \
  -p input_topic:=/cmd_vel \
  -p output_topic:=/bicycle_steering_controller/reference \
  -p frame_id:=base_link
```

Este nodo convierte los mensajes publicados por Nav2.

Entrada:

```text
/cmd_vel
```

Tipo esperado:

```text
geometry_msgs/msg/Twist
```

Salida:

```text
/bicycle_steering_controller/reference
```

Tipo esperado:

```text
geometry_msgs/msg/TwistStamped
```

El flujo es:

```text
Nav2
  |
  v
/cmd_vel
  |
  v
twist_to_stamped
  |
  v
/bicycle_steering_controller/reference
  |
  v
Controlador Ackermann
```

---

## Terminal 6: iniciar localización con AMCL

```bash
ros2 launch nav2_bringup localization_launch.py \
  map:=$HOME/maps/ev3_lab_final.yaml \
  params_file:=/home/frm/ros2_ws/src/ev3_navigation/config/nav2_params.yaml \
  use_sim_time:=false \
  autostart:=true
```

Este launch inicia principalmente:

* `map_server`.
* AMCL.
* Lifecycle manager de localización.

El mapa utilizado es:

```text
$HOME/maps/ev3_lab_final.yaml
```

El archivo de parámetros de Nav2 es:

```text
/home/frm/ros2_ws/src/ev3_navigation/config/nav2_params.yaml
```

AMCL compara el escaneo actual del LiDAR con el mapa guardado para estimar la posición del robot.

AMCL publica normalmente la transformación:

```text
map → odom
```

Mientras que la odometría del robot debe proporcionar:

```text
odom → base_link
```

El árbol TF esperado es:

```text
map
 └── odom
      └── base_link
           └── laser
```

Después de iniciar AMCL, se debe establecer la posición inicial del robot desde RViz usando:

```text
2D Pose Estimate
```

---

## Terminal 7: iniciar navegación

```bash
ros2 launch nav2_bringup navigation_launch.py \
  params_file:=/home/frm/ros2_ws/src/ev3_navigation/config/nav2_params.yaml \
  use_sim_time:=false \
  autostart:=true \
  use_composition:=false
```

Este launch inicia los componentes de navegación de Nav2, entre ellos:

* Planner server.
* Controller server.
* Behavior server.
* BT navigator.
* Costmaps global y local.
* Smoother server.
* Velocity smoother, si está configurado.

El parámetro:

```text
use_composition:=false
```

ejecuta los nodos de Nav2 como procesos separados, facilitando la visualización, depuración y diagnóstico.

---

# 7. Uso en RViz

Una vez iniciados AMCL y Nav2, abrir RViz:

```bash
rviz2
```

En RViz se recomienda agregar:

* `Map`.
* `LaserScan`.
* `RobotModel`.
* `TF`.
* `PoseWithCovariance`.
* `Path`.
* `Global Costmap`.
* `Local Costmap`.

El frame global debe configurarse como:

```text
map
```

Para localizar inicialmente el robot:

```text
2D Pose Estimate
```

Para enviar una meta de navegación:

```text
Nav2 Goal
```

o:

```text
2D Goal Pose
```

dependiendo de la configuración de RViz.

---

# 8. Topics principales

| Topic                                    | Función                                                |
| ---------------------------------------- | ------------------------------------------------------ |
| `/scan`                                  | Mediciones del RPLIDAR C1.                             |
| `/odom/laser`                            | Odometría estimada mediante Laser Scan Matcher.        |
| `/cmd_vel`                               | Comando de velocidad generado por Nav2.                |
| `/bicycle_steering_controller/reference` | Referencia de velocidad para el controlador Ackermann. |
| `/map`                                   | Mapa de ocupación.                                     |
| `/amcl_pose`                             | Posición estimada por AMCL.                            |
| `/tf`                                    | Transformaciones dinámicas.                            |
| `/tf_static`                             | Transformaciones estáticas.                            |

Para listar todos los topics:

```bash
ros2 topic list
```

---

# 9. Frames principales

| Frame       | Descripción                            |
| ----------- | -------------------------------------- |
| `map`       | Sistema de referencia global del mapa. |
| `odom`      | Referencia local de odometría.         |
| `base_link` | Frame principal del robot.             |
| `laser`     | Frame del RPLIDAR.                     |

El árbol TF puede inspeccionarse con:

```bash
ros2 run tf2_tools view_frames
```

También se puede comprobar una transformación específica:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Para comprobar la localización global:

```bash
ros2 run tf2_ros tf2_echo map base_link
```

---

# 10. Comprobaciones antes de mapear

Antes de iniciar `slam_toolbox`, verificar:

```bash
ros2 topic hz /scan
```

```bash
ros2 topic echo /odom/laser --once
```

```bash
ros2 run tf2_ros tf2_echo base_link laser
```

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

El sistema debe cumplir:

* El LiDAR publica continuamente en `/scan`.
* El frame del LiDAR es `laser`.
* Existe la transformación `base_link → laser`.
* Existe una estimación de movimiento entre `odom` y `base_link`.
* No existen dos nodos publicando simultáneamente la misma transformación TF.

---

# 11. Comprobaciones antes de navegar

Antes de enviar una meta con Nav2, verificar:

```bash
ros2 topic echo /map --once
```

```bash
ros2 topic echo /amcl_pose --once
```

```bash
ros2 run tf2_ros tf2_echo map odom
```

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

```bash
ros2 topic info /cmd_vel
```

```bash
ros2 topic info /bicycle_steering_controller/reference
```

Debe existir la cadena completa:

```text
map → odom → base_link → laser
```

Además:

* Nav2 debe publicar en `/cmd_vel`.
* `twist_to_stamped` debe recibir `/cmd_vel`.
* El puente debe publicar en `/bicycle_steering_controller/reference`.
* El controlador Ackermann debe estar suscrito a ese topic.

---

# 12. Orden resumido de ejecución

## Para hacer un mapa

```text
1. carlikebot.launch.xml
2. sllidar_c1_launch.py
3. bno08x_driver
4. laser_scan_matcher
5. slam_toolbox
6. teleop_twist_keyboard
7. map_saver_cli
```

## Para navegar sobre un mapa

```text
1. carlikebot.launch.xml
2. sllidar_c1_launch.py
3. bno08x_driver
4. laser_scan_matcher
5. twist_to_stamped
6. localization_launch.py
7. navigation_launch.py
8. RViz
9. Establecer 2D Pose Estimate
10. Enviar Nav2 Goal
```

---

# 13. Errores comunes

## No aparece `/scan`

Comprobar que el LiDAR está conectado:

```bash
ls /dev/ttyUSB*
```

Después revisar el nodo:

```bash
ros2 node list
```

Y los topics:

```bash
ros2 topic list | grep scan
```

---

## SLAM Toolbox indica que no puede calcular la pose de odometría

Comprobar:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

También verificar que los nombres configurados en `ev3_mapper_params.yaml` coincidan exactamente con:

```text
odom
base_link
laser
/scan
```

---

## AMCL no localiza el robot

Comprobar que:

* El mapa se cargó correctamente.
* El LiDAR publica `/scan`.
* Existe `base_link → laser`.
* Existe `odom → base_link`.
* Se estableció la pose inicial con `2D Pose Estimate`.
* El mapa coincide con el entorno físico actual.

---

## El robot no recibe los comandos de Nav2

Comprobar la entrada del puente:

```bash
ros2 topic echo /cmd_vel
```

Comprobar la salida:

```bash
ros2 topic echo /bicycle_steering_controller/reference
```

Revisar las conexiones:

```bash
ros2 node info /twist_to_stamped
```

---

## Aparecen saltos o errores en TF

Revisar qué nodos publican transformaciones:

```bash
ros2 topic info /tf --verbose
```

No deben existir dos nodos publicando simultáneamente una misma transformación, especialmente:

```text
odom → base_link
map → odom
```

---

# 14. Rutas utilizadas

Este README utiliza las siguientes rutas:

```text
/home/frm/ros2_ws/src/ev3_slam/config/ev3_mapper_params.yaml
/home/frm/ros2_ws/src/ev3_navigation/config/nav2_params.yaml
/home/frm/maps/ev3_lab_final.yaml
```

Si el proyecto se ejecuta con otro usuario, se deben modificar las rutas absolutas.

Por ejemplo, es preferible reemplazar:

```text
/home/frm/ros2_ws
```

por:

```text
$HOME/ros2_ws
```

Cuando el comando lo permita.

---

# 15. Resumen del funcionamiento

El robot utiliza el RPLIDAR C1 para medir las distancias a los objetos del entorno. El nodo `laser_scan_matcher` compara mediciones consecutivas y estima cuánto se ha desplazado el robot.

Durante el mapeo, `slam_toolbox` combina:

* Las mediciones del LiDAR.
* La estimación de movimiento.
* Las transformaciones TF.

Con esta información construye un mapa de ocupación del entorno.

Durante la navegación, AMCL compara las mediciones actuales del LiDAR con el mapa guardado para estimar la posición del robot. Nav2 utiliza esta posición para calcular una ruta y generar comandos de velocidad.

Como Nav2 publica mensajes `Twist`, pero el controlador Ackermann requiere mensajes `TwistStamped`, el nodo `twist_to_stamped` realiza la conversión y envía las referencias al controlador de dirección tipo bicicleta.

El resultado es un sistema capaz de:

1. Construir un mapa del entorno.
2. Guardar el mapa.
3. Localizar el robot dentro del mapa.
4. Recibir una posición objetivo.
5. Calcular una trayectoria.
6. Conducir el robot Ackermann hasta la meta.
****
