import csv
from datetime import datetime

# Archivos
resultDS = "CSV/predictionsDS1W.csv"
variables = "CSV/variables.csv"
DSWithHistorics = "CSV/DSWithHistorics.csv"
predicciones_batch = "CSV/predicciones_batch.csv"

# Constantes
rows = 0
numberOfSamplesBack = 3


with open(variables, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    for row in spamreader:
        titlesVariables = []
        if rows is 0:
            titlesVariables = row
            rows = rows+1

#print(titlesVariables)

rows = 0
with open(resultDS, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    titlesDS = []
    valuesDS = []
    for row in spamreader:

        if rows is 0:
            titlesDS = row
        else:
            valuesDS.append(row)
        rows = rows + 1

line4RTP = []
final = []
timestampFlag = True;

# Eliminar outputCSV
f = open(predicciones_batch, "w+")
f.close()


with open(DSWithHistorics, 'w') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

    for x in range(len(valuesDS)):

        line4RTP = []
        line4Graphs = []

        for h in range(len(titlesDS)):
            if x is 0:
                if titlesDS[h] in titlesVariables:
                    line4RTP.append(titlesDS[h])
                    #print(titlesDS[h])
                    if timestampFlag:
                        line4Graphs.append(titlesDS[0])
                    timestampFlag = False
                    line4Graphs.append(titlesDS[h])
                    for j in range(1, numberOfSamplesBack+1):
                        line4RTP.append(titlesDS[h] + "-"+str(j))

                else:
                    line4RTP.append(titlesDS[h])

            if x > 3:

                if titlesDS[h] in titlesVariables:
                    line4RTP.append(valuesDS[x][h])
                    line4Graphs.append(valuesDS[x][h])

                    for k in range(1, numberOfSamplesBack+1):
                        line4RTP.append(valuesDS[x - k][h])

                else:
                    line4RTP.append(valuesDS[x][h])
                    if titlesDS[h] == "Timestamp":
                        date = datetime.fromtimestamp(float(valuesDS[x][h])).strftime('%Y-%m-%d %H:%M:%S')
                        line4Graphs.append(date)

        if len(line4RTP) is not 0:
            spamwriter.writerow(line4RTP)

        #final.append(line4RTP)
        #print(line4Graphs)
        with open(predicciones_batch, 'a') as prediccionesfile:
            spamwriterGra = csv.writer(prediccionesfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

            if len(line4Graphs) is not 0:
                spamwriterGra.writerow(line4Graphs)


