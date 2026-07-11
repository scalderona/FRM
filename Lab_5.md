# Lab 5 FMR: Navegación basada en comportamientos
## Grupo de trabajo 2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón\
Mateo Concha Buitrago

## Código 1: BUG
### Descripción del Código
### Diagrama de flujo 
### Código
### Video de funcionamiento


## Código 2: MAZE
### Descripción del Código
El programa controla el robot LEGO EV3 para recorrer un laberinto siguiendo la **pared izquierda**. Para ello utiliza:

* Dos motores para el desplazamiento.
* Un sensor ultrasónico frontal para detectar obstáculos.
* Un sensor ultrasónico izquierdo para identificar paredes y aberturas.
* Un giroscopio para mantener el movimiento recto y realizar giros de 90°.

El robot mantiene una distancia aproximada de **15 cm** respecto a la pared izquierda mediante un control proporcional. También utiliza el giroscopio para corregir desviaciones durante el avance.

La navegación sigue el siguiente orden de prioridad:

1. Si detecta una pared frontal a menos de 120 mm, gira a la derecha.
2. Si detecta una abertura a la izquierda, avanza, gira a la izquierda e ingresa al nuevo pasillo.
3. Si existe una pared izquierda, la sigue manteniendo la distancia establecida.
4. Si no hay pared izquierda, continúa avanzando recto.

Las detecciones deben repetirse durante varios ciclos para evitar decisiones causadas por ruido en los sensores. El botón inferior permite detener el programa y el botón central muestra las lecturas de los sensores.

### Diagrama de flujo

```mermaid
flowchart TD
    A([Inicio]) --> B[Inicializar motores, sensores y parámetros]
    B --> C[Calibrar giroscopio]
    C --> D[Leer botones y sensores]

    D --> E{¿Botón inferior presionado?}
    E -- Sí --> F[Detener robot]
    F --> G([Fin])

    E -- No --> H{¿Pared frontal confirmada?}
    H -- Sí --> I[Girar 90° a la derecha]
    I --> D

    H -- No --> J{¿Está en el avance inicial?}
    J -- Sí --> K[Avanzar recto con giroscopio]
    K --> D

    J -- No --> L{¿Abertura izquierda confirmada?}
    L -- Sí --> M[Avanzar 160 mm]
    M --> N[Girar 90° a la izquierda]
    N --> O[Avanzar 90 mm]
    O --> D

    L -- No --> P{¿Hay pared izquierda?}
    P -- Sí --> Q[Seguir pared a 150 mm]
    P -- No --> R[Avanzar recto]

    Q --> D
    R --> D
```
### Código

```python
#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Stop, Button
from pybricks.tools import wait, StopWatch

ev3 = EV3Brick()

motor_izq = Motor(Port.A)
motor_der = Motor(Port.B)

ultra_frontal = UltrasonicSensor(Port.S1)
ultra_izquierdo = UltrasonicSensor(Port.S2)
sensor_gyro = GyroSensor(Port.S3)

reloj = StopWatch()

Ts = 20

sentido_motores = 1
sentido_giro = 1

distancia_objetivo_izq = 150
umbral_frente_pared = 120
umbral_izquierda_abierta = 320
zona_muerta_pared = 30

velocidad_base = 250
velocidad_min = 150
velocidad_max = 300

velocidad_giro_min = 130
velocidad_giro_max = 250

Kp_gyro = 2.0
Kp_pared = 1.0
Kp_giro = 3.6

correccion_gyro_max = 25
correccion_pared_max = 10
correccion_total_max = 30

signo_gyro = -1
signo_pared = 1

tolerancia_giro = 2

diametro_rueda = 56
PI = 3.1416

distancia_antes_giro_izq = 160
distancia_entrada = 90

conteo_frente = 0
conteo_frente_necesario = 5

conteo_apertura = 0
conteo_apertura_necesario = 8

tiempo_inicio_recto = 1800
tiempo_ignorar_apertura = 800

tiempo_ultimo_giro = 0
tiempo_inicio = 0

ya_encontro_pared_izq = False
angulo_referencia = 0


def limitar(valor, minimo, maximo):
    if valor > maximo:
        return maximo

    if valor < minimo:
        return minimo

    return valor


def detener_robot():
    motor_izq.stop(Stop.BRAKE)
    motor_der.stop(Stop.BRAKE)


def mover_motores(vel_izq, vel_der):
    motor_izq.run(sentido_motores * vel_izq)
    motor_der.run(sentido_motores * vel_der)


def leer_distancia(sensor):
    distancia = sensor.distance()

    if distancia > 1000:
        distancia = 1000

    return distancia


def actualizar_referencia():
    global angulo_referencia
    angulo_referencia = sensor_gyro.angle()


def distancia_recorrida_mm():
    angulo_izq = abs(motor_izq.angle())
    angulo_der = abs(motor_der.angle())

    angulo_promedio = (angulo_izq + angulo_der) / 2

    return (angulo_promedio / 360) * PI * diametro_rueda


def avanzar_recto():
    angulo_actual = sensor_gyro.angle()
    error_gyro = angulo_referencia - angulo_actual

    correccion_gyro = Kp_gyro * error_gyro
    correccion_gyro = limitar(
        correccion_gyro,
        -correccion_gyro_max,
        correccion_gyro_max
    )

    vel_izq = velocidad_base - signo_gyro * correccion_gyro
    vel_der = velocidad_base + signo_gyro * correccion_gyro

    vel_izq = limitar(vel_izq, velocidad_min, velocidad_max)
    vel_der = limitar(vel_der, velocidad_min, velocidad_max)

    mover_motores(vel_izq, vel_der)


def seguir_pared_izquierda(distancia_izq):
    angulo_actual = sensor_gyro.angle()

    error_gyro = angulo_referencia - angulo_actual
    correccion_gyro = Kp_gyro * error_gyro
    correccion_gyro = limitar(
        correccion_gyro,
        -correccion_gyro_max,
        correccion_gyro_max
    )

    error_pared = distancia_izq - distancia_objetivo_izq

    if abs(error_pared) < zona_muerta_pared:
        error_pared = 0

    correccion_pared = Kp_pared * error_pared
    correccion_pared = limitar(
        correccion_pared,
        -correccion_pared_max,
        correccion_pared_max
    )

    correccion_total = (
        signo_gyro * correccion_gyro
        + signo_pared * correccion_pared
    )

    correccion_total = limitar(
        correccion_total,
        -correccion_total_max,
        correccion_total_max
    )

    vel_izq = velocidad_base - correccion_total
    vel_der = velocidad_base + correccion_total

    vel_izq = limitar(vel_izq, velocidad_min, velocidad_max)
    vel_der = limitar(vel_der, velocidad_min, velocidad_max)

    mover_motores(vel_izq, vel_der)


def avanzar_distancia(distancia_objetivo):
    motor_izq.reset_angle(0)
    motor_der.reset_angle(0)

    actualizar_referencia()

    while distancia_recorrida_mm() < distancia_objetivo:
        distancia_frente = leer_distancia(ultra_frontal)

        if distancia_frente < umbral_frente_pared:
            detener_robot()
            return

        avanzar_recto()
        wait(Ts)

    detener_robot()
    wait(100)


def girar_gyro(angulo_objetivo):
    global tiempo_ultimo_giro

    detener_robot()
    wait(150)

    sensor_gyro.reset_angle(0)
    wait(150)

    print("Girando:", angulo_objetivo)

    while True:
        angulo_actual = sensor_gyro.angle()
        error = angulo_objetivo - angulo_actual

        if abs(error) <= tolerancia_giro:
            break

        salida = Kp_giro * error
        salida = limitar(
            salida,
            -velocidad_giro_max,
            velocidad_giro_max
        )

        if 0 < salida < velocidad_giro_min:
            salida = velocidad_giro_min

        if -velocidad_giro_min < salida < 0:
            salida = -velocidad_giro_min

        motor_izq.run(sentido_giro * salida)
        motor_der.run(-sentido_giro * salida)

        wait(Ts)

    detener_robot()
    wait(150)

    sensor_gyro.reset_angle(0)
    actualizar_referencia()

    tiempo_ultimo_giro = reloj.time()

    print("Giro terminado")


def girar_derecha():
    girar_gyro(90)


def girar_izquierda():
    girar_gyro(-90)


detener_robot()

ev3.speaker.beep()

print("MAZE: linea recta + pared izquierda")
print("A: motor izquierdo")
print("B: motor derecho")
print("S1: ultrasonido frontal")
print("S2: ultrasonido izquierdo")
print("S3: giroscopio")

print("Calibrando giroscopio. No mover.")
wait(1000)

sensor_gyro.reset_angle(0)
wait(500)

actualizar_referencia()

tiempo_inicio = reloj.time()
tiempo_ultimo_giro = reloj.time()

print("Listo. Inicia en linea recta.")
ev3.speaker.beep()

while True:
    botones = ev3.buttons.pressed()

    if Button.DOWN in botones:
        detener_robot()
        print("Programa terminado")
        ev3.speaker.beep()
        break

    if Button.CENTER in botones:
        detener_robot()

        print("------------------------------")
        print("Frente:", leer_distancia(ultra_frontal), "mm")
        print("Izquierda:", leer_distancia(ultra_izquierdo), "mm")
        print("Gyro:", sensor_gyro.angle())

        wait(700)
        actualizar_referencia()

    distancia_frente = leer_distancia(ultra_frontal)
    distancia_izq = leer_distancia(ultra_izquierdo)

    if distancia_frente < umbral_frente_pared:
        conteo_frente += 1
    else:
        conteo_frente = 0

    if conteo_frente >= conteo_frente_necesario:
        print("Pared frontal confirmada")

        conteo_frente = 0
        conteo_apertura = 0

        detener_robot()
        girar_derecha()
        continue

    if reloj.time() - tiempo_inicio < tiempo_inicio_recto:
        avanzar_recto()
        wait(Ts)
        continue

    if distancia_izq < umbral_izquierda_abierta:
        ya_encontro_pared_izq = True

    puede_tomar_izquierda = (
        reloj.time() - tiempo_ultimo_giro
        > tiempo_ignorar_apertura
    )

    if (
        ya_encontro_pared_izq
        and puede_tomar_izquierda
        and distancia_izq > umbral_izquierda_abierta
    ):
        conteo_apertura += 1
    else:
        conteo_apertura = 0

    if conteo_apertura >= conteo_apertura_necesario:
        print("Abertura izquierda confirmada")

        conteo_apertura = 0
        ya_encontro_pared_izq = False

        detener_robot()

        avanzar_distancia(distancia_antes_giro_izq)
        girar_izquierda()
        avanzar_distancia(distancia_entrada)

        actualizar_referencia()
        continue

    if distancia_izq < umbral_izquierda_abierta:
        seguir_pared_izquierda(distancia_izq)
    else:
        avanzar_recto()

    wait(Ts)
```

### Video de funcionamiento

[Ver video de la prueba](Varios/WhatsApp%20Video%202026-07-11%20at%204.59.56%20PM.mp4)
