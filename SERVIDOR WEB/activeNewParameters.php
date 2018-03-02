<?php

    if (!session_start()){
        session_start();
    }
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

    $id=$_POST['id'];

    $ch = curl_init();
    
    $url="http://".AWSIp.":8080/kaaAdmin/rest/api/activateConfiguration";
    $postFields=$id;

    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_USERPWD, "devuser" . ":" . "devuser123");

    $headers = array();
    $headers[] = "Content-Type: application/json";
    $headers[] = "Accept: application/json";
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result["response"] = curl_exec($ch);
    
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        $result["result"]="NOTOK";
    }else{
        $result["result"]="OK";
    }
    $result["url"] = $url;
    $result["id"] = $id;
    curl_close ($ch);
    echo json_encode($result);
