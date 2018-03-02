#!/bin/bash

#Crear tunel ssh con forward de puertos
#Ip del servidor: 54.94.146.78
#Puertos utilizados: 8080, 9999, 9998, 9997, 9889, 9888, 9887, 9080, 27017
#Clave publica: kaa-server-0100.pem

#Directorio base
dir=$(pwd)

#Darle los permisos correspondientes al archivo con la clave publica
llave=$dir/SERVIDOR_KAA/kaa-server-0100.pem
chmod 400 $llave

#Abrir el tunel
ip=54.94.146.78

p1=8080:$ip:8080
p2=9999:$ip:9999
p3=9998:$ip:9998
p4=9997:$ip:9997
p5=9889:$ip:9889
p6=9888:$ip:9888
p7=9887:$ip:9887
p8=9080:$ip:9080
p9=27017:$ip:27017

usuario=ubuntu

ssh -L $p1 -L $p2 -L $p3 -L $p4 -L $p5 -L $p6 -L $p7 -L $p8 -L $p9 -i $llave $usuario@$ip
