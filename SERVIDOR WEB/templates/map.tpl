<!DOCTYPE html>

<html>
<!--INDEX.tpl-->
    <head>
        <meta charset="UTF-8"> 
        <title>Riego Inteligente</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no"><!--OJO de maps-->
        <script type="text/javascript" src="/Tesis/JavaScript/jquery.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/googleMaps.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/maps.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/cabezal.js"></script>
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/login.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/estilos.css">
        <link rel="stylesheet" type="text/css" href="/Tesis/css/w3-theme-blue-grey.css">  
        <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Open+Sans'>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <script async defer src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBvFtO9j111A5TXcM7m7E9mcXsr0XMq2O8&callback=callMap"></script>
    </head>
    {*Incluyo el cabezal del sitio*}
    {include file = "cabezal.tpl"}
    <h1>Ubicación de las estaciones</h1>
    <body>   
        <div style="text-align: center" >
            <h4 id="labelMap"></h4>
        </div>
        <br><br>
        <div id="mapFilter" class='divFadeIn'>
            <div class="" style="" >
                <div>
                    <label>Parámetro a filtrar  </label>
                    <select id="mapParameter" class="">
                        <option Selected disabled>Seleccionar</option>
                        <option value="0">Humedad del Suelo</option>
                        <option value="1">Temperatura del Suelo</option>
                        <option value="2">Humedad del ambiente</option>
                        <option value="3">Temperatura del ambiente</option>
                        <option value="4">Detección de Lluvia</option>
                        <option value="6">RSSI</option>
                    </select>
                </div>    
                <br>
                <div>
                    <label>Menor a  </label>
                    <input id="mapHumMin"/>
                    <label>  de color </label>
                    <select id="colorMin" class="">
                        <option value="#00FF00">Verde</option>
                        <option selected value="#FF0000">Rojo</option>
                    </select>
                </div>
                <br>
                <div>
                    <label>Mayor a  </label>
                    <input id="mapHumMax"/>
                    <label>  de color  </label> 
                    <select id="colorMax" class="">
                        <option selected value="#00FF00">Verde</option>
                        <option value="#FF0000">Rojo</option>
                    </select>   
                </div>
            </div><br>
            <div class="" style="">
                <button type="submit" class="w3-btn w3-light-grey fa fa-search w3-border" id="btnChangeColorFilter"> Buscar</button><br><br>
            </div>
        </div>
        <br><br>
        <div id="map" class="divFadeIn"></div>
    </body>
</html> 

