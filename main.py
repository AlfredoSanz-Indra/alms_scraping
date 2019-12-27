#!/usr/bin/env python3
""" Aplicacion que analiza la web alms -> http://XXXX/ALMS/

    @author Alfredo Sanz
    @date Octubre 2019
    @v0.3 Implements a Loop for Find Package; -o pckg_state_loop; Loop Current setup: 3mins; 
"""

#APIs imports
import sys, os
import requests
from bs4 import BeautifulSoup
from string import Template
import click
import time

import ConfigRoot
import Consts
from actions.Find_package_state import Find_package_state
from actions.Find_module_packages import Find_module_packages
from actions.Find_module_pvcs import Find_module_pvcs
from actions.Find_package_detail import Find_package_detail



"""
* Perform the login into the application.
*
* @param _session_requests
* @param _sess_cookies
"""
def login_Action(_session_requests, _sess_cookies):
    """ Do the Login into web app"""

    try:
        login_rq_result = _session_requests.post(Consts.url_login, data = Consts.login_payload, headers = Consts.headers, cookies = _sess_cookies)
        print('login - status_code:' + repr(login_rq_result.status_code))
        print('login - status_reason:' + repr(login_rq_result.reason))
    except Exception as err:
        print('Error Login into webapp:' + (str(err)))
        raise Exception('*Error in Login: ' + str(err))
    #
#fin login_Action    



"""
* Load the welcome page, initializing the session 
* and obtaining the cookies.
* 
* @param _session_requests
* @return dict cookies
"""
def init_Session_Action(_session_requests):
    """Create the session accessing Welcome page"""

    try:
        init_rq_result = _session_requests.post(Consts.url_page, data = {}, headers = {})
        print('initSess - status_code:' + repr(init_rq_result.status_code))
        print('initSess - status_reason:' + repr(init_rq_result.reason))

        #cookies for JSESSIONID
        sess_cookies = _session_requests.cookies.get_dict()
        print('initSess - Cookies:' + repr(sess_cookies))
    except Exception as err:
        print('Error initializing Session:' + (str(err)))
        raise Exception('*Error initializing Session: ' + str(err))
    #

    return sess_cookies
#fin init_Session_Action



"""
* Main method
"""
@click.command()
@click.option('-o', '--operation', help='Current supported Operations: pckg_state, pckg_state_loop, module, pvcs, pckg_detail')
def runApp(operation):
    """ Main method"""

    click.echo('Running App')

    operation = operation.strip()
    click.echo("The Operation is:" + operation)

    opResult = '1'
    
    try:
        if operation not in Consts.operationsSupported:
            click.echo("Operation Not Supported!.")
        else:
            session_request = requests.session()
            session_cookies = init_Session_Action(session_request)
            login_Action(session_request, session_cookies)

            
            if 'pckg_state' == operation or 'pckg_state_loop' == operation:

                op = Find_package_state()
                opResult = op.executeOP(session_request, session_cookies, operation)
            elif 'module' == operation:
                
                op = Find_module_packages()
                opResult = op.executeOP(session_request, session_cookies)
            elif 'pvcs' == operation:

                op = Find_module_pvcs()
                opResult = op.executeOP(session_request, session_cookies)
            elif 'pckg_detail' == operation:
                
                op = Find_package_detail()
                opResult = op.executeOP(session_request, session_cookies)
            else:
                click.echo("Operation Not Supported!..2.")
            #
        #if
    except Exception as err:
        print('Error Executing Script:' + (str(err)))
        opResult = '-5'
    #

    click.echo("Finished with code: " + opResult)
#fin runApp



if __name__ == '__main__':
    runApp()
#