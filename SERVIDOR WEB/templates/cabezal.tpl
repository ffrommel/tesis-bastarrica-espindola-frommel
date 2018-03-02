<!--CABEZAL.tpl-->

    <!-- Opciones de la barra de navegacion, se usa la variable $areaPrivada para desplegar opciones del area privada ademas de la publica -->
    <div class="w3-top">
        <div id="cabezal" class="w3-container w3-theme-d2">
            <ul id="menuBar" class="w3-navbar w3-left-align w3-large ">
                <li class="w3-hide-medium w3-hide-large w3-opennav w3-right">
                    <a class="w3-padding-large w3-hover-white w3-large w3-theme-d2  w3-mobile" href="javascript:void(0);" onclick="openNav()"><i class="fa fa-bars"></i></a>
                </li>

                <li class="w3-hide-small w3-left"><a href="/Tesis/index.php" id="index" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Inicio"><i class="fa fa-home"></i> Inicio</a></li>
                <!--{if ($areaPrivada == TRUE && $areaAdmin == FALSE)}
                    <li class="w3-hide-small w3-left"><a href="/Tesis/execGraphs.php" id="tabMap" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Gráficas"><i class="fa fa-bar-chart"></i> Gráficas</a></li>
                    <li class="w3-hide-small w3-left"><a href="/Tesis/execMap.php" id="tabMap" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Mapa"><i class="fa fa-map-marker"></i> Mapa</a></li>
                    <li class="w3-hide-small w3-left"><a href="/Tesis/execParameters.php" id="tabParameters" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Parámetros"><i class="fa fa-cloud-upload"></i> Parámetros</a></li>
                    <li class="w3-hide-small w3-left"><a href="/Tesis/execForecast.php" id="tabForecast" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Pronóstico"><i class="fa fa-sun-o"></i> Pronóstico</a></li>

                {/if}-->
                {if ($areaPrivada == TRUE || $areaAdmin == TRUE)}
                    <li class="w3-hide-small w3-right"><a href="/Tesis/logout.php" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Logout"><i class="fa fa-sign-out"></i> Logout</a></li>
                {else}
                    <li class="w3-hide-small w3-right"><a href="#" id="login" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Login"><i class="fa fa-sign-in"></i> Login</a></li>
                {/if}
                {if ($areaAdmin == TRUE)}
                    <li class="w3-hide-small w3-left"><a href="#" id="newClient" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="newClient"><i class="fa fa-user-plus"></i> Nuevo Cliente</a></li>
                    <li class="w3-hide-small w3-left"><a href="#" id="newEndpoint" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="newEndpoint"><i class="fa fa-rss"></i> Nuevo Dispositivo</a></li>
                    <li class="w3-hide-small w3-left"><a href="/Tesis/execUsers.php" id="showUsersData" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="showUsersData"><i class="fa fa-users"></i> Usuarios</a></li>
                {/if}
                <li class="w3-hide-small w3-left"><a href="#" id="infoModal" class="w3-padding-large w3-hover-white w3-bar-item w3-mobile" title="Info"><i class="fa fa-info-circle"></i> Info</a></li>
            </ul>
        </div>
    </div>           

    <div id="pastoFinal" class="w3-bottom">
        <img src="images/pasto4.png">
    </div> 
                
                
        <!-- Modal de login -->
    <div id="id01" class="modal">
        <form id="loginForm" class="modal-content animate modalBack">
            <div class="imgcontainer">
                <img src="images/avatar2.png" alt="Avatar" class="avatar">
            </div>
            <div class="container">
                <label><b>Usuario</b><br></label>
                <input class="inputInicio" type="text" id="txtUsu" placeholder="Ingrese nombre de usuario" name="txtUsu" value="" required>
                <label><b>Clave</b><br></label>
                <input class="inputInicio" type="password" id="txtPass" placeholder="Ingrese clave" name="txtPass" value="" required><br>
                <p class="messageError" id="usuarioIncorrecto">    </p>
                <button type="button" autofocus id="botonLogin" class="w3-btn-block w3-green" >Login</button>
            </div>
            <div class="container">
                <button type="button" id="cancelarLogin" class="w3-btn-block w3-red">Cancelar</button>
            </div>
        </form>
    </div>

    <!-- Modal de New Client -->
    <div id="modalNewClient" class="modal">
        <form id="loginNewClient" class="modal-content animate modalBack">
            <div class="imgcontainer">
                <img src="images/avatar2.png" alt="Avatar" class="avatar">
            </div>
            <div class="container">
                <div class="w3-col l1" style="width:45%; margin-right:10%">
                    <label><b>Usuario</b><br></label>
                    <input class="inputInicio" type="text" id="txtUsuNewClient"  placeholder="Ingrese nombre de usuario" name="txtUsuNewClient" value="" required>
                </div>       
                <div class="w3-col l1" style="width:45%">
                    <label><b>Clave</b><br></label>
                    <input class="inputInicio" type="password" id="txtPassNewClient" placeholder="Ingrese clave" name="txtPassNewClient" value="" required><br>
                </div>    
                <label><b>KeyHash</b><br></label>
                <input class="inputInicio" type="text" id="txtKeyNewClient" placeholder="Ingrese KeyHash" name="txtKeyNewClient" value="" required><br>
                <p class="messageError" id="userExist">    </p>
                <button type="button" id="botonNewClient" class="w3-btn-block w3-green">Crear usuario</button>
            </div>
            <div class="container">
                <button type="button" id="cancelarNewClient" class="w3-btn-block w3-red">Cancelar</button>
            </div>
        </form>
    </div>
    
   
        <!-- Modal de New Endpoint -->
    <div id="modalNewEndpoint" class="modal">
        <form id="formNewEndpoint" class="modal-content animate modalBack">
            <div class="imgcontainer">
                <img src="images/imgEndpoint.png" alt="Avatar" class="avatar">
            </div>
            <div class="container"> 
                <div class="w3-col l1" style="width:48%; margin-right:4%">
                    <div>
                        <label><b>Usuario</b><br></label>
                        <select id="usersNewEndpoint" name="usersNE" class="inputInicio"></select>
                    </div>
                    <div>
                        <label><b>Latitud</b><br></label>
                        <input class="inputInicio" type="double" id="latitudNewEndpoint" placeholder="Ingrese latitud" name="endpointLatitud" value="" required><br>
                    </div>
                    <div>
                        <label><b>MAC</b><br></label>
                        <input class="inputInicio" type="text" id="macNewEndpoint" placeholder="Ingrese MAC" name="endpointMac" value="" required><br>
                    </div>
                </div>
                
                <div class="w3-col l1" style="width:48%">
                    <div>
                        <label><b>Número (GW=0)</b><br></label>
                        <input class="inputInicio" type="number" id="nroNewEndpoint"  placeholder="Numero de Dispositivo" name="nroEndpoint" value="" required>
                    </div>
                    <div>
                        <label><b>Longitud</b><br></label>
                        <input class="inputInicio" type="double" id="longitudNewEndpoint" placeholder="Ingrese longitud" name="endpointLongitud" value="" required><br>
                    </div>
                    <div>
                        <label><b>Activo</b></label>
                        <input type="checkbox" id="activeNewEndpoint"><br>
                    </div><br>
                </div><br>
                
                <p class="messageError" id="endpointIncorrect">    </p>

                <button type="button" id="botonNewEndpoint" class="w3-btn-block w3-green">Crear Endpoint</button>

            </div>


               
            <div class="container">
                <button type="button" id="cancelarNewEndpoint" class="w3-btn-block w3-red">Cancelar</button>
            </div>
        </form>
    </div> 
        
        
    <div id="info" class="modal">
        <div id="loginForm" class="modal-content animate modalBack">
            <div class="imgcontainer">
                <img src="images/logoORT.gif" alt="ORT" class="">
            </div>
            <div class="container" style="text-align: center">
                <p>Página Web hecha para el proyecto de fin de carrera de Ingeniería en Electrónica y Telecomunicaciones.<br>Grupo compuesto por: </p>
                <div>
                    <p><b>Felipe Bastarrica</b><br></p>
                    <p><b>Emiliano Espíndola</b><br></p>
                    <p><b>Fabián Frommel</b><br></p>
                </div>
            </div>
            <div class="container">
                <button type="button" id="cancelarInfo" class="w3-btn-block w3-red">Cerrar</button>
            </div>
        </div> 
    </div>
   
<!--FIN CABEZAL.tpl-->
