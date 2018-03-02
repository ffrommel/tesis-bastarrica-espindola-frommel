#include <stdlib.h>
#include <stdio.h>
#include <error.h>
#include <errno.h>
#include "../bibliotecas/manejoSockets.h"
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h> 
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include "../bibliotecas/constantes.h"
#include <string.h>

#define EPCREATE 0x01
#define EPCREATE_OK 0x00
#define EPCREATE_ERR 0x01

int cantidadEndPoints = 0;
volatile int seguirEjecutando = 1;

void terminar(int signum){
	signal(SIGCHLD,SIG_IGN);
	int status;
	int i;

	unlink(SERVDIR);
	if ( signum == SIGTERM ){
		for(i = 0; i < cantidadEndPoints; i++){
			wait(&status);
		}
		exit(EXIT_FAILURE);
	} else {
		exit(EXIT_FAILURE);
	}
}

void terminoComunicador(int signum){
	//Reclamo al comunicador para que no quede zombie
	int status;
	wait(&status);
	cantidadEndPoints--;
}

pid_t crearEndPoint(int sid){  //Debe crear el procesos hijo comunicador
    char sid_string[sizeof(int)];
    char epResponse[2];
	pid_t pid = fork();
	if( pid < 0 ) {
		error_at_line(EXIT_SUCCESS,errno,__FILE__,__LINE__,"Error al crear KAA ENDPOINT!\n");
		//No se pudo crear el hijo 
		epResponse[0] = EPCREATE;
		epResponse[1] = EPCREATE_ERR;
		write(sid, epResponse, sizeof(epResponse));
	} else if ( pid == 0 ) {
		//Estoy en el proceso hijo
	    printf("EPDIR: %s\n", EPDIR);		
        sprintf(sid_string, "%d", sid);
		execl(EPDIR, EPDIR, sid_string, NULL);
		error_at_line(EXIT_FAILURE, errno, __FILE__, __LINE__, "No se pudo ejecutar el KAA ENDPOINT\n");
		//Responder
		epResponse[0] = EPCREATE;
		epResponse[1] = EPCREATE_ERR;
		write(sid, epResponse, sizeof(epResponse));

	} else {
		//Sigo en el proceso padre
		return pid;
	}
	return 0;
}

int main(){

	int socket_id, socketComunicacion_id;

	//Determinar que hacer con las señales que se van a utilizar
	signal(SIGTERM, terminar);
	signal(SIGINT, terminar);
	signal(SIGCHLD, terminoComunicador);

	socket_id = crearSocket(SERVDIR, ROL_SERV);

    printf("Inicio proceso RECEPTOR\n");
	
	while(seguirEjecutando){
	//Queda en loop haciendo esto, hasta que se apague el sistema por una señal!

		//Si un proceso se conecto al scoket, debo crera otra conexion para comunicarme
		socketComunicacion_id = aceptarConexion(socket_id);

		if( (cantidadEndPoints < MAX_ENDPOINTS) && (socketComunicacion_id > 0) ){
			if ( crearEndPoint(socketComunicacion_id) > 0) {
				//Se creo el proceso hijo
				cantidadEndPoints ++;
			}
		}
		close(socketComunicacion_id);
	}		

    printf("Fin proceso RECEPTOR\n");
	
	return 0;
}
