#include "../bibliotecas/manejoSockets.h"
#include "../bibliotecas/constantes.h"
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <string.h>
#include <sys/un.h>
#include <unistd.h>
 
#define SOCKETDIR "/home/emiliano/PBN/obligatorio/simulacion.socket"

int crearSocket(char *rutaConexion, int rol){
	//Se considera que todos seran del tipo UDS, por lo tanto la familia es PF_LOCAL
	//El rol indica si es cliente o servidor
	
	struct sockaddr_un direccionServidor;
	int sockfd = -1, familia = PF_LOCAL, tipo = SOCK_STREAM;
	socklen_t largo;
	
	if ( (sockfd = socket(familia, tipo, 0)) < 0) {
		return sockfd;
	}
			memset( &direccionServidor, 0, sizeof(direccionServidor));
		direccionServidor.sun_family = familia;
	strncpy( direccionServidor.sun_path, rutaConexion, sizeof(direccionServidor.sun_path) - 1);
		largo = sizeof(direccionServidor);

	if (rol == ROL_CLI){
		if ( connect(sockfd, (struct sockaddr *) &direccionServidor, largo) < 0){
			close(sockfd);
			return -1;
		}
	} else if (rol == ROL_SERV) {
		if ( bind(sockfd, (struct sockaddr *) &direccionServidor, largo) < 0){
			close(sockfd);
			return -2;	
		}
		if ( listen(sockfd, MAX_CLIENTES) < 0) {
			close(sockfd);
		return -3;
		}
		
	} else {
		//En este caso se creo el socket pero no se enlazo a una direccion o no se conecto
		close(sockfd);
		return -4;
	}	

	return sockfd;		

}

int aceptarConexion(int sockEscuchafd){
	struct sockaddr_un direccionCliente;
	socklen_t largo = sizeof(direccionCliente);
	int sockfd, intentos = INTENTOS;
	
	do { 
		sockfd = accept(sockEscuchafd, (struct sockaddr *) &direccionCliente, &largo);
		intentos --; 
	} while (sockfd < 0 && intentos > 0);

	if ( intentos <= 0) {
		ERROR(EXIT_FAILURE, "No se pudo aceptar la conexion");
	}	

	return sockfd;
}
