#!/usr/bin/env python
""" Class containing Constants vars.

    @author Alfredo Sanz
    @date October 2019
"""


#supported operations
operationsSupported = {'pckg_state': '1', 'pckg_state_loop':'1', 'module': '1', 'pvcs': '1', 'pckg_detail': '1'}

#Seconds the loop to wait
loop_wait = 180
loop_iterations_max = 40 # 40 iterations are two hours of iterations in 3 minutes by iteration.

TIME_UNIT_SEC = 'SEC'
TIME_UNIT_MIN = 'MIN'


# Urls
url_page = 'http://XXXX'
url_login = 'http://XXXX'
url_buscar_paquete = 'http://XXXX/ALMS/ControllerPackView?task=pack.view.general.select&pk=$pakageID&operacion=consultapvcs'
url_buscar_modulo  = 'http://XXXX/ALMS/ControllerPackView?task=pack.view.general.select&moduloPvs_T=$moduleName&operacion=consultagen_modulopvcs'
url_buscar_modulo_pvcs_step1 = 'http://XXXX/proxyPVCS/search?archive=$moduleName&repomd5=21156050a97219c9ef60477bc5467029'
url_buscar_modulo_pvcs_step2 = 'http://XXXX/proxyPVCS/vlog?archive=//PVCS_XXXX/archives$thepath/$thename-arc'
url_paquete_detalle = 'http://XXXX/ALMS/ControllerPackView?paquete=$pakageID&task=pack.view.select.notif1&operacion=edit'        

login_payload = {
        'lgn': 'user_login',
        'pwd': 'user_password',
        'task': 'other',
        'url': '/ControllerPackAvMg',
        'idIdioma': 'EN'
    }

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': url_login,
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}