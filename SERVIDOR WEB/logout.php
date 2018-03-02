<?php
    
    //PHP que se ejecuta al desloguearse, que la página se redirige al index.tpl
    
    if (!session_start()){
        session_start();
    }
    $_SESSION['entro']=FALSE;
    $_SESSION['areaAdmin']=FALSE;                     
    header("Location: index.php");
  
?>
