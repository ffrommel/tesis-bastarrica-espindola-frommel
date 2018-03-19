# -*- coding: utf-8 -*-
#!/bin/bash


import boto.s3
import boto3
import csv
import datetime
from constantes import *
from sys import argv
from boto.s3.key import Key


# Funcion para convertir timestamp a fecha hora, estacion del año y momento del dia
def convertir_fecha(archivo_in, archivo_out) :
    samplesBack = 3
    auxArray = []
    # Abrir archivo para escribir la salida con la fecha procesada
    with open(archivo_out, 'w') as f_out:
        # Abrir archivo para procesar fecha y escribir la salida
        with open(archivo_in, 'r') as f_in:
            reader = csv.reader(f_in)
            writer = csv.writer(f_out)
            header = next(reader)
            # Modificar cabecera para las nuevas columnas
            header[0] = "Timestamp"
            header[1] = "Temperatura_amb"
            header[2] = "Humedad_amb"
            header[3] = "Precipitacion"
            header[4] = "Humedad_sue"
            header.append("Mes")
            
            writer.writerow(header)  # Escribir header antes de procesar el archivo

            cont_row = 0
            for row in reversed(list(reader)):

                if cont_row < samplesBack:
                    mes = int(datetime.datetime.fromtimestamp(int(row[0])).strftime('%m'))
                    row.append(mes)
                    auxArray.append(row)
                cont_row += 1
            
            for i in range(len(auxArray)):
                writer.writerow(auxArray[samplesBack-i-1])


# Obtener el nombre del archivo CSV por parametro
file_name = argv[1]
modified = file_name[0:-4] + "_mod.csv"

# Establecer conexion con la consola de Amazon AWS
conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

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

