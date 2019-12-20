#!/usr/bin/env python
""" Class containing logic for Find module packages list

    @author Alfredo Sanz
    @date October 2019
"""

#APIs imports
import requests
from bs4 import BeautifulSoup
from string import Template
import time
import pandas as pd
import xlsxwriter

import ConfigRoot
import Consts
import Util
from dao.PackageDAO import PackageDAO



class Find_module_packages():

    """
    * Constructor
    """
    def __init__(self):
        print('**Find_module_packages class instantiated**')
    #construct


    def __writeToExcel(self, _pckgsData, _pckgsListSort, _moduleName, _thetime):

        listData = []

        for id in _pckgsListSort:
            data = _pckgsData[str(id)]
            advanced = data['paramsOMOver']

            theData = {}
            theData['package'] = data['id']
            theData['moduleName'] = data['moduleName']
            theData['tipo_aplicacion'] = advanced['tipo_aplicacion']
            theData['app'] = data['id']
            theData['idrelease'] = advanced['idrelease']
            theData['codproyecto'] = advanced['codproyecto']
            theData['desc'] = data['desc']
            theData['status'] = data['status']
            theData['dest_env'] = data['dest_env']
            theData['empresa'] = advanced['empresa']
            theData['fechaultimamodificacion'] = advanced['fechaultimamodificacion']

            listData.append(theData)
        #for

        print('Writing to Excel result File')
     
        df = pd.DataFrame.from_dict(listData)  # Finally, create the DataFrame from the dictionary   
        #df = pd.DataFrame({'Packages': listData})        
        
        fileName = 'result-files/module-' + _moduleName + '-' + _thetime['strFechaHoraFilenameST'] + '.xlsx'
        writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
        
        df.to_excel(writer, sheet_name='PckgsList')
       
        writer.save()
    #fin __writeToExcel



    """    
    *
    * @param _pckgsData dict with the information obtained from all the packages we are consulting.
    """
    def __print(self, _pckgsData, _pckgsListSort):
        """ Print the data requested"""

        x = 0
        for id in _pckgsListSort:
            data = _pckgsData[str(id)]
            advanced = data['paramsOMOver']

            print('**')
            print('pckg: ' + data['id'])
            print('     moduleName: ' + data['moduleName'])
            print('     tipo_aplicacion: ' + advanced['tipo_aplicacion'])
            print('     app: ' + data['app'])
            print('     idrelease: ' + advanced['idrelease'])
            print('     codproyecto: ' + advanced['codproyecto'])
            print('     desc: ' + data['desc'])
            print('     status: ' + data['status'])
            print('     dest_env: ' + data['dest_env'])            
            print('     empresa: ' + advanced['empresa'])
            print('     fechaultimamodificacion: ' + advanced['fechaultimamodificacion'])
            print(' ')

            x += 1
        #for

        print('-->' + str(x) + ' packages found')                
    #fin __print



    def __splitOnmouseoverParams(self, _txt):
        """ Extraction of values from the onmouseover event declaration inside the tr tag"""

        result = {}

        dataList = _txt.split(',')
        result['tipo_aplicacion'] = dataList[1]
        result['aplicacion'] = dataList[2]
        result['idrelease'] = dataList[3]
        result['codproyecto'] = dataList[4]
        result['empresa'] = dataList[19]
        result['fechaultimamodificacion'] = dataList[20]

        return result
    #fin __splitOnmouseoverParams



    """
    * Performs the action of extracting the package list and data from the html page obtained. 
    *
    * @param _packageContent str with html content of package data.*
    * @param _moduleName The Module searched
    * @return dict with the packages, [pckgID, dict{}]
    """
    def __extract_module_data(self, _moduleContent, _moduleName):
        """Extraction of the module content data from page content"""

        result = {}

        package_soup =  BeautifulSoup(_moduleContent, 'html.parser')
        sp_table = package_soup.find('table', attrs={'id': 'package_list_edit'})
        trList = sp_table.findAll("tr", attrs={'class':'even package_list_edit_tr'})

        for theTR in trList:            
            
            record = {}

            tagOMOver = theTR.attrs['onmouseover']                 
            if tagOMOver:
                record['paramsOMOver'] =  self.__splitOnmouseoverParams(tagOMOver)
            #

            td_id = theTR.find('td', attrs={'class':'td_id'})
            record['id'] = td_id.text

            td_desc = theTR.find('td', attrs={'class':'td_desc'})
            record['desc'] = td_desc.text    

            td_status = theTR.find('td', attrs={'class':'td_status'})
            record['status'] = td_status.text

            td_source_env = theTR.find('td', attrs={'class':'td_source_env'})
            record['source_env'] = td_source_env.text

            td_dest_env = theTR.find('td', attrs={'class':'td_dest_env'})
            record['dest_env'] = td_dest_env.text

            td_last_m_date = theTR.find('td', attrs={'class':'td_last_m_date'})
            record['app'] = td_last_m_date.text

            record['moduleName'] = _moduleName

            result[td_id.text] = record
        #for
        
        return result
    #fin __extract_module_data



    """
    * Perform the action of search the module package list.
    *    
    * @param _session_requests
    * @param _sess_cookies
    * @param _moduleName str name of the module to search
    * @return str  html content returned by the action search
    """
    def __find_module_action(self, _session_requests, _sess_cookies, _moduleName):
        """ Find the Module in ALMS"""

        #Replacement of the module name  in the url template
        url_template = Template(Consts.url_buscar_modulo)
        url_template_subst = url_template.substitute(moduleName = _moduleName)
        print('findModule - URL:' + url_template_subst)

        #Make search action
        rq_result = _session_requests.get(url_template_subst, data = {}, headers = Consts.headers, cookies = _sess_cookies)
        print('findModule - status_code:' + repr(rq_result.status_code))
        print('findModule - status_reason:' + repr(rq_result.reason))
        #print('findModule - content:' + str(rq_result.content))

        return rq_result.content
    #__find_module_action


    
    """
    * Execute the search of packages where the module is referenced.
    *
    * @param session_requests Session data object
    * @param sess_cookies Cookies with JSESSIONID needed for the call.
    *
    * @return str '0' or a message with error
    """
    def executeOP(self, session_requests, sess_cookies):
        """ Find the packages where the Module is included."""
        
        thetime = Util.getCurrentTime()

        moduleName = ConfigRoot.module_name_search
        print('findModule - module name: ' + moduleName)

        if moduleName:
            moduleContent = self.__find_module_action(session_requests, sess_cookies, moduleName)
            pckgsData = self.__extract_module_data(moduleContent, moduleName)
        
            pckgsList = []

            for key in pckgsData.keys():
                pckgsList.append(int(key))
            #for

            pckgsListSort = sorted(pckgsList, reverse=True)
            print('pckgsList:' + repr(pckgsList))

            self.__print(pckgsData, pckgsListSort)
            self.__writeToExcel(pckgsData, pckgsListSort, moduleName, thetime)
        #if
            
        return '0'
    #fin executeOP
#