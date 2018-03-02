$(document).ready(initialize);
//
//setInterval(initialize,3000);
//Función que se ejecuta al iniciar

function initialize(){
    $("#listOfUsers").empty();
    showListUsers();
}

/////////////////////////////////LISTADO///////////////////////////////////
function showListUsers(){

    $.ajax({
        url: "getUsers.php",
        type: "POST",
        dataType: "JSON",
        success: showListOfUsers,
        timeout: 4000,
        error: errorListOfUsers, 
        data: {}
        
    });

} 


function showListOfUsers(datos){
    if(datos["result"]=="OK"){
       
        var users = datos["listUsers"];
        console.log(users.length);
        
        if(users.length!=0){
            $("#labelListOfUsers").html("Total de usuarios registrados: "+ users.length);
            var text="<dl style='list-style-type:none'>";
            for(i = 0 ; i < users.length ; i++){
                
                text += "<dt>Usuario: "+users[i]["user"]+"</dt>";                
                text += "<dd>---> Keyhash: "+users[i]["keyhash"]+"</dd>";                
                text += "<dd>------>Endpoints: "+users[i]["dispositivos"]+"</dd><br>";                

            }
            text += "</dl>";
            console.log("Text: ",text);
            $("#listOfUsers").append(text);
            //$("#labelGraph").html("Se encontraron "+stations.length+" registros de "+sortStations.length+" sistemas desde "+dateFrom+" hasta "+dateTo);
        }else{
            $("#labelListOfUsers").empty();
            $("#labelListOfUsers").html("No hay ususuarios");

        } 
         
    }else{
        $("#labelListOfUsers").html("Error en SQL usuarios");
    }
     
}

//Error al traer página
function errorListOfUsers(){
    mostrarError("ERROR EN PHP AL OBTENER EL LISTADO DE USUARIOS");
}