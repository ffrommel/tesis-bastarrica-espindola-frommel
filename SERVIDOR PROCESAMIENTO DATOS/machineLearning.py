# Script que corre en Servidor de almacenamiento de datos, que realiza la subida del .csv generado al S3 bucket, luego
# crea el modelo y sube un archivo batch asi hace la prediccion
#

import boto.s3
import boto3
import boto
import time
import gzip
import sys

from boto.s3.key import Key
from datetime import datetime


# Funcion para mostrar Buckets
def list_my_buckets(names_buckets, name_of_bucket):
    resp = names_buckets.list_buckets()
    bucket_exist = False
    for buckets in resp['Buckets']:
        if buckets['Name'] == name_of_bucket:
            bucket_exist = True
    return bucket_exist


# Funcion para obtener tiempo actual
def gettime():
    fecha = (str(datetime.now())).split(' ')[0].replace('-', '')
    hora = (str(datetime.now())).split(' ')[1].split('.')[0].replace(':', '')
    return fecha + hora

#Definir tiempo de espera
waitTime = 30

# extension
fechaActual = gettime()
extension = fechaActual
print(extension)

# Key de AWS
AWS_ACCESS_KEY_ID = "XXX"
AWS_SECRET_ACCESS_KEY = "YYY"

# Nombre de Archivo a subir
# file_name = "predicciones.csv"
FILE_NAME_BATCH = "predicciones_batch.csv"

# Nombres de Buckets
BUCKET_NAME = 'bucket_name' + extension
BUCKET_NAME_BATCH = 'bucket_name_batch' + extension


# URLs
# URIBucket = "s3://" + AWS_ACCESS_KEY_ID.lower() + "_" + extension + "/"
URI_BUCKET = "s3://bucket_serv_proc_datos/"
URI_BUCKET_BATCH = "s3://" + BUCKET_NAME_BATCH + "/"

# Variables de la creacion de Fuente de datos para modelo de ML
DATA_SOURCE_ID = 'dataSourceID' + extension
DATA_SOURCE_NAME = 'dataSourceName' + extension
DATA_SOURCE_ID_BATCH = 'dataSourceID_batch' + extension
DATA_SOURCE_NAME_BATCH = 'dataSourceName_batch' + extension

# Variables para Modelo de ML
ML_MODEL_ID = 'mLModelId' + extension
ML_MODEL_NAME = 'mLModelName' + extension


# Nombre de Batch Prediction
BATCH_PREDICTION_ID = 'batchPredictionID' + extension

# Region en donde crear el S3
REGION = 'us-east-1'


# Chequeo de existencia de buckets, si existen se vacian y eliminan
# Cliente para mostrar Buckets
clientBucket = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=REGION)
connectionS3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                              region_name=REGION)

# Creacion de objeto cliente para usos de ML
clientML = boto3.client('machinelearning', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)


# Crear Data Source del S3 para poder referenciar el modelo a esta fuente
print("-------------------------------\n")
print("Creando Data Source del S3\n")
print("Data Source ID: '%s'" % DATA_SOURCE_ID)
print("Data Source Name: '%s'" % DATA_SOURCE_NAME)

# Crear Data Source del CSV para el Modelo de ML
responseCreateDSFS3 = clientML.create_data_source_from_s3(
    DataSourceId=DATA_SOURCE_ID,
    DataSourceName=DATA_SOURCE_NAME,
    DataSpec={'DataLocationS3': URI_BUCKET,
              'DataRearrangement':
                  '{\"splitting\":{\"percentBegin\":0,\"percentEnd\":50}}',
              'DataSchema':
                  '{\"version\":\"1.0\",\"targetAttributeName\":\"Humedad_suelo\",\"dataFormat\":\"CSV\",'
                  '\"dataFileContainsHeader\": true,'
                  '\"attributes\":['
                  '{\"attributeName\":\"Fecha\",\"attributeType\":\"TEXT\"},'
                  '{\"attributeName\":\"Estacion\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Hora\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Temperatura\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Humedad\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Precipitacion\",\"attributeType\":\"BINARY\"},'
                  '{\"attributeName\":\"Humedad_suelo\",\"attributeType\":\"NUMERIC\"}],'
                  '\"excludedVariableNames\": ["Fecha"]}'

              },
    ComputeStatistics=True
)

s3Activo = 0

print("Esperando Data Source Activo")
while s3Activo == 0:
    print("S3 Inactivo")
    time.sleep(waitTime)
    responseS3Status = clientML.get_data_source(DataSourceId=DATA_SOURCE_ID, Verbose=False)
    statusS3 = responseS3Status['Status']
    print(statusS3)
    if statusS3 == 'COMPLETED':
        s3Activo = 1
        print("DataSource creada\n")
    if statusS3 == 'FAILED':
        s3Activo = 2
        print("Error al subir el Data Source del S3, mensaje FAILED\n")
        sys.exit(10)

# Creacion del modelo
print("-------------------------------\n")
print("Creando modelo de ML\n")

# Creacion del modelo de Machine Learning
response = clientML.create_ml_model(
    MLModelId=ML_MODEL_ID,
    MLModelName=ML_MODEL_NAME,
    MLModelType='REGRESSION',
    TrainingDataSourceId=DATA_SOURCE_ID
)

print("Modelo creado\n")
print("-------------------------------\n")
print("Creacion del cliente para Real Time Endpoint\n")

# Crear Real Time Endpoint
clientRTEndpoint = boto3.client('machinelearning', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

# Esperar hasta que el modelo este activo
print("Esperar a que el modelo quede activo\n")
mlActivo = False
while mlActivo is False:
    print("Modelo Inactivo")
    time.sleep(waitTime)
    responseMLState = clientRTEndpoint.get_ml_model(MLModelId=ML_MODEL_ID, Verbose=False)
    statusMLModel = responseMLState['Status']
    print(statusMLModel)
    if statusMLModel == 'COMPLETED':
        mlActivo = True
        print("Modelo de ML completado\n")
    elif statusMLModel == 'FAILED ':
        mlActivo = True
        print("Error al crear el Modelo de ML, mensaje FAILED")
        sys.exit(20)

print("-------------------------------\n")
print("Crear Real Time Endpoint\n")
'''
# Crear Cliente para RTEndpoint
responseRTEndpoint = clientRTEndpoint.create_realtime_endpoint(MLModelId=ML_MODEL_ID)
print("Respuesta al crear Real Time Endpoint: '%s'" % responseRTEndpoint)
'''
# Esperar hasta que el RT Endpoint este activo
print("Esperar a que el RT Endpoint quede activo\n")

rteActivo = False
while rteActivo is False:
    print("RTE Inactivo")
    time.sleep(waitTime)
    responseRTEState = clientRTEndpoint.get_ml_model(MLModelId=ML_MODEL_ID, Verbose=False)
    statusRTEModel = responseRTEState['Status']
    print(statusRTEModel)
    if statusRTEModel == 'COMPLETED':
        rteActivo = True
        print("Modelo de ML completado\n")
    elif statusRTEModel == 'FAILED ':
        rteActivo = True
        print("Error al crear el Real Time Endpoint, mensaje FAILED")
        sys.exit(25)


print("Endpoint creado\n")
print("-------------------------------\n")


# Conexion con AWS
conn_batch = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

# Creacion del Bucket
bucket_batch = conn_batch.create_bucket(BUCKET_NAME_BATCH, location=boto.s3.connection.Location.DEFAULT)

print("Subiendo archivo batch '%s' al bucket S3 de Amazon '%s'" % (FILE_NAME_BATCH, BUCKET_NAME_BATCH))

# Cliente para mostrar Buckets
clientBucket_batch = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

# Dar permisos a las ACL del Bucket y File
responseBucketACL_batch = clientBucket_batch.put_bucket_acl(ACL='public-read-write', Bucket=BUCKET_NAME_BATCH)

# Preparacion del Batch
# Dar permisos al archivo de Batch
k_bucket_batch = Key(bucket_batch)
k_bucket_batch.key = FILE_NAME_BATCH
llave_file_name_batch = k_bucket_batch.key
k_bucket_batch.set_contents_from_filename(FILE_NAME_BATCH)
responseFileACL_batch = clientBucket.put_object_acl(ACL='public-read-write', Bucket=BUCKET_NAME_BATCH,
                                                    Key=llave_file_name_batch)

print("-------------------------------\n")
# Crear Data Source del S3 para poder referenciar el modelo a esta fuente
print("Creando Data Source del S3 Batch")

# Creacion de objeto cliente para usos de ML
client_S3DS_batch = boto3.client('machinelearning', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

# Crear Data Source a partir del archivo en el S3 del Batch
responseCreateDSFS3_batch = client_S3DS_batch.create_data_source_from_s3(
    DataSourceId=DATA_SOURCE_ID + '_batch',
    DataSourceName=DATA_SOURCE_NAME + '_batch',
    DataSpec={'DataLocationS3': URI_BUCKET_BATCH,
              'DataRearrangement':
                  '{\"splitting\":{\"percentBegin\":0,\"percentEnd\":100}}',
              'DataSchema':
                  '{\"version\":\"1.0\",\"dataFormat\":\"CSV\",\"dataFileContainsHeader\": true,'
                  '\"attributes\":['
                  '{\"attributeName\":\"Fecha\",\"attributeType\":\"TEXT\"},'
                  '{\"attributeName\":\"Estacion\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Hora\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Temperatura\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Humedad\",\"attributeType\":\"NUMERIC\"},'
                  '{\"attributeName\":\"Precipitacion\",\"attributeType\":\"BINARY\"}],'
                  '\"excludedVariableNames\": ["Fecha"]}'

              },
    ComputeStatistics=True
)

print("Respuesta de creacion del Data Source de Batch: '%s'" % responseCreateDSFS3_batch)

s3Activo_batch = 0

# Esperar a que la Data Source Batch batch este terminada
while s3Activo_batch == 0:
    print("S3 Batch Inactivo")
    time.sleep(waitTime)
    responseS3Status = client_S3DS_batch.get_data_source(DataSourceId=DATA_SOURCE_ID + '_batch', Verbose=False)
    statusS3_batch = responseS3Status['Status']
    print(statusS3_batch)
    if statusS3_batch == 'COMPLETED':
        print("DataSource Batch creada\n")
        s3Activo_batch = 1
    if statusS3_batch == 'FAILED':
        print("DataSource Batch con error, mensaje FAILED\n")
        s3Activo_batch = 2
        sys.exit(30)


# Creacion de la prediccion batch
if s3Activo_batch == 1:
    responseBatchPrediction = client_S3DS_batch.create_batch_prediction(
        BatchPredictionId='BPID' + extension,
        BatchPredictionName='BPName' + extension,
        MLModelId=ML_MODEL_ID,
        BatchPredictionDataSourceId=DATA_SOURCE_ID + '_batch',
        OutputUri=URI_BUCKET_BATCH
    )

batch_prediction_exist = 0

# Esperar a que la prediccion este finalizada
while batch_prediction_exist == 0:
    print("Esperando Batch Prediction")
    time.sleep(waitTime)
    responseBPStatus = client_S3DS_batch.get_batch_prediction(BatchPredictionId='BPID' + extension)
    statusBP = responseBPStatus['Status']
    print(statusBP)
    if statusBP == 'COMPLETED':
        print("Batch Prediction creada\n")
        batch_prediction_exist = 1
    if statusBP == 'FAILED':
        print("Error al crear la Batch Prediction\n")
        batch_prediction_exist = 2
        sys.exit(40)

# Si se finaliza la prediccion, se trae el CSV con los resultados obtenidos
if batch_prediction_exist == 1:
    # Descarga de archivo en carpeta correspondiente de predicciones
    print("Descarga de archivo CSV con predicciones")
    s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=REGION)
    file_path = 'batch-prediction/result/BPID' + extension + '-' + FILE_NAME_BATCH + '.gz'

    s3.Bucket(BUCKET_NAME_BATCH).download_file(file_path, 'mlOutput.csv.gz')
    inF = gzip.GzipFile('mlOutput.csv.gz', 'rb')
    s = inF.read()
    inF.close()

    with open('mlOutput.csv', 'wb') as csvfile:
        csvfile.write(s)
        csvfile.close()

print("\n----------------FIN---------------\n")
