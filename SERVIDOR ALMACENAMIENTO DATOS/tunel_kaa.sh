#!/bin/bash

#Crear tunel ssh con forward de puertos
#Ip del servidor: 54.94.146.78
#Puertos utilizados: 8080, 9999, 9998, 9997, 9889, 9888, 9887, 9080, 27017
#Clave publica: kaa-server-0100.pem

#Darle los permisos correspondientes al archivo con la clave publica
chmod 400 /home/emiliano/kaa-server-0100.pem

#Abrir el tunel
ssh -L 8080:54.94.146.78:8080 -L 9999:54.94.146.78:9999 -L 9998:54.94.146.78:9998 -L 9997:54.94.146.78:9997 -L 9889:54.94.146.78:9889 -L 9888:54.94.146.78:9888 -L 9887:54.94.146.78:9887 -L 9080:54.94.146.78:9080 -L 27017:54.94.146.78:27017 -i /home/emiliano/kaa-server-0100.pem ubuntu@54.94.146.78 
