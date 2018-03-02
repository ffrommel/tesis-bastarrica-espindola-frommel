$(document).ready(inicializo);

//Función que inicializa cabezal.js
function inicializo(){
    $("#info").hide();
    $("#infoModal").click(mostrarInfo);
    $("#cancelarInfo").click(cancelarInfo);
    $("#botonLogin").focus();
    
    $("#modalNewClient").hide();
    $("#newClient").click(mostrarNewClient);
    $("#botonNewClient").click(newClient);
    $("#cancelarNewClient").click(cancelarNewClient);

    $("#id01").hide();
    $("#login").click(mostrarRegistro);
    $("#botonLogin").click(login);
    $("#cancelarLogin").click(cancelarLogin); 
     
    $("#modalNewEndpoint").hide();
    $("#newEndpoint").click(mostrarNewEndpoint);
    $("#botonNewEndpoint").click(newEndpoint);
    $("#cancelarNewEndpoint").click(cleanNewEndpointModal);

}
//Se depliega un modal con el texto de error devuelto por SQL via PHP


////////////MODAL ADVERTENCIA/////////////////
function mostrarAdvertencia (texto){
    var text="";
    text+="<label>"+texto+"</label>";
    
    $("#textoAdvertencia").empty();
    $("#textoAdvertencia").append(text);
    $("#advertencia").show();
}

function cerrarModalAdvertencia(){
    $("#advertencia").hide();
}
///////////////////////////////////////////////

//Se depliega un modal con el texto de error devuelto por SQL via PHP
function mostrarError (texto){
    var text="";
    text+="<label>"+texto+"</label>";
    text+="</br></br><label class='w3-right  w3-text-blue'>Lamentamos las molestias. Intente nuevamente en un rato</label>";
    
    $("#textoError").empty();
    $("#textoError").append(text);
    $("#errores").show();
}

//Cierra el modal de errores de SQL
function cerrarModalError(){
    $("#errores").hide();
    window.location.href = "/Tesis/index.php";
}



/////////////LOGIN//////////////////////////
function mostrarRegistro(){
    $("#id01").show();
    $("#txtUsu").focus();
}

function login(){
    $("#usuarioIncorrecto").html("");
    var txtUsu = $("#txtUsu").val();
    var txtPass = $("#txtPass").val();
    
    if (txtUsu!="" && txtPass!=""){
        $.ajax({
            url: "login.php",
            type: "POST",
            dataType: "json",
            success: respuestaLogin,
            timeout: 4000,
            error: errorLogin,
            data: {txtUsu:txtUsu,txtPass:txtPass}
        });
    }else{
        $("#usuarioIncorrecto").html("Debe completar los campos");
    }
}

function respuestaLogin(datos){
    console.log(datos["Access"]);
    //console.log(datos["listUsers"]);
    
    if(datos["result"]=="OK"){       
        if(datos["Access"]=="OK"){
            $("#id01").hide();

            location.reload(); //CORREGIR

        } else if(datos["Access"]=="NOOK"){
            console.log("NOOK ACCESS");
            $("#usuarioIncorrecto").html("Usuario o Contraseña incorrectos");
        }
    } else {
        mostrarError(datos["result"]);
    }
}

function errorLogin(){
    mostrarError("ERROR EN PHP AL HACER LA CONSULTA DE USUARIO");
}

function cancelarLogin (){ 
    $("#id01").hide();
    $("#usuarioIncorrecto").html("");
    $("#txtPass").val("");
}
///////////////////////////////////////////////////////

/////////////MODAL INFO////////////////////////////////
function mostrarInfo(){
    $("#info").show();
}
function cancelarInfo (){
    $("#info").hide();
    
}
///////////////////////////////////////////////////////


/////////////////////NEW CLIENT//////////////////////////
function mostrarNewClient(){
    $("#modalNewClient").show();
    $("#txtUsuNewClient").empty();
    $("#txtPassNewClient").empty();
    $("#txtIdNewClient").empty();
    $("#txtUsuNewClient").focus();
    $("#userExist").html(""); 
}

function newClient(){
    $("#usuarioIncorrecto").html("");
    var txtUsuNewClient = $("#txtUsuNewClient").val();
    var txtPassNewClient = $("#txtPassNewClient").val();
    var txtKeyNewClient = $("#txtKeyNewClient").val();
    if (txtUsuNewClient!="" && txtPassNewClient!="" && txtKeyNewClient!="" && 
            txtUsuNewClient.replace(/ /g,"")!="" && txtPassNewClient.replace(/ /g,"")!="" && txtKeyNewClient.replace(/ /g,"")!=""){
        $.ajax({
            url: "newClient.php",
            type: "POST",
            dataType: "json",
            success: respuestaNewClient,
            timeout: 4000,
            error: errorNewClient,
            data: {txtUsuNewClient:txtUsuNewClient,txtPassNewClient:txtPassNewClient,txtIdNewClient:txtKeyNewClient}
        });
    }else{
        $("#userExist").html("Debe completar los campos");
    }
}

function respuestaNewClient(datos){

    if(datos["result"]!="USEREXIST"){       
        if(datos["result"]=="OK"){       
                $("#modalNewClient").hide();
                $("#userExist").html(""); 
        } else {
            mostrarError(datos["result"]);
        }
    }else{
        $("#userExist").html("Nombre ya utilizado");    
    }
}

function errorNewClient(){
    mostrarError("ERROR EN PHP AL CREAR USUARIO");
}

function cancelarNewClient(){
    $("#modalNewClient").hide();
}
//////////////////////////////////////////////////////////////////

/////////////////////NEW ENDPOINT//////////////////////////
function mostrarNewEndpoint(){
    $("#modalNewEndpoint").show();

    $("#nroEndpoint").focus();
    $.ajax({
        url: "getUsers.php",
        type: "GET",
        dataType: "json",
        success: respuestaGetUsers,
        timeout: 4000,
        error: errorGetUsers,
        data: {}
    });
}


           
function respuestaGetUsers(datos){
    if(datos["result"]=="OK"){       
        var text ="";
        for(var i=0; i < datos["listUsers"].length; i++){
            text +="<option value='"+datos["listUsers"][i]["keyhash"]+"'>"+datos["listUsers"][i]["usuario"]+"</option>";       
        }
        $("#usersNewEndpoint").append(text);
            
    } else {
        mostrarError(datos["result"]);
    }
}

function errorGetUsers(){
    mostrarError("ERROR EN PHP AL TRAER LISTAENDPOINTS");
}




function newEndpoint(){
    $("#endpointIncorrect").html("");
    var nroEndpoint = $("#nroNewEndpoint").val();
    var latitudEndpoint = $("#latitudNewEndpoint").val();
    var longitudEndpoint = $("#longitudNewEndpoint").val();
    var userEndpoint = $("#usersNewEndpoint").val();
    var macEndpoint = $("#macNewEndpoint").val();
    var activeEndpoint=0;
    if(document.getElementById('activeNewEndpoint').checked){
        activeEndpoint=1;
    }

    if (nroEndpoint!="" && latitudEndpoint!="" && longitudEndpoint!="" && userEndpoint!="" && macEndpoint!=""){
        $.ajax({
            url: "newEndpoint.php",
            type: "POST",
            dataType: "json",
            success: respuestaNewEndpoint,
            timeout: 4000,
            error: errorNewEndpoint,
            data: {nroEndpoint:nroEndpoint,latitudEndpoint:latitudEndpoint,longitudEndpoint:longitudEndpoint,
                    userEndpoint:userEndpoint,macEndpoint:macEndpoint, activeEndpoint:activeEndpoint}
        });
    }else{
        $("#endpointIncorrect").html("Debe completar los campos");
    }
}

function respuestaNewEndpoint(datos){

    if(datos["result"]=="OK"){       
        cleanNewEndpointModal();
            
    } else {
        mostrarError(datos["result"]);
    }
}

function cleanNewEndpointModal(){
    $("#endpointIncorrect").html("");
    $("#usersNewEndpoint").empty();
    $("#latitudNewEndpoint").val("");
    $("#macNewEndpoint").val("");
    $("#nroNewEndpoint").val("");
    $("#longitudNewEndpoint").val("");
    document.getElementById('activeNewEndpoint').checked = false;
    $("#modalNewEndpoint").hide(); 
}

function errorNewEndpoint(){
    mostrarError("ERROR EN PHP AL CREAR Endpoint");
}

function cancelarNewEndpoint(){
    $("#modalNewEndpoint").hide();
}
//////////////////////////////////////////////////////////////////
