#ifndef _MANEJOSOCKETS_H_
#define _MANEJOSOCKETS_H_

#define ROL_CLI 0
#define ROL_SERV 1

int crearSocket(char *rutaConexion, int rol);
int aceptarConexion(int sockfd);

void cerrarSocket();
void escribirSocket();
void leerSocket();

#endif
