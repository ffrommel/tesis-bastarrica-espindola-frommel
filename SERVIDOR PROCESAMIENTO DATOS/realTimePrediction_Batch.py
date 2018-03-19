# Script que corre en Servidor de almacenamiento de datos, que realiza la subida del .csv generado al S3 bucket, luego
# crea el modelo y sube un archivo batch asi hace la prediccion
#


import boto3
import botocore
import csv

# Definir nombre archivos
realtimeCSV = "CSV/DSWithHistorics.csv"
outputCSV = "CSV/output.csv"
RTP_CSV = "CSV/mLOutput.csv"

# Key de AWS
AWS_ACCESS_KEY_ID = "*****"
AWS_SECRET_ACCESS_KEY = "#####"

# Constantes Real Time Endpoint
RTEndpoint = "/////"
modelID = ">>>>>"

# Region en donde crear el S3
REGION = 'us-east-1'

# Bucket
BUCKET_NAME = "bucketservprocdatos"
mongoData = 'CSV/datos_endpoints.csv'

# Constante
variableForPrediction = "Humedad_sue"

# Descargar CSV con los N datos de Mongo
s3 = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

try:
    s3.Bucket(BUCKET_NAME).download_file(mongoData, mongoData)
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise

with open(mongoData, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    HUM_SUE = []
    rows = 0
    for row in spamreader:
        if rows is 0:
            indexOfVariable = row.index(variableForPrediction)
        else:
            HUM_SUE.append(row[indexOfVariable])
        rows += 1

# Eliminar outputCSV
f = open(outputCSV, "w+")
f.close()
# Eliminar RTP_CSV
f = open(RTP_CSV, "w+")
f.close()


rows = 0
cont = 0
SMS1 = HUM_SUE[0]
SMS2 = HUM_SUE[1]
SMS3 = HUM_SUE[2]

# Creacion de objeto cliente para usos de ML
clientML = boto3.client('machinelearning', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

with open(realtimeCSV, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
        values = []
        if rows is 0:
            titles = row
            titles.append("Humedad_sue-1")
            titles.append("Humedad_sue-2")
            titles.append("Humedad_sue-3")
        else:
            values = row

            record = {}

            if rows is 1 or 0:

                values.append(str(SMS1))
                values.append(str(SMS2))
                values.append(str(SMS3))
                #print(titles)
                #print(values)
            else:
                values.append(str(SMS1))
                values.append(str(SMS2))
                values.append(str(SMS3))

            for x in range(len(values)):
                record[titles[x]] = values[x]
                cont = x
            print("=======================================================")
            #print(record)
            response = clientML.predict(
                MLModelId=modelID,
                Record=record,
                PredictEndpoint=RTEndpoint
            )
            predictedValue = str((response["Prediction"]["predictedValue"]))
            print(record)
            print(predictedValue)
            print(SMS1)
            print(SMS2)
            print(SMS3)
            #print(predictedValue)
            print("=======================================================")
            with open(outputCSV, 'a') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
                if rows is 1:
                    spamwriter.writerow(titles)
                values.append(predictedValue)
                spamwriter.writerow(values)



            SMS3 = SMS2
            SMS2 = SMS1
            SMS1 = predictedValue
        with open(RTP_CSV, 'a') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|')
            if rows is 1:
                spamwriter.writerow(["score"])
            if rows > 1:
                spamwriter.writerow([predictedValue])
        rows += 1

print("\n----------------FIN---------------\n")
