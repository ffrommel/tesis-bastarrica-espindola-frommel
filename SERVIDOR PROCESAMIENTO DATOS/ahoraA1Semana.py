from darksky import forecast
from datetime import date, timedelta
from datetime import datetime as dt
import datetime
import time
import json
import csv
import sys

# Coordenadas para localizacion de pronostico
MVD = -34.887793, -56.249178  # -34.894994, -56.14752

# Llave de usuario
api_key = '#####'

# Deficion de archivo CSV a guardar
fileCSV_name = 'CSV/predictionsDS1W.csv'

GMT = -3
lastDay = 7#int(sys.argv[2])
step = 10#int(sys.argv[3])
numberOfSamplesBack = 3


# Obtener fecha actual
timestamp = int(time.time()) + (60 * 60 * GMT) - (numberOfSamplesBack*60*step)
weekday = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
day_in_seconds = (60 * 60 * 24)

date_from = timestamp#int(sys.argv[1])
date_from_date = datetime.datetime.fromtimestamp(date_from).strftime('%Y-%m-%d')
date_to_date = datetime.datetime.fromtimestamp(date_from + (lastDay * day_in_seconds)).strftime('%Y-%m-%d')
human_time_now = datetime.datetime.fromtimestamp(date_from).strftime('%d-%m-%Y %H:%M:%S')

print("Comienzo DS")

date_to = date_from + (lastDay*day_in_seconds)

# Con el CSV, se va a hacer lo siguiente
with open(fileCSV_name, 'wb') as csvfile:
    # Escribir la primer linea con los nombres de las columnas
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(
        ['Timestamp', 'Temperatura_amb', 'Precipitacion', 'Humedad_amb', 'DewPoint', 'Mes'])

    # Iteracion en dias a predecir
    for seconds in range(date_from, date_to, step*60):

        human_time = datetime.datetime.fromtimestamp(seconds).strftime('%d-%m-%Y %H:%M:%S')
        human_time_split = human_time.split(" ")
        date_week = (human_time_split[0]).split("-")
        time_week = (human_time_split[1]).split(":")
        day_prediction = int(date_week[0])
        month_prediction = int(date_week[1])
        year_prediction = int(date_week[2])
        hour_prediction = int(time_week[0])
        minutes_prediction = int(time_week[1])

        time_of_prediction = dt(year_prediction, month_prediction, day_prediction, hour_prediction, minutes_prediction).isoformat()

        # Consulta de prediccion
        montevideo = forecast(*MVD, time=time_of_prediction, units='si')

        # Fecha y hora de prediccion
        date_and_time = datetime.datetime.fromtimestamp(int(montevideo.time))

        # Creacion de estructura solo para imprimir por pantalla
        first = dict(date=datetime.datetime.fromtimestamp(int(montevideo.time)),
                     time=montevideo.time,
                     precipIntensity=montevideo.precipIntensity,
                     temperature=montevideo.temperature,
                     dewPoint=montevideo.dewPoint,
                     humidity=float(montevideo.humidity) * 100
                     )

        #print('{date} : Temperatura : {temperature}, humedad : {humidity}'.format(**first))

        # Escritura en archivo CSV de la fila
        spamwriter.writerow(
            [montevideo.time, montevideo.temperature, montevideo.precipIntensity,
             round(float(montevideo.humidity)*100, 2), montevideo.dewPoint, month_prediction])
print("FIN DS")
