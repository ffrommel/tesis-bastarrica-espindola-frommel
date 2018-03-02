<!DOCTYPE html>

<html>
<!--INDEX.tpl-->
    <head>
        <meta charset="UTF-8"> 
        <title>Riego Inteligente</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no"><!--OJO de maps-->
        <script type="text/javascript" src="/Tesis/JavaScript/jquery.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/users.js"></script>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/cabezal.js"></script>
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/login.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/estilos.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3-theme-blue-grey.css">  
        <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Open+Sans'>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    {*Incluyo el cabezal del sitio*}
    {include file = "cabezal.tpl"} 
    <h1>Usuarios</h1>
    <body> 
        <div  style="text-align: center">
            <label id="labelListOfUsers"></label>
        </div>
        
        <div id="listOfUsers" class='divFadeIn'></div>
    </body>
</html> 

