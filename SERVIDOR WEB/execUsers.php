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
        $miSmarty->display("users.tpl");
    }else{
        
    if ($_SESSION['areaAdmin']){
        $areaAdmin = TRUE;
        $miSmarty->assign("areaAdmin",$areaAdmin);
    }else{
        $miSmarty->assign("mensaje",$_SESSION['msg']);
        $miSmarty->display("index.tpl");    
        
    }
  }

?>

