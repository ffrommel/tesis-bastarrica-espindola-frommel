from darksky import forecast
from datetime import date, timedelta
from datetime import datetime as dt
import datetime
import time
import json
import csv
import sys

#Coordenadas para localizacion de pronostico
MVD = -34.887793, -56.249178#-34.894994, -56.14752

#Llave de usuario
api_key = 'XXX'

GMT = -3
lastDay = int(sys.argv[2])
step = int(sys.argv[3])

#Obtener fecha actual
timestamp = int(time.time())+(60*60*GMT)
weekday = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
day_in_seconds = (60*60*24)
#Unix_time_now = int(time.mktime(datetime.datetime.strptime(weekday, "%Y-%m-%d").timetuple()))
date_from = int(sys.argv[1])
date_from_date = datetime.datetime.fromtimestamp(date_from).strftime('%Y-%m-%d')
date_to_date = datetime.datetime.fromtimestamp(date_from + (lastDay*day_in_seconds)).strftime('%Y-%m-%d')
human_time_now = datetime.datetime.fromtimestamp(date_from).strftime('%d-%m-%Y %H:%M:%S')


#Funcion que de una fecha, saca el numero de estacion
def number_station(date_predict):

	day_of_year = date(int(date_predict[2]), int(date_predict[1]), int(date_predict[0]))
	day_number = int(day_of_year.strftime("%j"))

	if(day_number>=80 and day_number<=171):
		season='1'
	elif(day_number>=172 and day_number<=263):
		season='2'
	elif(day_number>=264 and day_number<=354):
		season='3'
	else:
		season='4'
	return season 

#Funcion que de una hora saca momento del dia
def convert_time(time_prediction):

	if (time_prediction >= 0 and time_prediction < 6):
		moment = 1
	elif (time_prediction >= 6 and time_prediction < 12):
		moment = 2
	elif (time_prediction >= 12 and time_prediction < 18):
		moment = 3
	else:
		moment=4
	return moment
	

		
print("Comienzo DS")

#Deficion de archivo CSV a guardar		
fileCSV_name = 'predicciones_DMTTHP_'+str(date_from_date)+'_'+str(date_to_date)+'_'+str(step)+'.csv'

#Con el CSV, se va a hacer lo siguiente
with open(fileCSV_name, 'wb') as csvfile:
	
	#Escribir la primer linea con los nombres de las columnas
	spamwriter = csv.writer(csvfile, delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
	spamwriter.writerow(['Day','Month', 'Time','Outside Temperature TX2 (C)','Outside Humidity TX2 (%)','Rain Amount TX2 (mm)'])

	#Iteracion en dias a predecir
	for day in range (0,lastDay):
		
		human_time = datetime.datetime.fromtimestamp(date_from + day*(day_in_seconds)).strftime('%d-%m-%Y %H:%M:%S')
		human_time_split = human_time.split(" ")
		date_week = (human_time_split[0]).split("-")
		time_week = (human_time_split[1]).split(":")
		day_prediction = int(date_week[0])
		month_prediction = int(date_week[1])
		year_prediction = int(date_week[2])
		
		#Iteracion en horas a predecir
		for hour in range (0, 24):
		
			#Indiccion de la fecha  hora el cual se va a hacer la consulta
			for minutes in range (0, 60, step):
				time_of_prediction = dt(year_prediction, month_prediction, day_prediction, hour, minutes).isoformat()

				#Consulta de prediccion
				montevideo = forecast(api_key, *MVD, time=time_of_prediction, units='si')
			
					
				#Fecha y hora de prediccion
				date_and_time = datetime.datetime.fromtimestamp(int(montevideo.time))
			
				#Fecha de la prediccion
				date_of_prediction = [day_prediction, month_prediction, year_prediction]
				season_prediction = number_station(date_of_prediction)

				#Hora de prediccion
				moment_prediction = convert_time(hour) 

				#Precipitaciones
				#precipProbability_prediction = 1 if float(montevideo.precipProbability)>=0.3 else 0 

				
				#Creacion de estructura solo para imprimir por pantalla
				first = dict(date=datetime.datetime.fromtimestamp(int(montevideo.time)),
					 
					precipIntensity=montevideo.precipIntensity,
					temperature=montevideo.temperature,
					humidity=float(montevideo.humidity)*100,
					day_prediction=day_prediction,
					month_prediction=month_prediction,
					hour=hour
					
				)
				

		
			       	print('{day_prediction}/{month_prediction} : {hour} : Temperatura : {temperature}, humedad : {humidity}, intensidad: {precipIntensity}'.format(**first))
			
				#Escritura en archivo CSV de la fila
				spamwriter.writerow([day_prediction, month_prediction, hour, montevideo.temperature, float(montevideo.humidity)*100, montevideo.precipIntensity])
print("FIN DS")




