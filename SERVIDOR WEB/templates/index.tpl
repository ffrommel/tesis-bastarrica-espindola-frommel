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
        <h1>Bienvenido</h1>
        <h1 id="welcome"></h1>
        {if ($areaPrivada == TRUE && $areaAdmin == FALSE)}
        <div style="padding-top:100px">
            <table style="width:100%">
                <tr> 
                    <th>
                        <p>
                            <a href="/Tesis/execMap.php" id="tabMap" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Mapa">
                            <img src="images/ubicar.png" class="imgIndex grow"></a>
                        </p>  
                    </th>
                    <th>
                        <p>
                            <a href="/Tesis/execGraphs.php" id="tabMap" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Gráficas">
                            <img src="images/graficar.png" class="imgIndex grow"></a>                            
                        </p> 
                    </th>
                    <th>
                        <p>
                            <a href="/Tesis/execForecast.php" id="tabForecast" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Pronóstico">                            
                            <img src="images/predecir.png" class="imgIndex grow"></a>
                        </p>  
                    </th>
                    <th>
                        <p> 
                            <a href="/Tesis/execParameters.php" id="tabParameters" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Parámetros">
                            <img src="images/sensar.png" class="imgIndex grow"></a>
                        </p>
                        
                    </th> 
                </tr>
                <tr> 
                    <th>Ubicar</th>
                    <th>Graficar</th> 
                    <th>Predecir</th>
                    <th>Configurar</th>
                </tr>
                
                
              </table>
        </div>
        {/if}

    </body>
</html> 

