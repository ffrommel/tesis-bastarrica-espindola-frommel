# tesis-bastarrica-espindola-frommel
En este repositorio se reúnen todos los códigos generados en el marco del proyecto de final de la carrera de Ingeniería en Electrónica y Telecomunicaciones de la Universidad ORT Uruguay.

---

**Sistema de soporte a las decisiones de riego con herramientas de aprendizaje automático**

---

## Endpoint

Código desarrollado para Arduino que permite el manejo de los sensores y la comunicación entre ellos y con el Gateway.

1. endpoint.ino
2. configuration.h

---

## Gateway

Códigos desarrollados en lenguajes Python y C para la recepción de nuevos Endpoints y los datos de sensado de los mismos, y subirlos al Servidor de almacenamiento de datos.

1. receiver.py
2. ep_controller.c
3. ep_virtual.c

---

## Servidor de procesamiento de datos

Códigos desarrollados en lenguajes Python y bash para realizar distintas tareas asociadas al Servidor de procesamiento de datos: exportación de datos a .csv, conexión a un servidor remoto para la ejecución de un script y la descarga de los resultados, etc.

1. 

---

## Servidor web

Códigos desarrollados en PHP, JavaScript, HTML y CSS para la construcción del sitio web para la visualización de los valores de las variables sensadas en el tiempo y la configuración del sistema.

1.
