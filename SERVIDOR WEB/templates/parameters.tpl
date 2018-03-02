<!DOCTYPE html>

<html>
<!--INDEX.tpl-->
    <head>
        <meta charset="UTF-8"> 
        <title>Riego Inteligente</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no"><!--OJO de maps-->
        <script type="text/javascript" src="/Tesis/JavaScript/jquery.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/cabezal.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/showParameters.js"></script>
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/login.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/estilos.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3-theme-blue-grey.css">  
        <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Open+Sans'>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    {*Incluyo el cabezal del sitio*}
    {include file = "cabezal.tpl"}
    <body>
        <h1>Parámetros configurables</h1>
        <div class="genericText">
            <label>Período de muestreo actual : </label>
            <label id="actualSamplePeriod"></label>
            <label> minutos</label>
            </br></br>  
            <div>
                <label>Período de muestreo a configurar en minutos : </label>
                <input placeholder="nuevo período" id="inputNewSamplePeriod" min="10" max="60" type="number" style="width:120px"/>
                <button type="submit" class="w3-btn-floating w3-light-grey fa fa-upload w3-border w3-margin-right w3-margin-top" id="btnNewSamplePeriod"></button></br>
            </div>
        </div>
    </body>
</html> 
 
 