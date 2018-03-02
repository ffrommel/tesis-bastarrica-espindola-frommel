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
  
    $ch = curl_init();

    $url="http://".AWSIp.":8080/kaaAdmin/rest/api/configurationRecord?schemaId=".SCHEMAID."&endpointGroupId=".ENDPOINTGROUPID."";
    
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "GET");
 
    curl_setopt($ch, CURLOPT_USERPWD, "devuser" . ":" . "devuser123");

    $headers = array();
    $headers[] = "Accept: application/json";
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $result["samplePeriod"] = curl_exec($ch);
    $result["url"] = $url;

    if (curl_errno($ch)) {
        echo 'Error:' . curl_error($ch);
    }



    curl_close ($ch); 

    echo json_encode($result);


 