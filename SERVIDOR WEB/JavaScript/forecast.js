
$(document).ready(initialize);


function initialize(){
    google.charts.load('current', {packages: ['corechart', 'line']});
    google.charts.load('visualization', '1', {packages: ['controls', 'table','line']});
    google.charts.setOnLoadCallback(loadForecast);
    
}

function loadForecast(){
    $("#loadingLabelForecast").html("Cargando gráficos...");
    var urlCSV_DS =  "../../Predicciones/predicciones_batch.csv";
     $.ajax({
        type: "GET",
        url: urlCSV_DS,
        dataType: "text",
        success: printChartsDS,
        timeout: 40000,
        error: errorChartDS 
    });
    

}

function printChartsDS(data) {
    var dataCSV = parseCSV(data);
    var titles = dataCSV[0];
    var returnOfFunction = [];
    var dataBaseInfo = getDataOneWeekBack();
    generateGraphs(titles, dataCSV, dataBaseInfo);   
 
}

function generateGraphs(titles, dataCSV, dataBaseInfo){
    var dates = [];
    var allData = dataBaseInfo[0].concat(dataCSV);
    var arrayOfMongoDB = [];
    var arrayOfPredictions = [];
    
    for(var i = 3; i < titles.length; i++){
        var beforeMark = true;
        var datePrediction;
        arrayOfMongoDB = [];
        arrayOfPredictions = [];
   
        text = "";
        text += "<div id='forecast"+titles[i]+"' class='divFadeIn'>";
        text += "<br><label class='chartTitle'>Histórico de Estaciones y Predicciones de Dark Sky</label><br>";                
        text += "<br><br><label class='chartTitle'>Tipo de predicción : "+ titles[i] +"</label>";                
        text += "<div id='chart_div_"+titles[i]+"'></div>";
        text += "<br><label class='chartTitle'>Azul : Histórico ,  Naranja : Predicción</label><br>";                
        text += "<hr></div>";
        $("#showForecast").append(text);
        var vector = [];
        var timeForML = [];
        var date;
        var dateSplit;
        var timeSplit;
        var typeOfParameter = [titles[0],titles[i]];
        for(var j = 0; j < allData.length; j++){
            if(allData[j][0] == "*" || allData[j][0] == "Fecha"){
                beforeMark = false;
            }else{
                if(beforeMark){
                    datePrediction = allData[j][0];
                    
                }else{

                    date = allData[j][0].split(" ");
                    dateSplit = date[0].split("-");
                    timeSplit = date[1].split(":");
                    datePrediction = new Date(dateSplit[0], dateSplit[1]-1, dateSplit[2], timeSplit[0], timeSplit[1], timeSplit[2]);
                    timeForML.push(datePrediction);
                }
                dates.push(datePrediction);

                if(beforeMark){
                    arrayOfMongoDB.push([datePrediction,parseFloat(allData[j][i])]);
                }else{
                    arrayOfPredictions.push([datePrediction,parseFloat(allData[j][i])]);
                }
                vector.push([datePrediction,parseFloat(allData[j][i])]);
            }
        }
       
        drawBasic2Arrays(arrayOfMongoDB, arrayOfPredictions, typeOfParameter);

    }
    machineLearningGraph(dataBaseInfo[1],timeForML);
    

}

function machineLearningGraph(soilHumidity, timeForML){
    var urlCSV_ML =  "../../ML/mlOutput.csv";
    $.ajax({
        type: "GET",
        url: urlCSV_ML,
        dataType: "text",
        success: function printChartsML(data){
            
            var dataCSV = parseCSV(data);
            var dataCSVPlus = [];
            for(var i = 0; i<dataCSV.length; i++){
                dataCSVPlus.push([,dataCSV[i]]);
            }
            var titles = ["Fecha","Humedad del suelo"];
            
            text = "";
            text += "<div id='forecastML"+titles[1]+"' class='divFadeIn'>";
            text += "<br><label class='chartTitle'>Histórico de Estaciones y Predicciones de Amazon Machine Learning</label><br>";                
            text += "<br><br><label class='chartTitle'>Predicción de ML : "+ titles[1] +"</label><br>";                
            text += "<div id='chart_div_"+titles[1]+"'></div>";
            text += "<hr></div>";
            $("#showForecast").append(text);
            
            var vector = soilHumidity;
            var allData = vector.concat(dataCSVPlus);
            var contForTime = 0;
            var date;
            var dateSplit;
            var timeSplit;
            var datePrediction;
            var beforeMark = true;
            var arrayOfMongoDB = [];
            var arrayOfPredictions = [];
            var dates = [];
            var typeOfParameter = [titles[0],titles[1]];
            for(var j = 0; j < allData.length; j++){
                if(allData[j][1] == "score"){
                    beforeMark = false;
                }else{
                    
                    if(beforeMark){
                        datePrediction = allData[j][0];
                        dates.push(datePrediction);
                        arrayOfMongoDB.push([datePrediction,parseFloat(allData[j][1])]);
                    }else{
                        
                        datePrediction = timeForML[contForTime];
                        dates.push(datePrediction);
                        arrayOfPredictions.push([datePrediction,parseFloat(allData[j][1])]);
                        contForTime++;
                        
                    }
                    vector.push([datePrediction,parseFloat(allData[j][1])]);
                }
            }
           
            drawBasic2Arrays(arrayOfMongoDB, arrayOfPredictions, typeOfParameter);
      
        },
        timeout: 4000,
        error: errorChartML 
    });
}

function errorChartDS(){
    $("#loadingLabelForecast").empty();
    text = "";
    text += "<div id='forecastML' class='divFadeIn'>";
    text += "<br><label class='chartTitle'>Error al cargar CSV de Histórico y Predicciones Dark Sky</label><br>";                
    text += "<hr></div>";
    $("#showForecast").append(text);
}




function errorChartML(){
    $("#loadingLabelForecast").empty();
    text = "";
    text += "<div id='forecastML' class='divFadeIn'>";
    text += "<br><label class='chartTitle'>Error al cargar CSV de Histórico y Predicciones Machine Learning</label><br>";                
    text += "<hr></div>";
    $("#showForecast").append(text);
}


function getDataOneWeekBack(){

    var date = new Date();
    var backTimeFrom = new Date(date.getFullYear(), date.getMonth(), date.getDate()-7).getTime() / 1000;
    var backTimeTo = new Date(date.getFullYear(), date.getMonth(), date.getDate()).getTime() / 1000;
    var timeFrom = "00:00";
    var timeTo = "23:59";
    var returnOfFunction = [];
    var dataOfMDB = [];
    var temperature, humidity, precipitation = 0;
    var measure, soil_humidity = [];
    var markDivition = ["*","*","*","*","*","*"];
    $.ajax({
        async:false, 
        url: "charts.php",
        type: "POST",
        dataType: "JSON",
        success: function successGetData(data){
                
            dataOfMDB = data["Estaciones"].sort(function(a, b){return a.Hora > b.Hora}); ;

        },
        timeout: 4000,
        error: errorGetData, 
        data: {inputBackTimeFrom:backTimeFrom, inputBackTimeTo:backTimeTo, timeFrom:timeFrom, timeTo:timeTo}
    });    
    
    $("#loadingLabelForecast").empty();
    var macToUse;
    var macToUseFound = false;
    var countFound = 0;
    for(var i = 0; i < dataOfMDB.length; i++){

        if(!macToUseFound){
            countFound = 0;
            for(var h = 0; h < dataOfMDB[i]["Medidas"].length; h++){
                if (dataOfMDB[i]["Medidas"][h]["sensorType"]==2){
                    countFound++;
                }
                if (dataOfMDB[i]["Medidas"][h]["sensorType"]==3){
                    countFound++;
                }
                if (dataOfMDB[i]["Medidas"][h]["sensorType"]==4){
                    countFound++;
                }
                if (dataOfMDB[i]["Medidas"][h]["sensorType"]==0){
                    countFound++;
                }
            }
            if(countFound==4){
                macToUseFound = true;
                macToUse = dataOfMDB[i]["Estacion"];
            }    
        }
        
        if(macToUseFound){    
            if(dataOfMDB[i]["Estacion"] == macToUse){
                date = new Date(dataOfMDB[i]["Hora"]*1000);

                for(var j = 0; j < dataOfMDB[i]["Medidas"].length; j++){
                    if (dataOfMDB[i]["Medidas"][j]["sensorType"]==2){
                        humidity = dataOfMDB[i]["Medidas"][j]["measure"];
                    }
                    if (dataOfMDB[i]["Medidas"][j]["sensorType"]==3){
                        temperature = dataOfMDB[i]["Medidas"][j]["measure"];
                    }
                    if (dataOfMDB[i]["Medidas"][j]["sensorType"]==4){
                        precipitation = dataOfMDB[i]["Medidas"][j]["measure"];
                    }
                    if (dataOfMDB[i]["Medidas"][j]["sensorType"]==0){
                        soil_humidity.push([date, dataOfMDB[i]["Medidas"][j]["measure"]]);
                    }
                }   
                measure = [date, null, null, temperature, humidity, precipitation];
                returnOfFunction.push(measure);

            }
        }
    }
    
    measure = markDivition;
    returnOfFunction.push(measure);
    return [returnOfFunction, soil_humidity];
}




function errorGetData(){
    $("#loadingLabelForecast").empty();

    console.log("Error al traer la semana pasada de datos de mongoDB");
    
}




function parseCSV(str) {
    var arr = [];
    var quote = false;  // true means we're inside a quoted field

    // iterate over each character, keep track of current row and column (of the returned array)
    for (var row = col = c = 0; c < str.length; c++) {
        var cc = str[c], nc = str[c+1];        // current character, next character
        arr[row] = arr[row] || [];             // create a new row if necessary
        arr[row][col] = arr[row][col] || '';   // create a new column (start with empty string) if necessary

        // If the current character is a quotation mark, and we're inside a
        // quoted field, and the next character is also a quotation mark,
        // add a quotation mark to the current column and skip the next character
        if (cc == '"' && quote && nc == '"') { arr[row][col] += cc; ++c; continue; }  

        // If it's just one quotation mark, begin/end quoted field
        if (cc == '"') { quote = !quote; continue; }

        // If it's a comma and we're not in a quoted field, move on to the next column
        if (cc == ',' && !quote) { ++col; continue; }

        // If it's a newline (CRLF) and we're not in a quoted field, skip the next character
        // and move on to the next row and move to column 0 of that new row
        if (cc == '\r' && nc == '\n' && !quote) { ++row; col = 0; ++c; continue; }

        // If it's a newline (LF or CR) and we're not in a quoted field,
        // move on to the next row and move to column 0 of that new row
        if (cc == '\n' && !quote) { ++row; col = 0; continue; }
        if (cc == '\r' && !quote) { ++row; col = 0; continue; }

        // Otherwise, append the current character to the current column
        arr[row][col] += cc;
    }
    return arr;
}


