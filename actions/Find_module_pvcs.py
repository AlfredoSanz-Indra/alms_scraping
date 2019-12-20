#!/usr/bin/env python
""" Class containing logic for the pvcs module info

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
from dao.PackageDAO import PackageDAO


class Find_module_pvcs():

    """
    * Constructor
    """
    def __init__(self):
        print('**Find_module_pvcs class instantiated**')
    #construct



    def __writeToExcel(self, _moduleFullInfo, _thetime):

        result = '0'

        try:
            print('Generating Dataframe for excel writer!')

            #print('step1')
            dtMain = {}
            dtMain['archive'] = _moduleFullInfo['archive']
            dtMain['workfile'] = _moduleFullInfo['workfile']
            dtMain['revcount'] = _moduleFullInfo['revcount']
            dtMain['owner'] = _moduleFullInfo['owner']
            dtMain['archive'] = _moduleFullInfo['archive']
            dtMain['islocked'] = str(_moduleFullInfo['islocked'])
            dtMain['lockedby'] = _moduleFullInfo['lockedby']
            dtMain['iscreated'] = _moduleFullInfo['iscreated']
            dtMain['description'] = _moduleFullInfo['description']

            #print('step2')            
            dtVersionLabels = []
            for lb in _moduleFullInfo['versionlabels']:
                theData = {}                        
                theData['group'] = lb['group']
                theData['package'] = lb['package']
                theData['rev'] = lb['rev']                
                theData['nrev'] = lb['nrev']
                theData['date'] = lb['date']
                theData['label'] = lb['label']

                dtVersionLabels.append(theData)
            #for

            #print('step3')            
            jsGroups = _moduleFullInfo['groups']
            
            if 'DEV' in jsGroups:
                dtMain['DEV'] = jsGroups['DEV']

            if 'SIT1' in jsGroups:
                dtMain['SIT1'] = jsGroups['SIT1']

            if 'PPRD' in jsGroups:
                dtMain['PPRD'] = jsGroups['PPRD']

            if 'SIT2' in jsGroups:
                dtMain['SIT2'] = jsGroups['SIT2']

            if 'PROD' in jsGroups:
                dtMain['PROD'] = jsGroups['PROD']
            if 'SONAR' in jsGroups:
                dtMain['SONAR'] = jsGroups['SONAR']

            if 'SONAR1' in jsGroups:
                dtMain['SONAR1'] = jsGroups['SONAR1']

            if 'SONAR2' in jsGroups:
                dtMain['SONAR2'] = jsGroups['SONAR2']

            if 'TST' in jsGroups:
                dtMain['TST'] = jsGroups['TST']

            if 'TST1' in jsGroups:
                dtMain['TST1'] = jsGroups['TST1']

            if 'HIDSIT1' in jsGroups:
                dtMain['HIDSIT1'] = jsGroups['HIDSIT1']

            if 'HIDPPRD' in jsGroups:
                dtMain['HIDPPRD'] = jsGroups['HIDPPRD']
            #
            #print('step4')
            dtRevisions = []
            for rv in _moduleFullInfo['revisions']:
                theData = {}
                theData['numrev'] = str(rv['numrev'])        
                theData['rev'] = rv['rev']
                theData['authorId'] = rv['authorId']                
                theData['lastModified'] = rv['lastModified']
                theData['checkedIn'] = rv['checkedIn']
                theData['linesDelAddMove'] = rv['linesDelAddMove']
                theData['lockedBy'] = rv['lockedBy']
                theData['comment'] = rv['comment']

                dtRevisions.append(theData)
            #for
        
            print('Creating Excel File')    
            
            df1 = pd.DataFrame.from_dict(dtMain, orient='index')  # Finally, create the DataFrame from the dictionary   
            df2 = pd.DataFrame.from_dict(dtVersionLabels)  # Finally, create the DataFrame from the dictionary   
            df3 = pd.DataFrame.from_dict(dtRevisions)  # Finally, create the DataFrame from the dictionary   
            
            fileName = 'result-files/pvcs-' + _moduleFullInfo['workfile'] + '-' + _thetime['strFechaHoraFilenameST'] + '.xlsx'
            writer = pd.ExcelWriter(fileName, engine='xlsxwriter')
            
            df1.to_excel(writer, sheet_name='Main')
            df2.to_excel(writer, sheet_name='Labels')
            df3.to_excel(writer, sheet_name='Revisions')

            writer.save()
            print('Excel file successfully generated and saved to Disk-->' + fileName)
        except Exception as err:
            print(repr(err))
            result = '-1'
        #

        return result
    #fin __writeToExcel



    """
    *
    * @param _moduleFullInfo dict with the information of the module in PVCS.
    """
    def __print(self, _moduleFullInfo):
        """ Print the data requested"""

        print('*****')                    
        print('     archive  : ' + _moduleFullInfo['archive'])
        print('     workfile : ' + _moduleFullInfo['workfile'])
        print('     owner    : ' + _moduleFullInfo['owner'])
        print('     revcount : ' + _moduleFullInfo['revcount'])
        print('     islocked : ' + str(_moduleFullInfo['islocked']))        
        print('     lockedby : ' + _moduleFullInfo['lockedby'])            
        print('*****')
    #fin __print



    """
    * Performs the action of extracting the full content of the module
    * responsed in json format from pvcs.

    * @param _moduleFullContent str with html content of package data.*
    * @return dict with the module info, {path, type, name}
    """
    def __extract_module_pvcs_step2(self, _moduleFullContent):
        """Extraction of the pvcs reponse with json module info"""

        result = {}

        try:
            jsonData = json.loads(_moduleFullContent.decode('latin1'))

            result['revisions'] = jsonData[0]['revisions']
            result['lasttrunkrev'] = jsonData[0]['lasttrunkrev']
            result['groups'] = jsonData[0]['groups']
            result['owner'] = jsonData[0]['owner']
            result['versionlabels'] = jsonData[0]['versionlabels']
            result['lockedby'] = jsonData[0]['lockedby']
            result['islocked'] = jsonData[0]['islocked']
            result['revcount'] = jsonData[0]['revcount']
            result['description'] = jsonData[0]['description']
            result['iscreated'] = jsonData[0]['iscreated']
            result['archive'] = jsonData[0]['archive']
            result['workfile'] = jsonData[0]['workfile']
        except Exception as err:
            print("Error extracting json full info-> ")
            print(repr(err))
        #
                          
        return result
    #fin __extract_module_pvcs_step2



    """
    * Perform the action of search the module pvcs.
    *
    * @param _session_requests
    * @param _sess_cookies
    * @param _moduleInfo dict with module info, path and name
    * @return binary with the module full info form pvcs in json format
    """
    def __find_module_step2_action(self, _session_requests, _sess_cookies, _moduleInfo):
        """ Get the complete module info in pvcs"""

        result = '0'

        try:
            #Replacement of the module path and name in the url template
            url_template = Template(Consts.url_buscar_modulo_pvcs_step2)
            url_template_subst = url_template.substitute(thepath = _moduleInfo['path'], thename = _moduleInfo['name'])
            print('findModule2 - URL:' + url_template_subst)

            #Make search action
            rq_result = _session_requests.get(url_template_subst, data = {}, headers = Consts.headers, cookies = _sess_cookies)
            result = rq_result.content
            print('findModule2 - status_code:' + repr(rq_result.status_code))
            print('findModule2 - status_reason:' + repr(rq_result.reason))
        except Exception as err:
            print("Error in http GET request, step 2-> ")
            print(repr(err))
        #

        return result
    #__find_module_step2_action



    """
    * Performs the action of extracting the params from json response.
    *
    * @param _moduleContent binary with json module content.
    * @return dict with the module info, {path, type, name}
    """
    def __extract_module_pvcs_step1(self, _moduleContent):
        """Extraction of the json module info"""

        result = {}
        
        jsonData = json.loads(_moduleContent.decode('latin1'))

        result['path'] = jsonData[0]['path']
        result['type'] = jsonData[0]['type']
        result['name'] = jsonData[0]['name']
                  
        return result
    #fin __extract_module_pvcs_step1



    """
    * Perform the action of search the module pvcs.
    *
    * @param _session_requests
    * @param _sess_cookies
    * @param _moduleName module name to search
    * @return str  html content returned by the action search
        
    """
    def __find_module_step1_action(self, _session_requests, _sess_cookies, _moduleName):
        """ Find the Module and get the complete module route in pvcs repo"""

        result = '0'

        try:
            #Replacement of the module name  in the url template
            url_template = Template(Consts.url_buscar_modulo_pvcs_step1)
            url_template_subst = url_template.substitute(moduleName = _moduleName)
            print('findModule - URL:' + url_template_subst)

            #Make search action
            rq_result = _session_requests.get(url_template_subst, data = {}, headers = Consts.headers, cookies = _sess_cookies)
            result = rq_result.content
            print('findModule - status_code:' + repr(rq_result.status_code))
            print('findModule - status_reason:' + repr(rq_result.reason))
        except Exception as err:
            print("Error in http GET request, step 1-> ")
            print(err)
        #

        return result
    #__find_module_step1_action



    """
    * Execute the search of the module info in pvcs
    *
    * @param session_requests Session data object
    * @param sess_cookies Cookies with JSESSIONID needed for the call.
    *
    * @return str '0' or a message with error
    """
    def executeOP(self, session_requests, sess_cookies):
        """ Find the module pvcs info."""
        
        result = '1'
        thetime = Util.getCurrentTime()

        try:
            moduleName = ConfigRoot.module_pvcs_search
            assert moduleName, 'Error, moduleName param is not set!'
            print('findModule - module name: ' + moduleName)
                        
            sModuleContent = self.__find_module_step1_action(session_requests, sess_cookies, moduleName)
            assert sModuleContent != '0', 'Error searching content step 1'
            #print('moduleContent: ' + repr(sModuleContent))

            dictModuleInfo = self.__extract_module_pvcs_step1(sModuleContent)
            assert dictModuleInfo, 'Error, moduleInfo has no content'
            print('module complete path: ' + dictModuleInfo['path'] + '/' + dictModuleInfo['name'])

            bModuleFullInfo = self.__find_module_step2_action(session_requests, sess_cookies, dictModuleInfo)
            assert bModuleFullInfo != '0', 'Error searching full content for pvcs module'
            #print('moduleFullInfo:' + repr(bModuleFullInfo))

            dictModuleFullData = self.__extract_module_pvcs_step2(bModuleFullInfo)
            assert dictModuleFullData, 'Error moduleFullData has no content'            

            self.__print(dictModuleFullData)
            w = self.__writeToExcel(dictModuleFullData, thetime)
            assert w == '0', 'Error writting Excel'

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