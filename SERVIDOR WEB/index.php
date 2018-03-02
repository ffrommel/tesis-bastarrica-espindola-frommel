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
        $miSmarty->assign("mensaje",$_SESSION['msg']);
        $_SESSION['msg'] = "Inicio correcto";        
    }else{
        $miSmarty->assign("mensaje",$_SESSION['msg']);
        $_SESSION['msg'] = "Error de inicio";
    }
    $_SESSION['areaAdmin']==FALSE;
    if($_SESSION['areaAdmin']){
        $areaAdmin = TRUE;
    }else{
        $areaAdmin = FALSE;
    } 
    $miSmarty->assign("areaAdmin",$areaAdmin);
    $miSmarty->display("index.tpl");



?>

