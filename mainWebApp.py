#!/usr/bin/env python
""" Main for web project

    @author Alfredo Sanz
    @date Dec 2019
"""
from flask import Flask, render_template, request, jsonify, Response
from flask_restful import Api
from flask_restful import reqparse
from flask_cors import CORS, cross_origin
import urllib
import logging
import json
import Util

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(filename='/logs/pyalms.log', level=logging.DEBUG)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


#*******************************************************
#API RESTFULL WITH FLASK-RESTFUL LIB
#*******************************************************
api = Api(app)

#Example
#api.add_resource(apiController, '/vf/api/v1/data')


#*******************************************************
#RESTFUL API AVALAIBLE
#*******************************************************
api_routes = [
    {
        'route': u'/vf/api/v1/alive',
        'methods': u'GET'
    }
]



@app.route('/vf/api/v1/explore-api', methods=['GET'])
def get_api():
    return jsonify({'api-routes': api_routes})


#*******************************************************
##WEB REQUEST WITH FLASK
#*******************************************************

@app.route("/")
def hello():
    app.logger.info("---default INIT")
    return "Alfredo Tools."
#fin hello



@app.route("/vf/web/")
def helloWeb():
        
    app.logger.info("---helloWeb INIT")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        app.logger.debug(request.url_root)

        #Call to Controller
        try:
            #controller = Mainpage_Controller()
            #errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "10-10-2019"
            
        except Exception as err:
            app.logger.error(str(err))            
            app.logger.exception("@Error")
        #

        tem_values = {'errormessage':  errormessage,
                      'domain': request.url_root[:-1],#quita la barra final
                      'fecha': resultData['fecha']
                     }

    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Error Redireting index: ' + str(err)
    #
    
    #logging.info('tem_values=' + repr(tem_values))
    app.logger.info("---helloWeb ENDS")
    return render_template('index.html', datas = tem_values)
#fin helloWeb



"""
* HTTP - Launch the package state script.
"""
@app.route("/vf/ajx/scriptstate" , methods=['POST'])
def ajx_script_pckgState_get():
        
    app.logger.info("---ajx_script_pckgState_get INIT")

    errormessage = '0'
    resultData = {}

    try:
        timedata = Util.getCurrentTime()

        #***REQUESTING DATA
        params = {'pckg_id_list' : request.form.get("pckg_id_list")
                 }        

        #***PERFORM ACTION
        idList = [x.strip() for x in params['pckg_id_list'].split(',')]
        app.logger.info('The package list requested: ' + repr(idList))


        result = ''
        for i in idList:
            result += i
        #

        #RESPONSE DATA
        resultData['results'] = result
        resultData['successMessage'] = u'OK'
        resultData['errormessage'] = u'0'
        
    except Exception as err:
        app.logger.error(str(err))
        app.logger.exception("@Error")
        errormessage = '*Launching Script PackageState: ' + str(err)
        resultData['errormessage'] = errormessage
        resultData['successMessage'] = u'-1'
    #
    
    app.logger.info("---ajx_script_pckgState_get ENDS")
    return jsonify({'serverdata': resultData})
#fin ajx_script_pckgState_get

