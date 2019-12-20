#!/usr/bin/env python
""" Class containing logic for Find Package State Operation.

    @author Alfredo Sanz
    @date October 2019
"""

#APIs imports
import requests
from bs4 import BeautifulSoup
from string import Template
import time
import sqlite3

import ConfigRoot
import Consts
import Util
from dao.PackageDAO import PackageDAO



class Find_package_state():

    """
    * Constructor
    """
    def __init__(self):
        print('**Find_package_state class instantiated**')
    #construct
    


    """
    * Compare the package data obtained from the system with the previous version
    * stored in the system. Manage the necesary BD operations.
    *
    * @param _pckgsData dict with the information obtained from all the packages we are consulting.
    """
    def __storeAndPrint(self, _pckgsData):
        """ Store requested package data if we have to and print information"""

        conn = None
        try:
            thetime = Util.getCurrentTime()
            dao = PackageDAO()

            conn = sqlite3.connect('alms.db')
            c = conn.cursor()

            dao.bd_createTable(c)

            for key in _pckgsData.keys():
                pckg = _pckgsData[key]

                pckg_BD = dao.bd_selectPackageList_byID(c, pckg['id'])
                if pckg_BD :
                    if pckg_BD['status'] != pckg['status'] or pckg_BD['source_env'] != pckg['source_env'] or pckg_BD['dest_env'] != pckg['dest_env']:
                        print("PACKAGE REMOTE UPDATED***********************************************")
                        print("previous state=" + repr(pckg_BD))
                        print("     new state=" + repr(pckg))
                        print("*********************************************************************")

                        dao.bd_insertPackage(conn, c, pckg, pckg_BD['num'], thetime)
                    else:
                        print("PACKAGE HAS NO CHANGES****")
                        print("state=" + repr(pckg_BD))    
                    #if
                else:
                    print("PACKAGE FIRST****")
                    print("state=" + repr(pckg))    
                    dao.bd_insertPackage(conn, c, pckg, 0, thetime)            
                #if
            #for
        finally:
            conn.close()
        #
    #fin __storeAndPrint



    """
    * Performs the action of extracting the package data from the html page obtained. 
    *
    * @param _packageContent str with html content of package data.*
    * @return dict with the package data
    """
    def __extract_Package_Data(self, _packageContent):
        """Extraction of the package data from page content"""

        result = {}

        package_soup =  BeautifulSoup(_packageContent, 'html.parser')
        sp_table = package_soup.find('table', attrs={'id': 'package_list_edit'})
        sp_tr = sp_table.find("tr", attrs={'class':'even package_list_edit_tr'})
            
        td_id = sp_tr.find('td', attrs={'class':'td_id'})
        result['id'] = td_id.text

        td_desc = sp_tr.find('td', attrs={'class':'td_desc'})
        result['desc'] = td_desc.text    

        td_status = sp_tr.find('td', attrs={'class':'td_status'})
        result['status'] = td_status.text

        td_source_env = sp_tr.find('td', attrs={'class':'td_source_env'})
        result['source_env'] = td_source_env.text

        td_dest_env = sp_tr.find('td', attrs={'class':'td_dest_env'})
        result['dest_env'] = td_dest_env.text

        td_last_m_date = sp_tr.find('td', attrs={'class':'td_last_m_date'})
        result['app'] = td_last_m_date.text

        return result
    #fin __extract_Package_Data



    """
    * Perform the action of search the package by its id.
    *
    * @param _idPackage str Package to search
    * @param _session_requests
    * @param _sess_cookies
    * @return str  html content returned by the action search
    """
    def __find_Package_Action(self, _session_requests, _sess_cookies, _idPackage):
        """ Find the Package in ALMS"""

        #Replacement of the packageID  in the url template
        url_buscar_paquete_template = Template(Consts.url_buscar_paquete)
        url_buscar_paquete_subst = url_buscar_paquete_template.substitute(pakageID = _idPackage)
        print('findPack - URL:' + url_buscar_paquete_subst)

        #Make search action
        package_rq_result = _session_requests.get(url_buscar_paquete_subst, data = {}, headers = Consts.headers, cookies = _sess_cookies)
        print('findPack - status_code:' + repr(package_rq_result.status_code))
        print('findPack - status_reason:' + repr(package_rq_result.reason))
        #print('findPack - content:' + str(package_rq_result.content))

        return package_rq_result.content
    #__find_Package_Action



    """
    * Execute the search package state operation.
    *
    * @param session_requests Session data object
    * @param sess_cookies Cookies with JSESSIONID needed for the call.
    * @param op loop or not to loop
    *
    * @return str '0' or a message with error
    """
    def executeOP(self, session_requests, sess_cookies, op):
        """ Find Package State implementation."""
        
        doloop = True
        i = 0

        while doloop:
            print("Iteration: " + str(i))

            result = {}

            for pckgID in ConfigRoot.packages_id_searchlist:
                packageContent = self.__find_Package_Action(session_requests, sess_cookies, pckgID)
                result[pckgID] = self.__extract_Package_Data(packageContent)
            #for

            self.__storeAndPrint(result)    
            
            if 'pckg_state' == op or \
                i >= Consts.loop_iterations_max:

                doloop = False
                continue
            #

            time.sleep(Consts.loop_wait)
            i += 1
        #while

        return '0'
    #fin executeOP
#