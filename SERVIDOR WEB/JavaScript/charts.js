$(document).ready(initialize);
var GMTZone = 3;

function initialize(){
    $("#stationsResult").empty();
    $("#labelGraph").empty();
    google.charts.setOnLoadCallback(iniCharts);
    $("#btnSearchByMonth").click(goPage);
}

/////////////////////////////////LISTADO///////////////////////////////////
function iniCharts(){
    
    var daysBack = 60;
    var miliSecondsBack = daysBack*60*60*24*1000;
    var date = new Date();
    var dateNow = new Date(date.getTime());
    var datePast = new Date((date.getTime())-miliSecondsBack);
    
    var pastMinutes = add0ToNumber(datePast.getMinutes());
    var pastHours = add0ToNumber(datePast.getHours());
    var currentMinutes = add0ToNumber(dateNow.getMinutes());
    var currentHours = add0ToNumber(dateNow.getHours());
    
    var timeFrom = ""+pastHours+":"+pastMinutes+"";
    console.log(timeFrom);
    var timeTo = timeFrom;
    var inputBackTimeFrom=parseInt(datePast / 1000);
    var inputBackTimeTo=parseInt(dateNow / 1000);
    
    var currentMonth = add0ToNumber(dateNow.getMonth()+1);
    var currentDay = add0ToNumber(dateNow.getDate());
    var pastMonth = add0ToNumber(datePast.getMonth()+1);
    var pastDay = add0ToNumber(datePast.getDate());
    
    $("#inputBackTimeFrom").empty();
    $("#inputBackTimeTo").empty();
    $("#inputBackTimeFrom").val(""+datePast.getFullYear()+"-"+pastMonth+"-"+pastDay+"");
    $("#inputBackTimeTo").val(""+dateNow.getFullYear()+"-"+currentMonth+"-"+currentDay+"");
    $("#inputTimeBackTimeFrom").val(""+pastHours+":"+pastMinutes+""); 
    $("#inputTimeBackTimeTo").val(""+currentHours+":"+currentMinutes+"");
    $("#stationsResult").empty();
    $("#labelGraph").empty();
    $("#loadingLabelGraphs").html("Cargando gráficos...");
    $.ajax({
        url: "charts.php",
        type: "POST",
        dataType: "JSON",
        success: showChart,
        timeout: 40000,
        error: errorChart, 
        data: {inputBackTimeFrom:inputBackTimeFrom, inputBackTimeTo:inputBackTimeTo, timeFrom:timeFrom, timeTo:timeTo}
    });
} 



function goPage(){
    var timeFrom = $("#inputTimeBackTimeFrom").val();
    var timeTo = $("#inputTimeBackTimeTo").val();
    var timeFromSplit= timeFrom.split(":");
    var timeToSplit= timeTo.split(":");
    
    var timeFromUnix = ((timeFromSplit[0])*60*60)+(timeFromSplit[1]*60) + (GMTZone*60*60);
    var timeToUnix = ((timeToSplit[0])*60*60)+(timeToSplit[1]*60) + (GMTZone*60*60);
    console.log("timeFromUnix: ",timeFromUnix);
    console.log("timeToUnix: ",timeToUnix);
    
    var inputBackTimeFrom=(new Date($("#inputBackTimeFrom").val()).getTime() / 1000) + timeFromUnix;
    var inputBackTimeTo=(new Date($("#inputBackTimeTo").val()).getTime() / 1000)+timeToUnix;

    $("#stationsResult").empty();
    $("#labelGraph").empty();

    if($("#inputBackTimeFrom").val() == "" || $("#inputBackTimeTo").val() == ""){
        $("#labelGraph").html("Ingrese Fechas válidas");
    }else{
        $("#loadingLabelGraphs").html("Cargando gráficos...");
        $.ajax({
            url: "charts.php",
            type: "POST",
            dataType: "JSON",
            success: showChart,
            timeout: 40000,
            error: errorChart, 
            data: {inputBackTimeFrom:inputBackTimeFrom, inputBackTimeTo:inputBackTimeTo, timeFrom:timeFrom, timeTo:timeTo}
        });
    }
}

//Error al traer página
function errorChart(){
    mostrarError("ERROR EN PHP AL OBTENER EL LISTADO DE ESTACIONES");
}

function showChart(datos){
    console.log("$respuesta['$listEndpoints']",datos["listEndpoints"]);
    $("#loadingLabelGraphs").empty();
    var sensorTypes = {"0":"Humedad del Suelo","1":"Temperatura del Suelo",
                        "2":"Humedad del ambiente", "3":"Temperatura del ambiente",
                        "4":"Detección de lluvia", "6":"RSSI"};
    if(datos["result"]=="OK"){
        
        var dateFrom = spanishDate(new Date(datos["From"]*1000));
        var dateTo = spanishDate(new Date(datos["To"]*1000));
        var text="";
        var nStations=[];
        var hora = 0;
        var temp = 0; 
        var station;
        var stations = datos["Estaciones"];
        var typeOfSensorAux;
        var haveSensor = false;
        var numberOfSensor;
        var k = 0;
        
        if(stations.length!=0){
            var sortStationsKeyTime = stations.sort(function(a, b){return a.Hora > b.Hora}); 
            var sortStationsKey = sortStationsKeyTime.sort(function(a, b){return a.Estacion > b.Estacion}); 
            var resultOfStationsLabels = stationsLabels(sortStationsKey,datos["listEndpoints"]);
            var sortStationsLabels = resultOfStationsLabels[1];
            var numberOfSensors = resultOfStationsLabels[2];
            var stationNumber  = resultOfStationsLabels[0];

            console.log(resultOfStationsLabels);
            var i,j,h,measure = 0;
            
            for(h = 0; h < sortStationsLabels.length; h++){

                for(i=0;i<numberOfSensors[h].length;i++){
                    numberOfSensor = numberOfSensors[h][i];
                    nStations=[];
                    text = "";
                    
                    for(j=0;j<stations.length;j++){
                        station=stations[j];
                        haveSensor = false;
                        k = 0;
                        while((k < station["Medidas"].length) && (!haveSensor)){
                        
                            if(station["Medidas"][k]["sensorType"]==numberOfSensor){
                                haveSensor = true;
                                
                            }
                            k++;
                        }
                        
                        if(station["Estacion"]==sortStationsLabels[h]){
                            if(haveSensor){
                              
                                hora=(station["Hora"]);
                                measure=parseInt(station["Medidas"][k-1]["measure"]);
                                nStations.push([hora,measure]);
                                typeOfSensorAux = typeOfSensor(station["Medidas"][k-1]["sensorType"], sensorTypes);
                            }
                        }
                    }  
                    if(i==0){
                        text += "<h3 class='chartTitle'>Endpoint "+stationNumber[h]+"</h3>";                
                        text += "<h5 class='chartTitle'>Cantidad de registros con la MAC "+sortStationsLabels[h]+" : "+nStations.length+"</h5>";                
                    }
                    if(haveSensor){
                        text += "<div id='stationDiv"+sortStationsLabels[h]+i+"' class='divFadeIn'>";
                        text += "<br><br><label class='chartTitle'>Tipo de sensor : "+typeOfSensorAux+"</label><br>";                
                        text += "<div id='chart_div"+sortStationsLabels[h]+i+"'></div>";
                        text += "<hr></div>";
                        $("#stationsResult").append(text);
                        drawBasic(nStations,sortStationsLabels[h],i,typeOfSensorAux);
                    }
                }
            }
            if(sortStationsLabels.length==1){
                $("#labelGraph").html("Se encontraron "+stations.length+" registros de un solo sistema desde "+dateFrom+" "+datos["timeFrom"]+" hasta "+dateTo+" "+datos["timeTo"]);
            }else{
                $("#labelGraph").html("Se encontraron "+stations.length+" registros de "+sortStationsLabels.length+" sistemas desde "+dateFrom+" "+datos["timeFrom"]+" hasta "+dateTo+" "+datos["timeTo"]);
            }
        }else{
            $("#labelGraph").empty();
            $("#labelGraph").html("No hay registros para esas fechas");

        } 
         
    }
     
}

function stationsLabels(stations, stationNumbers){
    var stationArrayLabels=[];
    var sensorsArray=[];
    var pos = 0;
    var stat=[];
    var numberOfSensors = [];
    var uniqueStat = [];
    var returnArray = [];
    var typeOfSensors = [];
    var arrayTypeOfSensors = [];
    var numberOfStations = [];
    var changeOfStation = false;
    var station;
    for (pos = 0; pos < stations.length; pos++){
        changeOfStation = false;
        stat[pos]=stations[pos]["Estacion"];
        station = stations[pos];
        numberOfSensors[pos]=stations[pos]["Medidas"].length;
        
        if(pos == 0){
            numberOfStations.push(pos);
            for(var i = 0; i < numberOfSensors[pos]; i++){
                typeOfSensors.push(station["Medidas"][i]["sensorType"]);
            }
        }else{
            if(stat[pos] != stat[pos-1]){
                numberOfStations.push(pos);
                changeOfStation = true;
            }
            for(var i = 0; i < numberOfSensors[pos]; i++){
                if(changeOfStation){                    
                    arrayTypeOfSensors.push(typeOfSensors);
                    typeOfSensors=[];
                    for(var h = 0; h < numberOfSensors[pos]; h++){
                        typeOfSensors.push(station["Medidas"][h]["sensorType"]);
                    }
                    changeOfStation = false;
                }else{
                    if(!typeOfSensors.includes(station["Medidas"][i]["sensorType"])){
                        typeOfSensors.push(station["Medidas"][i]["sensorType"]);
                    }
                }    
            }
        }
    }
    arrayTypeOfSensors.push(typeOfSensors);
    
    for(var i = 0; i < numberOfStations.length; i++){
        sensorsArray.push(stations[numberOfStations[i]]["Medidas"].length);
    }
    
    $.each(stat, 
        function(i, el){
            if($.inArray(el, stationArrayLabels) === -1) stationArrayLabels.push(el);
        }
    );

    return getStationNumber(stationNumbers, stationArrayLabels, arrayTypeOfSensors);
}


function spanishDate(d){
    var weekday=["Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"];
    var monthname=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    return weekday[d.getDay()]+" "+d.getDate()+" de "+monthname[d.getMonth()]+" de "+d.getFullYear();
}

function typeOfSensor(station, sensorTypes){
    switch(station){
        case 0:
            return sensorTypes["0"];
            break;
        case 1:
            return sensorTypes["1"];
            break;
        case 2:
            return sensorTypes["2"];
            break;
        case 3:
            return sensorTypes["3"];
            break;
        case 4:
            return sensorTypes["4"];
            break;
        case 5:
            return sensorTypes["5"];
            break;
        case 6:
            return sensorTypes["6"];
            break;
    }
}


function add0ToNumber(number){

    if (number< 10){
        return "0"+number;
    }else{
        return number;
    }
}

function getStationNumber(stationNumbers, stationsMacs, arrayTypeOfSensors){
    var numbers = [];
    var stations = stationNumbers.sort(function(a, b){return a.nroDispositivo > b.nroDispositivo});
    var macs = [];
    var type = [];
    var aux = [];
    for(var i = 0; i < stations.length; i++){
        if(stations[i]["nroDispositivo"] != 0){
            aux.push(stations[i]);
        }
    }
    
    for(var i = 0; i < aux.length; i++){

        for(var h = 0; h < stationsMacs.length; h++){
        
            if((stationsMacs[h] == aux[i]["MAC"])){
                numbers.push(aux[i]["nroDispositivo"]);
                macs.push(aux[i]["MAC"]);
                type.push(arrayTypeOfSensors[h]);
                                
            }
        }
    }
    var returnArray = [];
    returnArray[0] = numbers;
    returnArray[1] = macs;
    returnArray[2] = type;
    return returnArray;
}

