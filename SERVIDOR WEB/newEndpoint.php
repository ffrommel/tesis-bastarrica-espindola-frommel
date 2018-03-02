<?php

//Este php se utiliza para ingresar a la base de datos los datos correctos de la
//nueva propiedad haciendo un INSERT INTO con los valores deseados


    session_start();

    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");

    $nroEndpoint = $_POST['nroEndpoint'];
    $endpointLatitud = $_POST['latitudEndpoint'];
    $endpointLongitud = $_POST['longitudEndpoint'];
    $userEndpoint = $_POST['userEndpoint'];
    $MAC = $_POST['macEndpoint'];
    //$areaEndpoint = $_POST['areaEndpoint'];
    $activeEndpoint = $_POST['activeEndpoint'];

    $respuesta = array();
    $parametros = array();
    $resultadoUsers = array();
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);

    if($conn->conectar()){
        
        $sql = "INSERT INTO Dispositivos (nroDispositivo, latitud, longitud, keyhash, MAC, activo)";
        $sql .= " VALUES (:nroEndpoint, :latitud, :longitud, :idCliente, :MAC, :activo)";
        $parametros = array(
                array("nroEndpoint",$nroEndpoint,"int",20),
                array("latitud",$endpointLatitud,"double",50),
                array("longitud",$endpointLongitud,"double",50),
                array("idCliente",$userEndpoint,"string",30), 
                array("MAC",$MAC,"string",30),     
                //array("area",$areaEndpoint,"int",2), 
                array("activo",$activeEndpoint,"int",2)
                );
        
        if($conn->consulta($sql, $parametros)){
            $respuesta["parametros"]=$parametros;
            $respuesta["id_user"] = $conn->ultimoIdInsert();
            $respuesta["result"] = "OK";
      
        }
        else{
            $respuesta["result"] = "ERROR CON SQL: " . $conn->ultimoError();
        }
    }
    else{
        $respuesta["result"] = "ERROR DE CONEXIÓN AL DAR DE ALTA A UN USUARIO";
    }
    
    
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);

    if($conn->conectar()){
        
        $parametros = array();
        $sql = "SELECT * FROM Usuarios";
        $sql .= " WHERE keyhash LIKE :keyhash";
        $parametros[0] = array("keyhash",$userEndpoint,"string",30);        

        
        if($conn->consulta($sql, $parametros)){  
            $resultadoUsers = $conn->restantesRegistros();
            $respuesta["result"] = "OK";
            $sql = "UPDATE Usuarios";
            $sql .= " SET dispositivos=:nroEndpoints";
            $sql .= " WHERE keyhash LIKE :keyhash";
            $endpoints = $resultadoUsers[0]["endpoints"]+1;
            $parametros = array(
                array("nroEndpoints",$endpoints,"int",2),
                array("keyhash",$userEndpoint,"string",30)               
                );
            $respuesta["resultadoUsers"]=$resultadoUsers;
            $respuesta["endpointssss"]=$endpoints;
            $respuesta["Varendpoints"]=$resultadoUsers[0]["endpoints"]+1;
            
            if($conn->consulta($sql, $parametros)){
                $respuesta["keyhash"]=$userEndpoint;    
                $respuesta["id_userEndpoints"] = $conn->ultimoIdInsert();
                $respuesta["result"] = "OK"; 

            }
            else{
                $respuesta["result"] = "ERROR CON SQL DE SUMAR ENDPOINT: " . $conn->ultimoError();
            }
        
            
        }else{
            //$respuesta["result"] = "NOOK";
            $respuesta["result"] = "ERROR CON SQL EN USERS AL SUMAR ENDPOINT: " . $conn->ultimoError();
        }
    }
    else{
        $respuesta["result"] = "ERROR DE CONEXIÓN AL DAR DE ALTA A UN USUARIO";
    }
    echo json_encode($respuesta);

?>