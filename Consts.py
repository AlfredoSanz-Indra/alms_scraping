#!/usr/bin/env python
""" Class containing Constants vars.

    @author Alfredo Sanz
    @date October 2019
"""

import ConstsAux


#supported operations
operationsSupported = ConstsAux.operationsSupported

#Seconds the loop to wait
loop_wait = ConstsAux.loop_wait
loop_iterations_max = ConstsAux.loop_iterations_max # 40 iterations is two hours of iterations in 3 minutes by iteration.

TIME_UNIT_SEC = 'SEC'
TIME_UNIT_MIN = 'MIN'


# Urls
url_page = ConstsAux.url_page
url_login = ConstsAux.url_login
url_buscar_paquete = ConstsAux.url_buscar_paquete
url_buscar_modulo  = ConstsAux.url_buscar_modulo
url_buscar_modulo_pvcs_step1 = ConstsAux.url_buscar_modulo_pvcs_step1
url_buscar_modulo_pvcs_step2 = ConstsAux.url_buscar_modulo_pvcs_step2
url_paquete_detalle = ConstsAux.url_paquete_detalle

login_payload = ConstsAux.login_payload
    
headers = ConstsAux.headers