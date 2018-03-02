//Librerías de KAA SDK
#include <target.h>
#include <inttypes.h>
#include <kaa/kaa_error.h>
#include <kaa/kaa_context.h>
#include <kaa/platform/kaa_client.h>
#include <kaa_configuration_manager.h>
#include <kaa_logging.h>
#include <platform-impl/common/ext_log_upload_strategies.h>
#include <stdint.h>
#include <kaa/gen/kaa_logging_gen.h>
#include <extensions/logging/kaa_logging.h>


//Librerías
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <error.h>
#include <errno.h>
#include "../bibliotecas/manejoSockets.h"
#include <signal.h>
#include <sys/types.h>
#include <sys/select.h>
#include <sys/time.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/socket.h>
#include "../bibliotecas/constantes.h"

//Para mostrar los errores
#define RETURN_ERROR(error, mensaje) \
	if ((error)) { \
		printf("ERORR: %d - MENSAJE: " mensaje, (error)); \
		return (error);	\
	}

typedef struct {
	kaa_client_t *kaa_client;
	int32_t periodoMuestreo;
} datosConfiguracion;


char SOCKDIR[MAX_PATH]=BASEDIR;
int sId, sServId, sServComId;
char MAC[MAC_LENGTH+1], data[MAX_DATA], epResponse[EPRESPONSE_LENGTH];
//Para el select
int esperando_conexion = 0;
fd_set read_fds;
struct timeval tv;
int retval;

//Cliente kaa
kaa_client_t *kaa_client = NULL;

static void error_cleanup(kaa_client_t *cliente)
{
	if (cliente != NULL) {
		kaa_client_stop(cliente);
		kaa_client_destroy(cliente);
	}

	exit(EXIT_FAILURE);
}

static kaa_error_t actualizarConfiguracion(void *context,
		const kaa_configuration_configuration_t *configuration)
{
	int sockfd, i, indice = 0;
	uint8_t d[4] = {0};
	int32_t u;
	unsigned char trama[MAX_LENGTH_TRAMA], mac_bytes[MAC_LENGTH], *pos = MAC;
	
	if (!context || !configuration) {
		return KAA_ERR_BADPARAM;
	}

	datosConfiguracion *datos = context;
	u = configuration->sample_period;
	printf("Viejo periodo de muestreo: %d\n", datos->periodoMuestreo);
	printf("Nuevo periodo de muestreo: %d\n", u);
	
	if (datos->periodoMuestreo != u){
		datos->periodoMuestreo = u;
		//Enviar el dato al EP físico
		//1 - Conectar al socket del RECEIVER (socket cliente)
		//2 - Enviar trama con el nuevo periodo de muestreo
		trama[indice] = EPNEW_SP;
		indice++;
		for (i = 0; i < 8; i++){
			sscanf(pos, "%2hhx", &trama[indice]);
			pos += 2*sizeof(char);
			indice++;
		}
		
		trama[indice] = sizeof(datos->periodoMuestreo);
		indice++;
	    trama[indice + 3] = (char)u;
	    trama[indice + 2] = (char)(u>>=8);
	    trama[indice + 1] = (char)(u>>=8);
	    trama[indice + 0] = (char)(u>>=8);
		indice += sizeof(u);

		printf("0x");
		for (i = 0; i < indice; i++){
			printf("%x",trama[i]);
		}
		printf("\n");

		sockfd = crearSocket(SENDDIR, ROL_CLI);
		write(sockfd, &trama, (size_t)indice);

		close(sockfd);
			
		return KAA_ERR_NONE;
	}
}

static void actualizarSensores(void *context)
{
	//Obtener los datos
	if (context == NULL) {
		return;
	}
	datosConfiguracion *datos = context;
	kaa_client_t *kaa_client = datos->kaa_client;

	char frameId, frameLength, mac[MAC_LENGTH+1], timestamp[sizeof(time_t)+1];

	if(!esperando_conexion){
		//Comienza a esperarla
		printf("Esperando por una conexion de %s ", MAC);
		esperando_conexion = 1;
	}else{
		printf(".");
	}
	
	//Select para que no bloquee esperando por el socket
	FD_ZERO(&read_fds);
	FD_SET(sServId, &read_fds);
	//Ver si llega algo, sino continuar luego (timeout = 0)
	tv.tv_sec = 0;
	tv.tv_usec = 0;
	//sentencia select
	retval = select(sServId+1, &read_fds, NULL, NULL, &tv);
	//resultado del select
	if(retval == -1){
		//ERROR
	}else if (retval){
		//OK - hay datos para leer
		if (FD_ISSET(sServId, &read_fds)){
			esperando_conexion = 0;
		}
	}else{
		//Timeout
	}

	if(!esperando_conexion){ //Si no espero mas por la conexion, es porque llego

		sServComId = aceptarConexion(sServId);

		kaa_logging_ep_data_t *log_record = kaa_logging_ep_data_create();
		if (!log_record) {
			demo_printf("Falla al crear registro de datos\r\n");
			error_cleanup(kaa_client);
		}

		if(sServComId > 0){
			printf("Se recibio la conexión de una estacion\n");
			read(sServComId, &frameId, sizeof(char));
			sprintf(timestamp, "%lu", (unsigned long)time(NULL)); //Timestamp
			read(sServComId, &frameLength, sizeof(char));
			if (frameId == EPDATA && frameLength > 0){
				log_record->mac = kaa_string_copy_create(MAC)				/*MAC*/;
				log_record->time_stamp = kaa_string_copy_create(timestamp)	/*TIMESTAMP*/;
				log_record->sensores = kaa_list_create();					/*CREAR LISTA*/
				printf("Informacion: \n");
				printf("-MAC: %s\n",log_record->mac->data);
				printf("-timeStamp: %s\n",log_record->time_stamp->data);
				printf("-frameLength: %d\n", (int32_t)frameLength);
				char i = 0;
				int x;
				while (i < frameLength){ /*AGREGAR REGISTRO POR CADA SENSOR*/
					char sensorType, sensorId, measureLength;
					char measure[MAX_MEASURE_LENGTH];
					int measureInt;
					kaa_logging_sensor_data_t *sensor= kaa_logging_sensor_data_create(); /*CREAR EL CAMPO DEL SENSOR*/
					read(sServComId, &sensorType, sizeof(char)); 
					printf("Medida:\n");
					printf("-Tipo de sensor: %d\n",(int32_t)sensorType);
					i++;
					read(sServComId, &sensorId, sizeof(char)); 
					printf("-Id de sensor: %d\n",(int32_t)sensorId);
					i++;
					read(sServComId, &measureLength, sizeof(char)); 
					printf("-Largo de medida: %d\n", (int32_t)measureLength);
					i++;
					read(sServComId, measure, sizeof(char)*(measureLength));
					measure[measureLength] = '\0';
					printf("-Valor recibido: %s\n", measure);
					i+=measureLength;
					printf("-indice: %d\n", (int32_t)i);
					//Agregar la medida al registro
					sensor->sensor_type = (int32_t)sensorType;			/*TIPO DE SENSOR*/
					sensor->sensor_id = (int32_t)sensorId; 				/*ID DEL SENSOR*/
					sensor->measure = kaa_string_copy_create(measure); 	/*MEDIDA*/
					//Agregar el registro a la lista
					kaa_list_push_back(log_record->sensores, sensor);
				}
				//Pronto para subir al servidor
				kaa_error_t error = kaa_logging_add_record(kaa_client_get_context(kaa_client)->log_collector,log_record, NULL);
				if (error) {
					demo_printf("Falla al agregar la informacion para subir al servidor, error code %d\r\n", error);
					error_cleanup(kaa_client);
				}
			}else{
				printf("No es EPDATA o no hay datos\n");
			}
			close(sServComId);
		}else{
			printf("Error al recibir la conexion de la estacion\n");
		}

		log_record->destroy(log_record);
	}
}

void terminate(int signum){
	unlink(SOCKDIR);   

	kaa_client_destroy(kaa_client);
}

//AGREGAR PARA CALLBACKS CUANDO ENVIA
/* Set of routines that handles log delivery events */
static void success_log_delivery_callback(void *context, const kaa_log_bucket_info_t *bucket)
{
    printf("\nExito al enviar!\n");
}
 
static void failed_log_delivery_callback(void *context, const kaa_log_bucket_info_t *bucket)
{
    printf("\nFalla al enviar!\n");
}
 
static void timeout_log_delivery_callback(void *context, const kaa_log_bucket_info_t *bucket)
{
    printf("\nTimeout al enviar!\n");
}

int main(int argc, char *argv[])
{
	//Comportamiento ante señales (interrupciones)
	signal(SIGTERM, terminate);
	signal(SIGINT, terminate);
	
	//Obtener el socketId heredado del EPCONTROLLER
	sscanf(argv[1], "%d", &sId);
	
	//RESPONDER
	epResponse[0] = EPCREATE;
	epResponse[1] = EPCREATE_OK;
	write(sid, epResponse, sizeof(epResponse));

	//Esperar la MAC para crear el socket servidor correspondiente
	read(sId, MAC, (size_t)MAC_LENGTH);
	MAC[MAC_LENGTH] = '\0';


	//Inicializar una placa
	int ret = target_initialize();
	if (ret < 0) {
		//Si la consola falla al inicializar, no deberías ver este mensaje
		printf("Falla al inicializar el 'target'\r\n");
		return 1;
	}
	
	demo_printf("Inicio de EPVIRTUAL\r\n");

	//Iniciar cliente Kaa
	kaa_client_t *kaa_client = NULL;
	kaa_error_t error = kaa_client_create(&kaa_client, NULL);
	RETURN_ERROR(error, "Falla al crear el cliente Kaa\r\n");

	//Definir función para actualización de CONFIGURACIÓN
	datosConfiguracion datos;
	datos.kaa_client = kaa_client;
	kaa_configuration_root_receiver_t receiver = {
		&datos,
		actualizarConfiguracion,
	};

	error = kaa_configuration_manager_set_root_receiver(
			kaa_client_get_context(kaa_client)->configuration_manager,
			&receiver);
	RETURN_ERROR(error, "Falla al definir función para actualización de CONFIGURACIÓN\r\n");    

	const kaa_configuration_configuration_t *default_configuration =
			kaa_configuration_manager_get_configuration(kaa_client_get_context(kaa_client)->configuration_manager);

	datos.periodoMuestreo = default_configuration->sample_period;
	

	void *log_upload_strategy_context = NULL;
	 
	/* Log delivery listener callbacks. Each callback called whenever something happen with a log bucket. */
	kaa_log_delivery_listener_t log_listener = {
	     .on_success = success_log_delivery_callback,   /* Called if log delivered successfully */
	     .on_failed  = failed_log_delivery_callback,    /* Called if delivery failed */
	     .on_timeout = timeout_log_delivery_callback,   /* Called if timeout occurs */
	};

	error = ext_log_upload_strategy_create(kaa_client_get_context(kaa_client),
			&log_upload_strategy_context, THRESHOLD_COUNT_FLAG);
	RETURN_ERROR(error, "Falla al crear una estrategia de LOG\r\n");    

	error = ext_log_upload_strategy_set_threshold_count(log_upload_strategy_context,
			LOG_UPLOAD_THRESHOLD);
	RETURN_ERROR(error, "Falla al definir umbral de cantidad de registros\r\n");

	error = kaa_logging_set_strategy(kaa_client_get_context(kaa_client)->log_collector,
			log_upload_strategy_context);
	RETURN_ERROR(error, "Falla al definir la estrategia de LOG");
	
	//Agregar los listeners
	kaa_logging_set_listeners(kaa_client_get_context(kaa_client)->log_collector, &log_listener);
	
	
	printf("Se va a crear un EP para la estacion: %s\n", MAC);
	strncat(SOCKDIR, MAC, (size_t)MAC_LENGTH);
	printf("SOCKDIR: %s\n", SOCKDIR);

	if ((sServId = crearSocket(SOCKDIR, ROL_SERV)) > 0){
		//Se crea socket servidor de la estacion virtual de forma correcta
		epResponse[0] = EPEXISTS;
		epResponse[1] = EPEXISTS_OK;
		//TODO: Agregar perido de muestreo
	}else{
		//Problemas al crear el socket servidor para la estacion virtual
		epResponse[0] = EPEXISTS;
		epResponse[1] = EPEXISTS_ERR;  
	}
	write(sId, epResponse, sizeof(epResponse)); //Agregar antes de la caida por cualquier problema de Kaa
	close(sId);

	//Comenzar bucle KAA
	error = kaa_client_start(kaa_client, actualizarSensores,
			&datos, MAX_DELAY);
	RETURN_ERROR(error, "Falla al comenzar el cliente KAA\r\n");

	//Destruir cliente KAA
	kaa_client_destroy(kaa_client);

	return EXIT_SUCCESS;
}
