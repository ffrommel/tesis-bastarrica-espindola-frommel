#ifndef _CONSTANTES_H_
#define _CONSTANTES_H_

#include <error.h>
#include <errno.h>
#include <sys/types.h>
#include <string.h>

//Maximos
#define MAX_ENDPOINTS 20
#define MAX_PATH 100
#define MAX_DATA 100
#define MAX_DELAY 1 //Segundos
#define MAX_MEASURE_LENGTH 20
#define MAX_CLIENTES 5

//Largos
#define DEMO_LOG_UPLOAD_THRESHOLD 1 //Cantidad de registros en memoria antes de hacer upload
#define INTENTOS 10 //Reintentar conexiones a socket
#define MAC_LENGTH 16
#define EPRESPONSE_LENGTH 2
#define EP_HEAD_LENGTH 2

//True y False
#define FALSE 0
#define TRUE 1

//Rutas
#define EPDIR "./DESARROLLO_KAA/build/epvirtual"
#define RECEPDIR "./C/epcontroller/epcontroller.out"
#define BASEDIR "./tmp/"
#define SERVDIR "./tmp/receiver"

//Mensaje de error
#define ERROR(ESTADO,TEXTO) error_at_line(ESTADO, errno, __FILE__, __LINE__, TEXTO) 

//Protocolo EPV-RECEIVER
#define EPDATA 0x00
#define EPEXISTS 0x02
#define EPEXISTS_OK 0x00
#define EPEXISTS_ERR 0x01

#endif
