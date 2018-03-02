<?php

//Este php se utiliza para ingresar a la base de datos los datos correctos de la
//nueva propiedad haciendo un INSERT INTO con los valores deseados


    session_start();

    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");

    $txtUsuNewClient = $_POST['txtUsuNewClient'];
    $txtPassNewClient = $_POST['txtPassNewClient'];
    $txtIdNewClient = $_POST['txtIdNewClient'];
    

    $respuesta = array();
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);
    
    if ($conn->conectar()){
        $respuesta = array();
        $parametros = array();
        $sql = "SELECT * FROM Usuarios";
        $sql .= " WHERE (usuario LIKE :usu) AND (keyhash Like :keyhash)";
        //Defino array de parámetros
        $parametros = array(
                        array("usu",$txtUsuNewClient,"string",20),
                        array("keyhash",$txtIdNewClient,"string",50)
                    );        

        //Ejecuto la consulta y verifico
        if($conn->consulta($sql, $parametros)){
            $resultado = $conn->restantesRegistros();
            $respuesta["resultado"]=$resultado;
            
            if(($resultado[0]["user"]!=$txtUsuNewClient) && ($txtUsuNewClient!="admin")){

                if($conn->conectar()){
                    $sql = "INSERT INTO Usuarios (usuario, contrasena, keyhash)";
                    $sql .= " VALUES (:user, :password, :keyhash)";
                    $respuesta = array();
                    $parametros = array(
                            array("user",$txtUsuNewClient,"string",20),
                            array("password",$txtPassNewClient,"string",20),
                            array("keyhash",$txtIdNewClient,"string",50)

                            );

                    if($conn->consulta($sql, $parametros)){

                        $respuesta["id_user"] = $conn->ultimoIdInsert() ;
                        $respuesta["result"] = "OK";
                        //$parametros=array();
                        

                    }
                    else{
                        $respuesta["result"] = "ERROR CON SQL: " . $conn->ultimoError();
                    }
                }
                else{
                    $respuesta["result"] = "ERROR DE CONEXIÓN AL DAR DE ALTA A UN USUARIO";
                }
            }else{
                $respuesta["result"] ="USEREXIST";
            }
        }
    }else{
        $respuesta["result"] =  "ERROR DE CONEXIÓN AL HACER LA CONSULTA DE USUARIO";
    } 
    $respuesta["user"]=$resultado[0]["user"];
    $respuesta["txt"]=$txtUsuNewClient;
    echo json_encode($respuesta);

?>