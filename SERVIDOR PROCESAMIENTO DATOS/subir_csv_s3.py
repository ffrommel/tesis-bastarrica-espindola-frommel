# -*- coding: utf-8 -*-
#!/bin/bash

from sys import argv
import boto.s3
import boto3
from boto.s3.key import Key
import csv
import datetime
from constantes import *

# Funcion para convertir timestamp a fecha hora, estacion del año y momento del dia
def convertir_fecha(archivo_in, archivo_out):
    # Abrir archivo para escribir la salida con la fecha procesada
    with open(archivo_out, 'w') as f_out:
        # Abrir archivo para procesar fecha y escribir la salida
        with open(archivo_in, 'r') as f_in:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            header = next(reader)
            # Modificar cabecera para las nuevas columnas
            header[0] = "Fecha"
            header.insert(1, "Estacion")
            header.insert(2, "Hora")
            header[3] = "Temperatura"
            header[4] = "Humedad"    
            header[5] = "Precipitacion"
            header[6] = "Humedad_suelo"
	    # TODO: Para codigo automatizado, comentar este
	    # header[7] = "Temperatura_suelo" 
            writer.writerow(header)  # Escribir header antes de procesar el archivo

            for row in reader:
                # Disgregar el timestamp
                ano = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%Y'))
                mes = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%m'))
                dia = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%d'))
                hora = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%H'))
                min = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%M'))
                seg = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%S'))

                # Escribir fecha y hora
                fecha_horario = "{:4d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(ano, mes, dia, hora, min, seg)
                row[0] = fecha_horario

                # Escribir estacion del año
                es_otono = (dia >= DIA and mes == MES_OTONO) or \
                           (mes > MES_OTONO and mes < MES_INVIERNO) or \
                           (dia < DIA and mes == MES_INVIERNO)

                es_invierno = (dia >= DIA and mes == MES_INVIERNO) or \
                              (mes > MES_INVIERNO and mes < MES_PRIMAVERA) or \
                              (dia < DIA and mes == MES_PRIMAVERA)

                es_primavera = (dia >= DIA and mes == MES_PRIMAVERA) or \
                               (mes > MES_PRIMAVERA and mes < MES_VERANO) or \
                               (dia < DIA and mes == MES_VERANO)

                es_verano = (dia >= DIA and mes == MES_VERANO) or \
                            (mes >= ENERO and mes < MES_OTONO) or \
                            (dia < DIA and mes == MES_OTONO)

                if es_otono:
                    row.insert(1, ID_OTONO)
                elif es_invierno:
                    row.insert(1, ID_INVIERNO)
                elif es_primavera:
                    row.insert(1, ID_PRIMAVERA)
                elif es_verano:
                    row.insert(1, ID_VERANO)

                # Escribir momento del dia
                es_madrugada = hora >= HORA_MADRUGADA and hora < HORA_MANANA
                es_manana = hora >= HORA_MANANA and hora < HORA_TARDE
                es_tarde = hora >= HORA_TARDE and hora < HORA_NOCHE
                es_noche = hora >= HORA_NOCHE

                if es_madrugada:
                    row.insert(2, ID_MADRUGADA)
                elif es_manana:
                    row.insert(2, ID_MANANA)
                elif es_tarde:
                    row.insert(2, ID_TARDE)
                elif es_noche:
                    row.insert(2, ID_NOCHE)

                writer.writerow(row)


# Obtener el nombre del archivo CSV por parametro
file_name = argv[1]
modified = file_name[0:-4] + "_mod.csv"

# Region en donde crear el S3
REGION = 'us-east-1' # TODO: Pasar a constantes.py

# Establecer conexión con la consola de Amazon AWS
conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)

# Crear un bucket S3 para almacenar el archivo CSV con datos de los sensores
bucket = conn.create_bucket(BUCKET_NAME, location=boto.s3.connection.Location.DEFAULT)

# Cliente para mostrar Buckets
clientBucket = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

# Dar permisos a las ACL del Bucket y File
responseBucketACL = clientBucket.put_bucket_acl(ACL='public-read-write', Bucket=BUCKET_NAME)

# Modificar columna de timestamp en el archivo CSV antes de subirlo
convertir_fecha(file_name, modified)

# Subir archivo CSV al bucket S3 recien creado
print("Subiendo archivo '%s' al bucket S3 '%s'..." % (modified, BUCKET_NAME))
k = Key(bucket)
key_val = "datos_endpoints.csv"
k.key = key_val
k.set_contents_from_filename(modified)

responseFileACL = clientBucket.put_object_acl(ACL='public-read-write', Bucket=BUCKET_NAME, Key=key_val)

print("Subida completa")

