#!/usr/bin/env python
""" Class containing logic for Package Database Operations.

    @author Alfredo Sanz
    @date October 2019
"""

#APIs imports
import requests
from bs4 import BeautifulSoup
from string import Template
import sqlite3
import time

import ConfigRoot
import Consts
import Util



class PackageDAO():

    """
    * Constructor
    """
    def __init__(self):
        print('**PackageDAO class instantiated**')
    #construct


    """
    * Create the DB table if necessary.
    *
    * @param _c cursor
    """
    def bd_createTable(self, _c):
        """ Create the DB table if necessary"""

        _c.execute('CREATE TABLE IF NOT EXISTS package (id TEXT, num INT, desc TEXT, status TEXT, source_env TEXT, dest_env TEXT, app TEXT, last_rev TEXT)')
    #fin bd_createTable



    """
    * Select a package from the DB.
    *
    * @param _c cursor
    * @param _pckgID str Id del package
    * @return dict with the data selected from DB or None if the package was not stored yet.
    """
    def bd_selectPackageList_byID(self, _c, _pckgID):
        """ Select the package from DB"""

        result = {}

        _c.execute("SELECT id, num, desc, status, source_env, dest_env, app, last_rev FROM  package WHERE id=? ORDER BY num DESC", [_pckgID])    
        data = _c.fetchone()

        if data:
            result['id'] = data[0]            
            result['desc'] = data[2]
            result['status'] = data[3]
            result['source_env'] = data[4]
            result['dest_env'] = data[5]
            result['app'] = data[6]
            result['last_rev'] = data[7]
            result['num'] = data[1] #Place this attribute the last because of print issue.  I know this is a Dict, take it easy.
        #

        return result
    #fin bd_selectPackageList_byID


    """
    * Store a package in DB.
    *
    * @param _conn Connection
    * @param _c cursor
    * @param _pckg dict with packge data
    * @param num int The number of package record stored.
    * @param _thetime dict containing datetime info
    """
    def bd_insertPackage(self, _conn, _c, _pckg, num, _thetime):

        _c.execute("INSERT INTO package VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (_pckg['id'], num + 1, _pckg['desc'], _pckg['status'], _pckg['source_env'], _pckg['dest_env'], _pckg['app'], _thetime['strFechaHoraFilename']))
        _conn.commit()
    #fin bd_insertPackage
#