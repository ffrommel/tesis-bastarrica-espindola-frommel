<?php   
    if (!session_start()){
        session_start();
    }
    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");
    
    $miSmarty = new Smarty();
    $miSmarty->template_dir = "templates";
    $miSmarty->compile_dir = "templates_c"; 
    
    if ($_SESSION['entro']){
        $areaPrivada = TRUE;
        $miSmarty->assign("areaPrivada",$areaPrivada);
    }else{
        $miSmarty->assign("mensaje",$_SESSION['msg']);
    }
  
    $inputBackTimeFrom = $_POST['inputBackTimeFrom'];
    $inputBackTimeTo = $_POST['inputBackTimeTo'];
    $timeFrom = $_POST['timeFrom'];
    $timeTo = $_POST['timeTo'];

    $dataBase=DATABASE;
    $scheme=SCHEME;
    
    $entro=false; 
    $respuesta = array();
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
         $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);
    
        if ($conn->conectar()){

            $sql = "SELECT * FROM Dispositivos ";
            $sql .= "WHERE keyhash LIKE :keyhash";
            $parametros = array();
            array_push($parametros, array("keyhash",$_SESSION['keyhash'],"string",20));

            if($conn->consulta($sql, $parametros)){
                $listEndpoints = $conn->restantesRegistros();
                $respuesta["resultEndpoints"]="OK";
                $respuesta["listEndpoints"]= $listEndpoints;

            }else{
                $respuesta["resultEndpoints"]="NOTOK";
                echo "ERROR CON SQL: " . $conn->ultimoError();
            }
        }
        $stationsData = array();
        $station = array();
        $collection = $connection->$dataBase->$scheme;
        $rangeQuery = array('event.timeStamp' => array( '$gt' => $inputBackTimeFrom, '$lt' => $inputBackTimeTo), 'header.endpointKeyHash.string'=>$_SESSION['keyhash']);
        $result = $collection->find($rangeQuery);

        foreach ($result as $parameter) {        
            $station["Estacion"] = $parameter["event"]["MAC"];
            $station["Hora"] = $parameter["event"]["timeStamp"];
            $station["Medidas"] =$parameter["event"]["sensores"];
          
            array_push($stationsData, $station);
            
        }
        $respuesta["timeFrom"]=$timeFrom;
        $respuesta["timeTo"]=$timeTo;
        $respuesta["numberOf"]=sizeof($stationsData[0]["Medidas"]);
        $respuesta["result"]="OK";
        $respuesta["Estaciones"]=$stationsData;
        $respuesta["From"]=$inputBackTimeFrom;
        $respuesta["To"]=$inputBackTimeTo;
        $respuesta["keyhash"]=$_SESSION['keyhash'];
        
        echo json_encode($respuesta);
    }

?>
  