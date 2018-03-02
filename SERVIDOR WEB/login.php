<?php

    //PHP que se ejecuta para obtener los datos de logueo, se revisa la base de 
    //datos para ver si los campos ingresados fueron correctos
    
    session_start();
    //Incluyo las clases externas y configuración
    require_once("includes/class.Conexion.BD.php");
    require_once("includes/smarty/libs/Smarty.class.php");
    require_once("config/configuracion.php");
    
    $user = $_POST['txtUsu'];
    $password = $_POST['txtPass'];
    $conn = new ConexionBD("mysql", MYSQLSERVER, MYSQLDATABASE, MYSQLUSER, MYSQLPASS);
    
    $miSmarty = new Smarty();

    $miSmarty->template_dir = TEMPLATEDIR;
    $miSmarty->compile_dir = COMPILEDIR;

    
    if ($conn->conectar()){
        $respuesta = array();
        
        //Creo la consulta a ejecutar
        $parametros = array();
        $sql = "SELECT * FROM Usuarios";
        $sql .= " WHERE usuario LIKE :usu";
        //Defino array de parámetros
        $parametros[0] = array("usu",$user,"string",20);        
        
        //Ejecuto la consulta y verifico
        if($conn->consulta($sql, $parametros)){ 
            $resultado = $conn->restantesRegistros();
            $respuesta["result"] = "OK";
            if($resultado[0][contrasena] == $password && $resultado[0][contrasena] != "" && $resultado[0][usuario] != ""){ 
                $_SESSION['entro']=TRUE; 
                $respuesta["Access"]="OK";
                $_SESSION['username']=$resultado[0][usuario]; 
                //$_SESSION['idUser']=$resultado[0][idUser]; 
                $_SESSION['endpoints']=$resultado[0][dispositivos]; 
                $_SESSION['keyhash']=$resultado[0][keyhash];
                $respuesta["username"] = $resultado[0][usuario];
                if($resultado[0][keyhash] == "0"){
                    $_SESSION['areaAdmin'] = TRUE; 
                  
                }else{
                    $_SESSION['areaAdmin']=FALSE;                     
                }

            }
            else{
                $_SESSION['entro']=FALSE;
                $respuesta["Access"]="NOOK";
                
            }
        }else{
            //$respuesta["result"] = "NOOK";
            $respuesta["result"] = "ERROR CON SQL: " . $conn->ultimoError();
        }
    }
    else{
        $respuesta["result"] =  "ERROR DE CONEXIÓN AL HACER LA CONSULTA DE USUARIO";
    } 
    echo json_encode($respuesta);
?>