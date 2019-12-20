Necesario Python 3 para ejecutar.

Primero instalar las librerias ejecutando mypip.bat 
Puede que haya que actualizar primero la versión de pip. En el mismo fichero está el comando necesario.

El fichero ConfigRoot.py hay que editarlo antes de ejecutar, porque ahí
es donde hay que indicar los datos de entrada.


El Script implementa distintas operaciones, que se indican por parametro
en la llamada al script desde la consola.

Se han creado distintos staters .bat, uno por cada operación soportada, así
que para ejecutar hay que abrir una consola cmd y ejecutar uno de estos::

run_module.bat
run_pckstate.bat
run_pckstate_loop.bat
run_pvcs.bat

*run module:
	-El objetivo de esta operación es buscar la lista de packages donde se ha
	 incluido este fichero/modulo.
	
	-En este caso hay que setear la variable 'module_name_search' en ConfigRoot.py
	
*run_pckstate:
	-Esta Operación obtiene info básica de estado de un Paquete de alms.
	
	-Hay que setear la variable 'packages_id_searchlist' en ConfigRoot.py
	 Esta variable espera una lista, ya que la operación admite consultar una lista
	 de paquetes.

*run_pckstate_loop:
	-Igual que la anterior, obtiene info básica de estado de un paquete de alms,
	  pero en este caso lo va a realizar en bucle cada varios minutos, hasta
	  que paremos el programa.
	  
	  -Hay que setear la misma variable 'packages_id_searchlist' en ConfigRoot.py,
	   indicando una lista de valores.
	 
*run_pvcs:
	-Operación que obtiene toda la información de un modulo/fichero en pvcs.
	 Nos va a recuperar la información de versiones, revisiones y etc.
	 
	 -Hay que setear la variable 'module_pvcs_search' en ConfigRoot.py,
	  indicando el nombre del fichero/modulo que buscamos.
	  
	
	







