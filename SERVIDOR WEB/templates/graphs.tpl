<!DOCTYPE html>

<html>
<!--INDEX.tpl-->
    <head>
        <meta charset="UTF-8"> 
        <title>Riego Inteligente</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="viewport" content="initial-scale=1.0, user-scalable=no"><!--OJO de maps-->
        <script type="text/javascript" src="/Tesis/JavaScript/jquery.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/charts.js"></script>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript" src="/Tesis/JavaScript/googleChart.js"></script>
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
    <h1>Gráficas</h1>
    <body> 
        <div id="searchByMonth" style="text-align: center">
            <div>
                <label>Desde :</label>
                <input placeholder="Desde : YYYY-MM-DD" id="inputBackTimeFrom" type="date" name="inputBackTimeFrom" value="{$backDateFrom}" class=""/>
                <input id="inputTimeBackTimeFrom" type="time" name="time_in" value="{$backTimeFrom}">
            </div>
            <br>
            <div>
                <label>Hasta : </label>
                <input placeholder="Hasta : YYYY-MM-DD" id="inputBackTimeTo" type="date" name="inputBackTimeTo" value="{$backDateTo}" class=""/>
                <input id="inputTimeBackTimeTo" type="time" name="time_in" value="{$backTimeTo}">
            </div>
            <br>
            <div><button type="submit" class="w3-btn w3-light-grey fa fa-search w3-border " id="btnSearchByMonth"> Buscar </button></div></br></br>
            <h4 id="labelGraph"></h4>

        </div>
        <div style="text-align: center">    
            <label id="loadingLabelGraphs" class="loadingLabels"></label>
        </div>
        <div id="stationsResult" class="stationsResultClass">
        </div>     
    </body>
</html> 

