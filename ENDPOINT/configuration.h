/**
 * Constantes y funciones a utilizar en el programa ejectuado por los endpoints
 */

#ifndef _CONFIGURATION_H_
#define _CONFIGURATION_H_

//Pines utilizados
#define PIN_XBEE_SLEEP 2
// Pin sensor DHT11
#define DHT_PIN 7
// Tipo de sensor
#define DHT_TIPO DHT11
// Pin YL-69
#define YL_PIN A0
// Pin DS18B20
#define DS_PIN 9
// Pin Deteccion lluvia
#define RAIN_PIN A1

//Parametros humedad suelo
#define HUM_MIN_MEDIDA 900
#define HUM_MAX_MEDIDA 200

//Parametros de sensor de lluvia
#define RAIN_THRESHOLD 400 

//Identificadores de paquete de descubrimiento
#define DISCOVERY 0x01
#define ASSIGN 0x02
#define CONFIRM 0x03
#define ACCEPT 0x04
//Identificadores de alta en CONFIRM
#define ACCEPT_OK 0x00
#define ACCEPT_ERR 0x01
//Identificadores de envio de datos
#define DATA 0x11
//Identificadores de paquetes recibidos 
#define NEW_SP 0x12 //de actualización de periodo de muestreo
#define RESET 0x13 //reseter el sistema
#define START_GW 0x14 //reinicio por comienzo de GW

//Tamaño de arrays
#define MAX_TRAMA_LENGTH  100
#define ADDRESS_LENGTH 8

//Inidices
#define TRAMA_ID_INDEX 0
#define TRAMA_MAC_INDEX 1
#define TRAMA_LENGTH_INDEX 9
#define TRAMA_DATA_INDEX 10

//Tiempos de espera (mS)
#define WAIT_MY_ADDRESS 150
#define WAIT_DISCOVERY_PROCESS 10000
#define DEFAULT_SAMPLE_PERIOD 60000//600000 //T(minutos)*60(segundos/minuto)*1000(milisengundos/segundo) --> milisegundos
#define WAIT_AT_COMMAND 5000
#define WAIT_XBEE_DATA 2000

//Tipos de sensores
#define SENSOR_HUMEDAD_SUELO 0x00
#define SENSOR_TEMPERATURA_SUELO 0x01
#define SENSOR_HUMEDAD_AMBIENTE 0x02
#define SENSOR_TEMPERATURA_AMBIENTE 0x03
#define SENSOR_DETECCION_LLUVIA 0x04
#define SENSOR_GPS 0x05
#define SENSOR_RSSI 0x06

//Periodo de WDT
#define WDT_PERIOD SLEEP_8S
#define WDT_TIME 8500 //ms (el tiempo que pasa cada vez que interrumpe, no son exactamente 8 segundos)
#define RESET_AFTER_TIMES 2

//Transmisión para debug por consola serial
#define FTDI_RX 4
#define FTDI_TX 6

#endif
