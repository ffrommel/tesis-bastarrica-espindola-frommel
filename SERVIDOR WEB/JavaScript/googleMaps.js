var gatewayHum = 200;

function initMap(coord,gatewayPos) {
    var radioEndpoints=[];

    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: gatewayPos["Latitud"], lng: gatewayPos["Longitud"]},
        zoom: 20,
        mapTypeId: 'terrain'
    });
    var infoWindow = new google.maps.InfoWindow({map: map});
    
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };

        infoWindow.setPosition(pos);
        infoWindow.setContent('Usted está aquí.');
        map.setCenter(pos);
        }, 
    
        function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
      // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }    
    for(var i=0; i<coord.length;i++){           
        radioEndpoints.push(initDots(coord[i],map));
    }
            // Construct the circle for each value in citymap.
        // Note: We scale the area of the circle based on the population.
    var radioColorRed= '#FF0000';
    var radioColorGreen= '#00FF00';
    var radioColorYellow= '#FFFF00';
    var radioColorBlue= '#0000FF';
    
    
    
    var radioMaxColor=$("#mapHumMax").val();
    var radioMinColor=$("#mapHumMin").val();

    if (radioMaxColor != ""){
        for (var endpoint in radioEndpoints) { 
            
            if(radioEndpoints[endpoint].parameter != "No data"){
            
                if (radioEndpoints[endpoint].parameter==gatewayHum){
                    radioColor=radioColorBlue;

                }else if(radioEndpoints[endpoint].parameter > radioMaxColor){
                    radioColor=$("#colorMax").val();
                }else if((radioEndpoints[endpoint].parameter < radioMaxColor) && (radioEndpoints[endpoint].parameter >= radioMinColor)){
                    radioColor=radioColorYellow;
                }
                else{
                    radioColor=$("#colorMin").val();
                }
                //console.log(radioColor);
                // Add the circle for this city to the map. 
                var endpointCircle = new google.maps.Circle({
                  strokeColor: radioColor,
                  strokeOpacity: 0.8,
                  strokeWeight: 2,
                  fillColor: radioColor,
                  fillOpacity: 0.35,
                  map: map,
                  center: radioEndpoints[endpoint].center,
                  radius: Math.sqrt(1) * 100
                  //radius: Math.sqrt(radioEndpoints[endpoint].range) * 100
                });
            }
        }    
    }
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}




function initDots(myLatLng,map) {
    var sensorTypes = {"0":"Humedad del Suelo","1":"Temperatura del Suelo",
                        "2":"Humedad del ambiente", "3":"Temperatura del ambiente",
                        "4":"Detección de lluvia", "6":"RSSI"};

    var coord=[];
    console.log(myLatLng["nroDispositivo"]);
    var stationNumber="Endpoint "+ myLatLng["nroDispositivo"] + "\n";
    
    if(myLatLng["activo"]==0){
        stationNumber+="Inactivo"+ "\n";
    }
    coord["lat"]=parseFloat((myLatLng["Latitud"]));
    coord["lng"]=parseFloat((myLatLng["Longitud"]));
 
    var parameter = "No data";
    if(myLatLng["nroDispositivo"]=="0"){
        stationNumber = "Gateway";
        var pinColor = "2569FE";
        parameter = gatewayHum;
    }else{
        //console.log(new Date(parseInt(myLatLng["Medidas"]["Hora"])*1000));
        if(myLatLng["Medidas"]=="No data"){
            stationNumber+="No se encontraron datos recientes de este Endpoint";
            parameter = "No data";
        }else{
            stationNumber+=spanishDate(new Date(parseInt(myLatLng["Medidas"]["Hora"])*1000)) + "\n";
            for(var i = 0; i < myLatLng["Medidas"]["Medidas"].length; i++){
                stationNumber+=typeOfSensor(myLatLng["Medidas"]["Medidas"][i]["sensorType"],sensorTypes)+
                        " "+myLatLng["Medidas"]["Medidas"][i]["measure"]+"\n";
               
                if(typeOfSensor(myLatLng["Medidas"]["Medidas"][i]["sensorType"],sensorTypes)==sensorTypes[$("#mapParameter").val()]){
                    parameter=parseInt(myLatLng["Medidas"]["Medidas"][i]["measure"]);
                }
            }
        }
        var pinColor = "FE2569";
        if ((myLatLng["activo"])=="1"){
            var pinColor = "25FE69";
        }
        
    }
    
    
    var pinImage = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + pinColor,
        new google.maps.Size(21, 34),
        new google.maps.Point(0,0),
        new google.maps.Point(10, 34));
    var pinShadow = new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_shadow",
        new google.maps.Size(40, 37),
        new google.maps.Point(0, 0),
        new google.maps.Point(12, 35));
        
    var marker = new google.maps.Marker({
        position: coord,
        map: map,
        icon: pinImage,
        shadow: pinShadow,
        title: stationNumber
    });
    var returnRadioEndpoint={center:{lat: coord["lat"], lng: coord["lng"]}, range: myLatLng["nroDispositivo"]+1, parameter: parameter};
    return returnRadioEndpoint;
}

function spanishDate(d){
    var weekday=["Domingo","Lunes","Martes","Miercoles","Jueves","Viernes","Sabado"];
    var monthname=["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"];
    var time = d.toString();
    return weekday[d.getDay()]+" "+d.getDate()+" de "+monthname[d.getMonth()]+" de "+d.getFullYear()+ " " + time.split(" ")[4];
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

