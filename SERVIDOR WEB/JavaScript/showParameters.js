$(document).ready(initialize);
//
//setInterval(initialize,3000);
//Función que se ejecuta al iniciar



function initialize(){
    $("#actualSamplePeriod").empty();        
    getSamplePeriod();
    $("#btnNewSamplePeriod").click(configureNewSamplePeriod);
}

/////////////////////////////////LISTADO///////////////////////////////////

function getSamplePeriod(){
    
    $.ajax({
        url: "showParameters.php", 
        type: "GET",
        dataType: "JSON",
        success: showParameters,
        timeout: 40000,
        error: errorParameters,
        data: {}

    })
    	
}


//Error al traer página
function errorParameters(){
    mostrarError("ERROR EN PHP AL OBTENER parametros");
}

function showParameters(datos){
console.log("samplePeriod: "+datos["samplePeriod"]+".");

    var actualSamplePeriod=datos["samplePeriod"].substring(datos["samplePeriod"].indexOf("samplePeriod")+15,datos["samplePeriod"].indexOf("__uuid")-3);
console.log("samplePeriod:"+actualSamplePeriod);    
    $("#actualSamplePeriod").html(actualSamplePeriod);        
    
}

function configureNewSamplePeriod(){

    var newSamplePeriod=$("#inputNewSamplePeriod").val();
      $.ajax({
        url: "changeSamplePeriod.php", 
        type: "POST",
        dataType: "JSON",
        success: showNewSamplePeriod,
        timeout: 40000,
        error: errorNewSamplePeriod,
        data: {newSamplePeriod:newSamplePeriod}

    })
}

//Error al traer página
function errorNewSamplePeriod(){
    mostrarError("ERROR EN PHP AL OBTENER NEWSAMPLEPERIOD");
}

function showNewSamplePeriod(datos){
    console.log(datos["id"]);
    var id=datos["id"].substring(datos["id"].indexOf(": ")+2,datos["id"].indexOf("\"applicationId")-4);
    $.ajax({
        url: "activeNewParameters.php", 
        type: "POST",
        dataType: "JSON",
        success: showActivateNewParameters,
        timeout: 40000,
        error: errorActivateNewParameters,
        data: {id:id}

    })
}

function showActivateNewParameters(datos){
    
    getSamplePeriod();
    
}

//Error al traer página
function errorActivateNewParameters(){
    mostrarError("ERROR EN PHP AL OBTENER ACTIVNEWSAMPLEPERIOD");
}