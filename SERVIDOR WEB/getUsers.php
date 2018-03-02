<?php

    //PHP que se ejecuta para obtener los datos de logueo, se revisa la base de 
    //datos para ver si los campos ingresados fueron correctos
    
    session_start();
    //Incluyo las clases externas y configuración
    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");
    
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);
    
    if ($conn->conectar()){
        
        $sql = "SELECT * FROM Usuarios";
        $parametros = array();

        if($conn->consulta($sql, $parametros)){
            $listUsers = $conn->restantesRegistros();
            $respuesta["result"]="OK";
            $respuesta['listUsers']= $listUsers;

            //$miSmarty->assign("listUsers",$listUsers);

        }else{
            $respuesta["result"]="NOTOK";
            echo "ERROR CON SQL: " . $conn->ultimoError();
        }



    }else{
        $respuesta["result"] =  "ERROR DE CONEXIÓN AL TRAER LISTA USUARIOS";
    } 
    echo json_encode($respuesta);
?>