// ===== LIBRERIAS =====
#include <XBee.h>
#include <stdio.h>
#include <SoftwareSerial.h>
#include <DHT_U.h>
#include <LowPower.h>
#include "configuration.h"
#include <avr/sleep.h>
#include <avr/wdt.h>
#include <avr/power.h>
#include <avr/interrupt.h>
#include <OneWire.h>
#include <DallasTemperature.h>
// =====================

// ===== VARIABLES =====
// ----- Xbee -----
// Puerto
SoftwareSerial FTDISerial(FTDI_RX, FTDI_TX); // RX, TX
// Objeto
XBeeWithCallbacks xbee;
// Variables asociadas
uint8_t payload[MAX_TRAMA_LENGTH]; // Reservar espacio para la información a enviar
uint8_t direccion_ep[ADDRESS_LENGTH]; // Reservar espacio para la dirección del Endpoint
XBeeAddress64 direccion_gw; // Reservar espacio para la dirección del Gateway
//Parámetros medidos
uint8_t last_rssi;
String last_rssi_string;
// ----------------

// ----- Sensor DHT11 (humedad y temperatura ambiente) -----
// Objeto 
DHT dht(DHT_PIN, DHT_TIPO);
// Variables asociadas
// para humedad
int hum_ambiente;
String hum_ambiente_str;
uint8_t largo_hum_ambiente_str;
// para temperatura
float temp_ambiente;
String temp_ambiente_str;
uint8_t largo_temp_ambiente_str;
// ---------------------------------------------------------

// ----- Sensor YL-69 (humedad suelo) -----
// Variables asociadas
int hum_suelo;
String hum_suelo_str;
uint8_t largo_hum_suelo_str;
// ----------------------------------------

// ----- Sensor DS18B20 (temperatura suelo) ----- 
// Objeto 
OneWire ds(DS_PIN);
DallasTemperature temperatura(&ds);
// Variables asociadas
int temp_suelo;
String temp_suelo_str;
uint8_t largo_temp_suelo_str;
// -----------------------------------------------

//---------SENSOR LLUVIA--------------------------
int medida_lluvia;
//-----------------------------------------------

// ----- Objetos para solicitudes -----
ZBTxRequest tx; //0x10
AtCommandRequest at; //0x08
// ------------------------------------

// ----- Banderas -----
bool es_SH = false;
bool es_SL = false;
bool es_direccion_ep = false; // Obtener mi dirección
bool es_direccion_gw = false; // Obtener dirección del Gateway
bool sensar_ahora = false; // Sensar parámetros
bool es_assign = false; // Gateway asignado
bool es_accepted = false; // Endpoint aceptado
bool obtener_datos = false; // Se cumplió un período de muestreo
bool enviar_datos = false; // Hay nuevos datos para enviar
bool imprimir = true;
bool sleep_encendido = true;
bool envio_dormir;
bool rssi = false;
bool comenzar = false;
// --------------------

// ----- Contadores -----
int timesToReset = 0;
int32_t periodo_muestreo = DEFAULT_SAMPLE_PERIOD;
unsigned long inicio = 0; // Contador de tiempo genérico
unsigned long tiempo = 0; // Contador de tiempo para periodo de muestreo
int i = 0, j = 0; // Índices genéricos
uint8_t largo_trama = 0;
// ----------------------

int estado_anterior = LOW;
// =======================

// ===== FUNCIONES =====

// Procesar TRANSMIT STATUS (0x8B)
void txStatusResponse(ZBTxStatusResponse& response, uintptr_t){
   FTDISerial.println("ENVIÓ PAQUETE!");
}

// Procesar RECEIVE PACKET (0x90)
void rxResponse(ZBRxResponse& rx, uintptr_t){
  FTDISerial.println("LLEGA PAQUETE");
  i = rx.getDataOffset();
  uint8_t id_trama = rx.getFrameData()[TRAMA_ID_INDEX + i];
  uint8_t largo_trama = rx.getFrameData()[TRAMA_LENGTH_INDEX + i];
  FTDISerial.begin(9600);
  switch (id_trama){
    case ASSIGN:
      j = TRAMA_MAC_INDEX + i;
      FTDISerial.println("Desc.: ASSIGN");
      direccion_gw.setMsb(( uint32_t)rx.getFrameData()[j] << 24 | (uint32_t)rx.getFrameData()[j+1] << 16 | (uint32_t)rx.getFrameData()[j+2] << 8 | (uint32_t)rx.getFrameData()[j+3]);
      j+=4;
      direccion_gw.setLsb((uint32_t)rx.getFrameData()[j] << 24 | (uint32_t)rx.getFrameData()[j+1] << 16 | (uint32_t)rx.getFrameData()[j+2] << 8 | (uint32_t)rx.getFrameData()[j+3]);
      j+=4;
      es_assign = true;
      break;
    case ACCEPT:
      j = TRAMA_DATA_INDEX + i;
      FTDISerial.println("Desc.: ACCEPT");
      if( rx.getFrameData()[j] == ACCEPT_OK){
        es_accepted = true;
        //Obtener periodo de muestreo actual
        j++;
        periodo_muestreo = (( uint32_t)rx.getFrameData()[j]<< 24 | (uint32_t)rx.getFrameData()[j + 1] << 16 | (uint32_t)rx.getFrameData()[j + 2] << 8 | (uint32_t)rx.getFrameData()[j + 3]);
        periodo_muestreo = periodo_muestreo * 60 * 1000;
        FTDISerial.print("P. MUESTREO RECIBIDO: ");
       FTDISerial.println(periodo_muestreo);
    }else{
        es_accepted = false;
      }
      break;
    case NEW_SP:
       FTDISerial.println("Desc.: NEW_SP");
       j = TRAMA_DATA_INDEX + i;
       periodo_muestreo = (( uint32_t)rx.getFrameData()[j]<< 24 | (uint32_t)rx.getFrameData()[j + 1] << 16 | (uint32_t)rx.getFrameData()[j + 2] << 8 | (uint32_t)rx.getFrameData()[j + 3]);
       periodo_muestreo = periodo_muestreo * 60 * 1000;
       FTDISerial.print("NUEVO P. MUESTREO: ");
       FTDISerial.println(periodo_muestreo);
       break;
     case RESET:
       FTDISerial.println("RESETEAR SISTEMA");
       timesToReset = RESET_AFTER_TIMES;
       break; 
     default:
        FTDISerial.println("PAQUETE NO CONOCIDO");
  }
}

// Procesar AT COMMAND RESPONSE (0x88)
void atCommandResponse(AtCommandResponse& response, uintptr_t){
    if (response.isOk()) {
      FTDISerial.println("LLEGA AT RESPONSE");
      //RESPUESTA AT DE CONSULTA
      if (response.getValueLength() > 0) {

        //Respuesta a comando SL
        if (response.getCommand()[0] == 'S' && response.getCommand()[1] == 'L'){         
          for (i = 0; i < response.getValueLength(); i++) {
            direccion_ep[i+ADDRESS_LENGTH/2] = response.getValue()[i];
          }
          es_SL = true;
          
        //Respuesta a comando SH
        }else if (response.getCommand()[0] == 'S' && response.getCommand()[1] == 'H'){
          for (i = 0; i < response.getValueLength(); i++) {
            direccion_ep[i] = response.getValue()[i];
          }
          es_SH = true;
        }else if (response.getCommand()[0] == 'D' && response.getCommand()[1] == 'B'){
          if(response.getValueLength() > 0 ){
            rssi = true;
            last_rssi = response.getValue()[0]; 
          }
        }

      //RESPUESTA AT DE CONFIGURACION
      }else{
        
        //Respuesta a comando SM
        if (response.getCommand()[0] == 'S' && response.getCommand()[1] == 'M'){
          if (response.isOk() && !envio_dormir){
            sleep_encendido = false;
          }
        }
      }
    } 
    else {
      //AT ERROR
    }
}

// Definir el modo Sleep del Endpoint en la Xbee
void setSleepModeXbee(bool sleep){
  FTDISerial.print("CAMBIAR MODO SLEEP - ");
  //Sleep Mode = Synchronized Cyclic Sleep (SM = 8)
  uint8_t cmd[] = {'S','M'};
  uint8_t par[1];
  if (sleep){
    par[0] = {0x08};
    FTDISerial.println("ON");
  }else{
    par[0] = {0x00};
    FTDISerial.println("OFF");
  }
  at = AtCommandRequest(cmd, par, (uint8_t)sizeof(par));
  inicio = millis();
  xbee.send(at);
  while (millis() - inicio < WAIT_AT_COMMAND){ 
    xbee.loop();
  }
}

// Obtener mi dirección
bool getMyAddress(){
  FTDISerial.println("OBTENIENDO MAC EP");
  while(!es_SH){
    //Obtener SH
    at =  AtCommandRequest((uint8_t*)"SH"); //Definir comando SH
    inicio = millis();
    xbee.send(at); //Enviar y esperar respuesta por 150mS
    while (millis() - inicio < WAIT_MY_ADDRESS && !es_SH){ 
      xbee.loop();
    }
  }

  while(!es_SL){  
    //Obtener SL
    at =  AtCommandRequest((uint8_t*)"SL"); //Definir comando SH
    inicio = millis();
    xbee.send(at); //Enviar y esperar respuesta por 150mS
    while (millis() - inicio < WAIT_MY_ADDRESS && !es_SL){ 
      xbee.loop();
    }
  }
  
  return es_SH && es_SL;
}

// Obtener dirección de gateway
bool realizarProtocoloDescubrimiento(){
  es_assign = false;
  FTDISerial.println("REALIZANDO PROTOCOLO DE DESCUBRIMIENTO");
  //Proceso de descubrimiento -> Mensaje de broadcast
  //Crear la trama DISCOVERY
  largo_trama = 0;
  payload[TRAMA_ID_INDEX] = DISCOVERY;
  for (i = 0; i < ADDRESS_LENGTH; i++){
    payload[TRAMA_MAC_INDEX + i] = direccion_ep[i];
  }
  payload[TRAMA_LENGTH_INDEX] = largo_trama;
  //Crear la solicitud TX
  tx.setAddress64(XBeeAddress64(BROADCAST_ADDRESS)); //Enviar a dirección de broadcast
  tx.setPayload(payload, largo_trama + TRAMA_DATA_INDEX);
  //Enviarla y epserar por, máximo, 10 segundos
  inicio = millis();
  xbee.send(tx); //Enviar y esperar respuesta por 10S
  while (millis() - inicio < WAIT_DISCOVERY_PROCESS && !es_assign){ 
    xbee.loop();
  }
  FTDISerial.print("es_assign ");
  FTDISerial.println(es_assign);
  if (!es_assign){
    return false;
  }

  //Crear la trama CONFIRM, si recibió respuesta
  largo_trama = 0;
  payload[TRAMA_ID_INDEX] = CONFIRM;
  for (i = 0; i < ADDRESS_LENGTH; i++){
    payload[TRAMA_MAC_INDEX + i] = direccion_ep[i];
  }
  payload[TRAMA_LENGTH_INDEX] = largo_trama;
  //Crear la solicitud TX
  tx.setAddress64(direccion_gw); //Enviar a gateway
  tx.setPayload(payload, largo_trama + TRAMA_DATA_INDEX);
  //Enviarla y epserar por, máximo, 10 segundos
  inicio = millis();
  xbee.send(tx); //Enviar y esperar respuesta por 10S
  while (millis() - inicio < WAIT_DISCOVERY_PROCESS && !es_accepted){ 
    xbee.loop();
  }
  FTDISerial.print("es_assign ");
  FTDISerial.println(es_assign);
  FTDISerial.print("es_accepted ");
  FTDISerial.println(es_accepted);
  return es_assign && es_accepted;
}

// Imprimir unint64_t
void print64(uint64_t int64){
  uint32_t msb = int64 >> 32, lsb = int64;
  FTDISerial.print( msb, HEX);
  FTDISerial.print(" ");
  FTDISerial.print( lsb, HEX);
}

// Función para atender la interrupción del WDT
ISR(WDT_vect){
  cli();
  if (timesToReset < RESET_AFTER_TIMES){
     //Configurar WDT para resetear
     FTDISerial.println(WDTCSR, BIN);
     WDTCSR |= (1 << WDIE); //WDIE = 1 (Si no se reconfigura, a la siguiente no interrumpe, resetea)
     FTDISerial.println(WDTCSR, BIN);
  }else{
    wdt_disable();
    wdt_reset();
    wdt_enable(WDT_PERIOD);
  }
  FTDISerial.print("INTERRUPCION WDT - ");
  FTDISerial.print(tiempo);
    FTDISerial.println("ms");
  if (comenzar){
    tiempo += WDT_TIME;
    obtener_datos = (tiempo >= periodo_muestreo);
  }
  if(obtener_datos){
    if (timesToReset == 0){
      FTDISerial.print("SE CUMPLIÓ UN PERIODO (");
      FTDISerial.print(periodo_muestreo);
      FTDISerial.println(")");   
    }else{
      FTDISerial.println("Sistema trancado!");
    }
    timesToReset++;
  }
  sei();
}

// Función para agarrar la interrupción del XBee SLEEP_ON
void prueba(){
  FTDISerial.println("DESPIERTA XBEE");
}
// ========================

// ===== SETUP ARDUINO =====
void setup(){
  wdt_reset();
  wdt_disable();
  wdt_enable(WDT_PERIOD);
  WDTCSR |= (1 << WDIE); //WDIE = 1 (WDT interrupt enable)
  
  FTDISerial.begin(9600);
  FTDISerial.println("INICIA SETUP");
  Serial.begin(9600);
  xbee.setSerial(Serial);
  dht.begin();
  temperatura.begin();

  // Setear pin de lectura de estado de Sleep XBee
  pinMode(PIN_XBEE_SLEEP, INPUT);
  
  // Definir funciones de callback para cada tipo de RESPONSE
  xbee.onZBTxStatusResponse(txStatusResponse);
  xbee.onZBRxResponse(rxResponse);
  xbee.onAtCommandResponse(atCommandResponse);

  // Apagar modo sleep de Xbee
  envio_dormir = false;   
  while(sleep_encendido){
    setSleepModeXbee(false);
    delay(500);
  }

  // Si no tiene la dirección propia, la debe obtener
  while (!es_direccion_ep) {
    es_direccion_ep = getMyAddress();
    FTDISerial.print("MAC EP: ");
    for (i = 0; i < ADDRESS_LENGTH; i ++){
      FTDISerial.print(direccion_ep[i], HEX);
      FTDISerial.print(" ");
    }
    FTDISerial.println("");
  }
  
  // Si no tiene dirección del gateway, debe realizar todo el proceso para obtenerlo
  FTDISerial.println("es_direccion_gw");
  FTDISerial.println(es_direccion_gw);
  while (!es_direccion_gw){
    es_direccion_gw = realizarProtocoloDescubrimiento();
    FTDISerial.print("MAC GW: ");
    print64(direccion_gw.get());
    FTDISerial.println("");
  }
  
  // Encender modo sleep de Xbee
  envio_dormir = true;
  setSleepModeXbee(true);
  
  // Setear interrupcion cuando se despierta XBee
  attachInterrupt(digitalPinToInterrupt(PIN_XBEE_SLEEP), prueba, RISING);

  // Activar WDT para contar de a 8 segundos
  comenzar = true;
  obtener_datos=true;
  wdt_enable(WDT_PERIOD);
  WDTCSR |= (1 << WDIE); //WDIE = 1 (WDT interrupt enable)
}
// =========================

// ===== LOOP ARDUINO =====
void loop(){
  if (imprimir){
    FTDISerial.println("LOOP PRINCIPAL");
    imprimir = false;
  }

  if(obtener_datos){
    tiempo = (tiempo - periodo_muestreo) < periodo_muestreo ? tiempo - periodo_muestreo : 0;
    timesToReset = 0;
    FTDISerial.println("NUEVO MUESTREO");
    // Inicializar la trama a enviar
    largo_trama = 0;
    payload[TRAMA_ID_INDEX] = DATA;
    for (i = 0; i < ADDRESS_LENGTH; i++){
      payload[TRAMA_MAC_INDEX + i] = direccion_ep[i];
    }
    // ----- Sensor DHT11 (humedad y temperatura ambiente) -----
    // Leer temperatura o humedad toma aproximadamente 250ms, entonces se debe elegir SP > 250ms
    // Leer humedad
    hum_ambiente = dht.readHumidity();
    // Leer temperatura (en grados Celsius)
    temp_ambiente = dht.readTemperature();
    // Pasar medidas a string
    hum_ambiente_str = String(hum_ambiente);
    temp_ambiente_str = String(temp_ambiente);

    // Verficiar si hubo error en alguna lectura
    if (!isnan(hum_ambiente) && !isnan(temp_ambiente)) {
      // Temperatura
      largo_temp_ambiente_str = temp_ambiente_str.length();
      FTDISerial.begin(9600);
      FTDISerial.println("DHT11 - Temp amb:");
      FTDISerial.print("largo: ");
      FTDISerial.println(largo_temp_ambiente_str);
      FTDISerial.print("medida: ");
      FTDISerial.println(temp_ambiente_str);
      // Humedad
      largo_hum_ambiente_str = hum_ambiente_str.length();
      FTDISerial.println("DHT11 - Hum amb:");
      FTDISerial.print("largo: ");
      FTDISerial.println(largo_hum_ambiente_str);
      FTDISerial.print("medida: ");
      FTDISerial.println(hum_ambiente_str);

      // Armar trama - temperatura
      payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_TEMPERATURA_AMBIENTE; // Tipo de sensor
      largo_trama++;
      payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; // Id de sensor
      largo_trama++;
      payload[TRAMA_DATA_INDEX + largo_trama] = largo_temp_ambiente_str; // Largo de medida
      largo_trama++;
      for (i = 0; i < largo_temp_ambiente_str; i ++){
        payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)temp_ambiente_str[i]; // Tipo de sensor
        largo_trama++;
      }
      // Armar trama - humedad
      payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_HUMEDAD_AMBIENTE; //Tipo de sensor
      largo_trama++;
      payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Id de sensor
      largo_trama++;
      payload[TRAMA_DATA_INDEX + largo_trama] = largo_hum_ambiente_str; //Largo de medida
      largo_trama++;
      for (i = 0; i < largo_hum_ambiente_str; i ++){
        payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)hum_ambiente_str[i]; //Tipo de sensor
        largo_trama++;
      }
    }
  // ---------------------------------------------------------

  // ----- Sensor DS18B20 (temperatura suelo) -----
    temperatura.requestTemperatures(); 
    temp_suelo = temperatura.getTempCByIndex(0);
    temp_suelo_str = String(temp_suelo); 
    largo_temp_suelo_str = temp_suelo_str.length();  
    FTDISerial.println("DS18B20 - Hum suelo");
    FTDISerial.print("largo: ");
    FTDISerial.println(largo_temp_suelo_str);
    FTDISerial.print("medida: ");   
    FTDISerial.println(temp_suelo_str);
    payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_TEMPERATURA_SUELO; //Tipo de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Id de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = largo_temp_suelo_str; //Largo de medida
    largo_trama++;
    for (i = 0; i < largo_temp_suelo_str; i ++){
      payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)temp_suelo_str[i]; //Tipo de sensor
      largo_trama++;
    }
  // ------------------------------------------------

  //  ----- Sensor YL-69 (humedad suelo) -----
    hum_suelo = analogRead(YL_PIN);
    hum_suelo = map(hum_suelo ,HUM_MIN_MEDIDA,HUM_MAX_MEDIDA,0,100); //Convertir rango humedad de 0 a 100
    if (hum_suelo < 0) hum_suelo = 0;
    if (hum_suelo > 100) hum_suelo = 100;
    hum_suelo_str = String(hum_suelo); 
    largo_hum_suelo_str = hum_suelo_str.length();
    FTDISerial.print("YL-69 - Temp suelo:\n");
    FTDISerial.print("largo: ");
    FTDISerial.println(largo_hum_suelo_str);
    FTDISerial.print("medida: ");
    FTDISerial.println(hum_suelo_str);
    FTDISerial.print("\n\n");
    payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_HUMEDAD_SUELO; //Tipo de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Id de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = largo_hum_suelo_str; //Largo de medida
    largo_trama++;
    for (i = 0; i < largo_hum_suelo_str; i ++){
      payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)hum_suelo_str[i]; //medida de sensor
      largo_trama++;
    }
  // ------------------------------------------

  //  ----- RSSI -----
    last_rssi_string = String(last_rssi);
    FTDISerial.print("XBEE - RSSI:\n");
    FTDISerial.print("largo: ");
    FTDISerial.println(last_rssi_string.length());
    FTDISerial.print("medida: ");
    FTDISerial.println(last_rssi);
    FTDISerial.print("medida str: ");
    FTDISerial.println(last_rssi_string);
    FTDISerial.print("\n\n");
    payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_RSSI; //Tipo de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Id de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = last_rssi_string.length(); //Largo de medida
    largo_trama++;
    for (i = 0; i < last_rssi_string.length(); i ++){
      payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)last_rssi_string[i]; //medida de sensor
      largo_trama++;
    }
    // ------------------------------------------

  //  ----- Sensor lluvia----------------------
    medida_lluvia = analogRead(RAIN_PIN);
    FTDISerial.print("Lluvia:\n");
    FTDISerial.println("largo: 1");
    FTDISerial.print("medida (");
    FTDISerial.print(medida_lluvia);
    FTDISerial.print("): ");
    payload[TRAMA_DATA_INDEX + largo_trama] = SENSOR_DETECCION_LLUVIA; //Tipo de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Id de sensor
    largo_trama++;
    payload[TRAMA_DATA_INDEX + largo_trama] = 0x01; //Largo de medida
    largo_trama++;
    if (medida_lluvia <= RAIN_THRESHOLD){
      FTDISerial.println("No llueve");
      payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)'0'; //medida de sensor
    }else{
      FTDISerial.println("Llueve");
      payload[TRAMA_DATA_INDEX + largo_trama] = (uint8_t)'1'; //medida de sensor
    }
    largo_trama++;
    FTDISerial.print("\n\n");
  // ------------------------------------------
    
    //Definir el largo de la trama
    payload[TRAMA_LENGTH_INDEX] = largo_trama;
    FTDISerial.print("Largo de trama: ");
    FTDISerial.println(largo_trama);
    //Crear la solicitud TX
    tx.setAddress64(direccion_gw); //Enviar a gateway
    tx.setPayload(payload, largo_trama + TRAMA_DATA_INDEX);
    //Indicar que ya se tomaron nuevos datos
    obtener_datos = false;
    //Indicar que hay datos para enviar
    enviar_datos = true;
  }

  //Verificar estado del modulo RF XBee
  if(digitalRead(PIN_XBEE_SLEEP) == HIGH){
    //Solicitar ultimo RSSI
    //Obtener SH
    at =  AtCommandRequest((uint8_t*)"DB"); //Definir comando SH
    xbee.send(at); //Enviar y esperar respuesta
    //Imprimir el estado de la XBee
    if(estado_anterior == LOW){
      FTDISerial.println("XBEE ON");
      estado_anterior = HIGH; 
    }
    //Si se tomaron nuevas medidas, enviarlas ahora!
    if(enviar_datos){
      FTDISerial.println("ENVÍO DATOS");
      xbee.send(tx);  
      enviar_datos = false;
    }else{
      FTDISerial.println("NO HAY DATOS");
    }
    //Esperar por paquetes DigiMesh
    inicio = millis();
    while(millis() - inicio < WAIT_XBEE_DATA){
      xbee.loop();
    }
    FTDISerial.println("Termina de esperar por datos");
  }else{
    //Imprimir el estado de la XBee
    if(estado_anterior == HIGH){
      FTDISerial.println("XBEE OFF");
      estado_anterior = LOW; 
    }
  }
  
  FTDISerial.println("ARDUINO OFF");
  LowPower.powerDown(SLEEP_FOREVER, ADC_OFF, BOD_OFF);
  FTDISerial.println("ARDUINO ON");
}
//===============================

