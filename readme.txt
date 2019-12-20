Necesario Python 3 para ejecutar.

Primero instalar las librerias ejecutando mypip.bat 
Puede que haya que actualizar primero la versi�n de pip. En el mismo fichero est� el comando necesario.

El fichero ConfigRoot.py hay que editarlo antes de ejecutar, porque ah�
es donde hay que indicar los datos de entrada.


El Script implementa distintas operaciones, que se indican por parametro
en la llamada al script desde la consola.

Se han creado distintos staters .bat, uno por cada operaci�n soportada, as�
que para ejecutar hay que abrir una consola cmd y ejecutar uno de estos::

run_module.bat
run_pckstate.bat
run_pckstate_loop.bat
run_pvcs.bat

*run module:
	-El objetivo de esta operaci�n es buscar la lista de packages donde se ha
	 incluido este fichero/modulo.
	
	-En este caso hay que setear la variable 'module_name_search' en ConfigRoot.py
	
*run_pckstate:
	-Esta Operaci�n obtiene info b�sica de estado de un Paquete de alms.
	
	-Hay que setear la variable 'packages_id_searchlist' en ConfigRoot.py
	 Esta variable espera una lista, ya que la operaci�n admite consultar una lista
	 de paquetes.

*run_pckstate_loop:
	-Igual que la anterior, obtiene info b�sica de estado de un paquete de alms,
	  pero en este caso lo va a realizar en bucle cada varios minutos, hasta
	  que paremos el programa.
	  
	  -Hay que setear la misma variable 'packages_id_searchlist' en ConfigRoot.py,
	   indicando una lista de valores.
	 
*run_pvcs:
	-Operaci�n que obtiene toda la informaci�n de un modulo/fichero en pvcs.
	 Nos va a recuperar la informaci�n de versiones, revisiones y etc.
	 
	 -Hay que setear la variable 'module_pvcs_search' en ConfigRoot.py,
	  indicando el nombre del fichero/modulo que buscamos.
	  
	
	







