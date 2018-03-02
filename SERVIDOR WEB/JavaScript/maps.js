$(document).ready(initialize);

//setInterval(initialize,3000);
//Función que se ejecuta al iniciar
function initialize(){
$("#btnChangeColorFilter").click(callMap);
    
}

function callMap(){
    console.log("Entro a CallMap");
    $.ajax({
        url: "maps.php",
        type: "POST",
        dataType: "JSON",
        success: showMap,
        timeout: 4000,
        error: errorMap,
        data: {}
    });
}

//Error al traer página
function errorMap(){
    mostrarError("ERROR EN PHP AL OBTENER EL LISTADO DE COORDENADAS");
}

function showMap(datos){

    console.log("Resultados:", datos["stationsData"]);
    console.log("Estaciones:", datos["Estaciones"]);

    if(datos["result"]=="OK"){ 
        
        if(datos["Estaciones"].length==0){
            $("#labelMap").html("No hay equipos registrados");
        }else{
            var gatewayPos=[];
            var stations = datos["Estaciones"].sort();
            var stationsData = datos["stationsData"];
            var infoEndpoints=[];
            var j,h = 0;
            var stationFound = false;
            for(var i=0;i<stations.length;i++){

                stationFound = false; 
                j = 0;

                if(stations[i]["0"]=="0"){ 
                    gatewayPos["Latitud"]=parseFloat(stations[i]["1"]);
                    gatewayPos["Longitud"]=parseFloat(stations[i]["2"]);
                    gatewayPos ["nroDispositivo"]="0";
                    infoEndpoints.push(gatewayPos);

                }else{
                    while((j<stationsData.length+1) && !stationFound){
                        if (j==stationsData.length){
                            h=j-1;
                            
                        }else{
                            h=j;
                        }
                        if(stationsData[h]["Estacion"]==stations[i]["MAC"]){
                            infoEndpoints.push({"Latitud":stations[i]["latitud"],"Longitud":stations[i]["longitud"],
                                "nroDispositivo":stations[i]["nroDispositivo"],"activo":stations[i]["activo"],
                                "Medidas":stationsData[h]});
                            stationFound = true;
                            
                        }else{
                            if(j==stationsData.length){
                                infoEndpoints.push({"Latitud":stations[i]["latitud"],"Longitud":stations[i]["longitud"],
                                    "nroDispositivo":stations[i]["nroDispositivo"],"activo":stations[i]["activo"],
                                    "Medidas":"No data"});
                                stationFound=true;
                            }
                            j++;
                        }    
                    }
                }    
            }

            $("#labelMap").html("Cantidad de equipos en el campo: "+stations.length);
            infoEndpoints.reverse();
            console.log(infoEndpoints);
            initMap(infoEndpoints,gatewayPos);        
        }
    }
}
