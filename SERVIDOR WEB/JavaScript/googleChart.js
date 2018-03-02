
google.charts.load('current', {packages: ['corechart', 'line']});
google.charts.load('visualization', '1', {packages: ['controls', 'table','line']});
google.charts.load('visualization', '1', {packages:['corechart']});


function drawBasic(vector, station, h, typeOfSensor) {
    
    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'Fecha');
    data.addColumn('number', typeOfSensor);
    var modVector = modifyVector(vector);
    data.addRows(
        modVector
    );

    var options = {
        //width: 900,
        height: 500,
        pointSize: 5,
        //colors: ['black', 'blue', 'red', 'green', 'yellow', 'gray'],
        legend: {position: 'none'},
        //enableInteractivity: false,
        chartArea: {
            width: '80%' 
        },

        vAxis: {
            title: typeOfSensor 
        },
        hAxis: { 
            viewWindow: {
                min: modVector[0][0],
                max: modVector[modVector.length-1][0]
            },
            gridlines: {
                count: -1,
                units: {
                    days: {format: ['MMM dd']},
                    hours: {format: ['HH:mm', 'ha']},
                }
            },
            minorGridlines: {
                units: {
                    hours: {format: ['hh:mm:ss a', 'ha']},
                    minutes: {format: ['HH:mm a Z', ':mm']}
                }
            },
            title: 'Fecha'
        }
    };

    var idChart = 'chart_div'+station+h;
    var chart = new google.visualization.LineChart(document.getElementById(idChart));
    chart.draw(data, options);

    
}


function drawBasic2Arrays(arrayOfMongoDB, arrayOfPredictions, typeOfSensor) {
    var modVectorMongo = modifyVector(arrayOfMongoDB);
    var modVectorPredictions = modifyVector(arrayOfPredictions);
    //var data1 = new google.visualization.DataTable();
    
    var vector = [];
    vector.push([typeOfSensor[0],typeOfSensor[1],typeOfSensor[1]]);
    for (var i = 0;i < arrayOfMongoDB.length; i++){
        vector.push([arrayOfMongoDB[i][0], arrayOfMongoDB[i][1], null]);
    }
    for (var i = 0;i < arrayOfPredictions.length; i++){
        vector.push([arrayOfPredictions[i][0], null, arrayOfPredictions[i][1]]);
    }
    var data = google.visualization.arrayToDataTable(
        vector
    );
    
    var options = {
        hAxis: {title: typeOfSensor[0] },
        vAxis: {title: typeOfSensor[1]},
        legend: 'none',
        height: 500,
        pointSize: 5
        //trendlines: {0: {}, 1: {}}
    };
    
    var idChart = 'chart_div_'+typeOfSensor[1];
    
    var chart = new google.visualization.LineChart(document.getElementById(idChart));
    chart.draw(data, options);
}


function modifyVector(vector){
    var modVector = [];
    for(var i=0;i<vector.length;i++){
        modVector.push([new Date(vector[i][0]*1000), vector[i][1]]);
    }
    return modVector;
    
}