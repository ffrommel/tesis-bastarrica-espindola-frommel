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

    
    $newSamplePeriod=$_POST['newSamplePeriod'];
    
    $response;
    $ch = curl_init();
    

    //$url="http://".AWSIp.":8080/kaaAdmin/rest/api/configuration";
    $url="http://".AWSIp.":8080/kaaAdmin/rest/api/configuration";

    $postFields="{\"applicationId\":\"".APPLICATIONID."\",\"endpointGroupId\":\"".ENDPOINTGROUPID."\",\"schemaId\":\"".SCHEMAID."\",\"body\":\"{\\\"samplePeriod\\\":".$newSamplePeriod.",\\\"__uuid\\\":{\\\"org.kaaproject.configuration.uuidT\\\":\\\"".RECORDID."\\\"}}\"}";
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $postFields);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_USERPWD, "devuser" . ":" . "devuser123");

    $headers = array();
    $headers[] = "Content-Type: application/json";
    $headers[] = "Accept: application/json";
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result["id"] = curl_exec($ch);
    $result["ch"]=curl_getinfo($ch);
    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
        $result["result"]="NOTOK";
    }else{
        $result["result"]="OK";
    }

    curl_close($ch);
    
    echo json_encode($result);
