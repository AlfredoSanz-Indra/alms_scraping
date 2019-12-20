#!/usr/bin/env python
""" Class containing logic for the details package request

    @author Alfredo Sanz
    @date October 2019
"""

#APIs imports
import sys
import requests
from bs4 import BeautifulSoup
from string import Template
import time
import pandas as pd
import xlsxwriter
import json

import ConfigRoot
import Consts
import Util


class Find_package_detail():

    """
    * Constructor
    """
    def __init__(self):
        print('**Find_package_detail class instantiated**')
    #construct



    """
    * Perform the action of search the module pvcs.
    *
    * @param _session_requests
    * @param _sess_cookies
    * @param _moduleName module name to search
    * @return str  html content returned by the action search
        
    """
    def __getPackageDetailContent(self, _session_requests, _sess_cookies, _packageID):
        """ Get the content for the Package Detail"""

        result = '0'

        try:
            #Replacement of the module name  in the url template
            url_template = Template(Consts.url_paquete_detalle)
            url_template_subst = url_template.substitute(pakageID = _packageID)
            print('getPackageDetailContent - URL:' + url_template_subst)

            #Make search action
            rq_result = _session_requests.get(url_template_subst, data = {}, headers = Consts.headers, cookies = _sess_cookies)
            result = rq_result.content
            print('getPackageDetailContent - status_code:' + repr(rq_result.status_code))
            print('getPackageDetailContent - status_reason:' + repr(rq_result.reason))
        except Exception as err:
            print("Error in http GET request-> ")
            print(err)
        #

        return result
    #__getPackageDetailContent



    """
    * Execute the search of the package details
    *
    * @param session_requests Session data object
    * @param sess_cookies Cookies with JSESSIONID needed for the call.
    *
    * @return str '0' or a message with error
    """
    def executeOP(self, session_requests, sess_cookies):
        """ Get the Package details."""
        
        result = '1'
        thetime = Util.getCurrentTime()

        try:
            packageID = ConfigRoot.package_id_detail
            assert packageID, 'Error, package_id_detail param is not set!'
            print('getPckgDetails - packageID: ' + packageID)
                        
            sPackageContent = self.__getPackageDetailContent(session_requests, sess_cookies, packageID)
            assert sPackageContent != '0', 'Error requesting content'
            print('sPackageContent: ' + repr(sPackageContent))

            result = '0'            
        except AssertionError as err:
            print('Assertion: ' + str(err))
            result = '-1'
        except Exception as err:
            print('Error executing Operation->')
            print(err)
            result = '-2'
        #

        return result
    #fin executeOP
#