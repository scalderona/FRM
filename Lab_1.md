# Lab 1 FMR: Trayectorias y sensores
## Grupo de trabajo con el EV3-2
Johan Sebastian Suarez Sepulveda\
Santiago Calderón Alarcón

## Actividad 1
En esta actividad se programó el robot LEGO EV3 para desplazarse en línea recta, asegurando que ambas ruedas operaran a la misma velocidad.
Se realizaron ajustes en los parámetros de velocidad hasta obtener un movimiento estable.

Se analizó la relación entre el tiempo de desplazamiento y la distancia recorrida, programando el robot para avanzar durante un intervalo
determinado y verificando la proporcionalidad entre ambas variables.

Asimismo, se midió el radio de las ruedas y se calculó el avance lineal por revolución. Se estudió el funcionamiento del encoder del motor y se
programó el robot para realizar un desplazamiento correspondiente a ocho revoluciones, deteniéndose mediante la lectura del sensor de rotación.

### Solución planteada
Para lograr el movimiento en línea recta, se programó el robot con ambos motores a igual potencia y velocidad según el diagrama de bloques. No obstante, se observó que la trayectoria no
siempre se mantenía recta debido a factores como el patinamiento de las ruedas y la fricción de los cables, entre otros, lo que generaba desviaciones acumulativas.

Para mitigar estas perturbaciones, se incrementó la potencia a valores iguales o superiores al 50%, logrando una trayectoria más estable y consistente.

Posteriormente, se realizaron tres ensayos de 5 segundos para estimar la velocidad media del robot, midiendo la distancia recorrida y aplicando la relación cinemática básica:

$$v =\frac{d}{t}$$

Obteniéndose:

$$v \approx 24.0\ \frac{cm}{s}$$

Luego, a partir del diámetro medido de la rueda (radio $$r=3 cm$$), se calculó la distancia recorrida por revolución:

$$D_{rev} = 2 \pi r = 18.85\ \frac{cm}{rev}$$

Por tanto, para ocho revoluciones:

$$D_{8rev} = 150.80\ cm$$

Además, se identificó que el motor EV3 incorpora un encoder rotativo óptico incremental con una resolución de 360 pulsos por revolución, lo que permite controlar el desplazamiento con base
en el número de vueltas programadas.

Posteriormente, se implementó la lectura del sensor ultrasónico, que mide la distancia mediante el principio de tiempo de vuelo. Se programó un bucle que permitía al robot avanzar mientras la distancia al obstáculo fuera mayor o igual a $$10\ cm$$, deteniéndose al no cumplirse esta condición.

Debido a la inercia del vehículo, la detención no era inmediata, por lo que se ajustó el umbral a valores ligeramente superiores para compensar el efecto dinámico y aproximarse a la distancia deseada de $$10\ cm$$.
### Diagrama de flujo de las acciones del robot
#### Moverse hacia adelante por $5$ segundos
![Fig 1. MF5S](Varios/lab1/fig1.png)
#### Moverse hacia adelante $8$ giros de la rueda
![Fig 2. 8R](Varios/lab1/fig2.png)
#### Moverse hacia adelante hasta $10 \ cm$ de un obstaculo
![FIg 3. M10](Varios/lab1/fig3.png)

### Videos del robot ejecutando las actividades

### Codigo en blóques del software LEGO MINDSTORMS
#### Moverse hacia adelante $8$ giros de la rueda
![FIg 5. B8R](Varios/lab1/fig5.png)
#### Moverse hacia adelante hasta $10 \ cm$ de un obstaculo
![FIg 6. B10CM](Varios/lab1/fig6.png)


## Actividad 2
En esta actividad se programó el robot para describir trayectorias curvas controlando la diferencia de velocidades entre las ruedas. Primero,
se ejecutó un programa con una rueda a la mitad de la velocidad de la otra, se registró la trayectoria obtenida y se estimó de forma aproximada el
radio de giro. Luego, se diseñó un programa para replicar un radio de giro similar, pero realizando el giro en el sentido contrario (izquierda/derecha).

Adicionalmente, se realizaron pruebas variando la velocidad de la rueda más lenta a un cuarto y tres cuartos de la rueda más rápida, describiendo el efecto
de estos cambios sobre la curvatura y el radio de giro. Finalmente, se propuso un programa que combinara giros en sentidos opuestos para generar una trayectoria en forma de “S”.

### Solución planteada
### Diagrama de flujo de las acciones del robot
### Video del robot ejecutando la actividad
### Codigo en blóques del software LEGO MINDSTORMS

## Actividad 3
En esta actividad se estudió el funcionamiento del girosensor, analizando los valores que entrega en términos de ángulo de rotación y velocidad angular.
Se programó el robot para avanzar en línea recta, realizar un giro controlado de 45° utilizando la lectura del sensor y continuar con un segundo tramo en línea recta.

Posteriormente, se repitió el procedimiento programando un giro de 135°, evaluando la precisión del ángulo alcanzado y el comportamiento del robot durante el cambio de dirección.

### Solución planteada
### Diagrama de flujo de las acciones del robot
### Video del robot ejecutando la actividad
### Codigo en blóques del software LEGO MINDSTORMS

## Actividad 4
En esta actividad se programó el robot para avanzar en línea recta utilizando el sensor infrarrojo para detectar un obstáculo frontal. Al identificar la presencia del obstáculo,
el robot retrocede aproximadamente 10 cm, realiza un giro de 90° hacia la izquierda y continúa con un desplazamiento final en línea recta. Se cargó y ejecutó el programa en el EV3,
verificando el comportamiento esperado frente a la detección del objeto.

### Solución planteada
### Diagrama de flujo de las acciones del robot
### Video del robot ejecutando la actividad
### Codigo en blóques del software LEGO MINDSTORMS

## Actividad 5
En esta actividad se programó el robot para ejecutar la misma secuencia de movimientos del ejercicio anterior, pero utilizando el sensor de contacto como mecanismo de detección.
El robot avanza en línea recta hasta que el sensor táctil es presionado por un obstáculo; en ese momento, retrocede aproximadamente 10 cm, realiza un giro de 90° hacia la izquierda
y continúa con un desplazamiento final en línea recta. El programa fue cargado y ejecutado en el EV3, verificando el funcionamiento del sensor como sistema de detección por contacto.

### Solución planteada
### Diagrama de flujo de las acciones del robot
### Video del robot ejecutando la actividad
### Codigo en blóques del software LEGO MINDSTORMS
