<?php

    //PHP que se ejecuta para obtener los datos de logueo, se revisa la base de 
    //datos para ver si los campos ingresados fueron correctos
    
    session_start();
    //Incluyo las clases externas y configuración
    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");
    
    $userId = $_SESSION['keyhash'];
    
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);
    
    if ($conn->conectar()){
        $respuesta = array();
        
        //Creo la consulta a ejecutar
        $parametros = array();
        $sql = "SELECT * FROM Dispositivos";
        $sql .= " WHERE keyhash LIKE :userId";
        
        //Defino array de parámetros
        $parametros[0] = array("userId",$userId,"string",30);        
        
        //Ejecuto la consulta y verifico
        if($conn->consulta($sql, $parametros)){
            $resultado = $conn->restantesRegistros();
            $respuesta["result"] = "OK";
            $respuesta["Estaciones"]=$resultado;
            $respuesta["key"]=$userId;
        }else{ 
            //$respuesta["result"] = "NOOK";
            $respuesta["result"] = "ERROR CON SQL: " . $conn->ultimoError();
        }
    }
    else{
        $respuesta["result"] =  "ERROR DE CONEXIÓN AL HACER LA CONSULTA DE USUARIO";
    }  
    
    $dataBase=DATABASE;
    $scheme=SCHEME;
    
    $entro=false; 
    $url="mongodb://".AWSIp;
    
    try  
    {    
        $connection = new MongoClient($url);
        $entro=true;
    } 
    catch ( MongoConnectionException $e ) 
    {
        trigger_error('Mongodb not available', E_USER_ERROR);
        echo '<p>Problema en MongoDB</p>';
        exit();
    }
    
    if($entro){
        $stationsData = array();
        $station = array();
        $collection = $connection->$dataBase->$scheme;

        $rangeQuery = array('header.endpointKeyHash.string'=>$respuesta["key"]);
        $result = $collection->find($rangeQuery)->sort( array('event.timeStamp' => -1 ))->limit($_SESSION['endpoints'] - 1);
       
        foreach ($result as $parameter) {        
            $station["Estacion"] = $parameter["event"]["MAC"];
            $station["Hora"] = $parameter["event"]["timeStamp"];
            $station["Medidas"] =$parameter["event"]["sensores"];
          
            array_push($stationsData, $station);
            
        }
        $respuesta["stationsData"]=$stationsData;
        $respuesta["result"]="OK";
        $respuesta["keyHash"]=$userId;
    }
    echo json_encode($respuesta);
?>