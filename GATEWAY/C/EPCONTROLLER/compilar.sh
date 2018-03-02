#!/bin/bash
clear
#Directorio base
dir=$(pwd)

#-------------------BIBLIOTECAS-------------------------------
manejoSockets=$dir/bibliotecas/manejoSockets.o

gcc -Wall -c $dir/bibliotecas/manejoSockets.c -o $manejoSockets

#-------------PROGRAMAS DEL SERVIDOR--------------------------
#receptor:
gcc -Wall -o $dir/epcontroller/epcontroller.out $manejoSockets	$dir/epcontroller/epcontroller.c
