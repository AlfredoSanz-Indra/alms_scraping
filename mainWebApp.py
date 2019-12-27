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
import shutil #move files
import subprocess #launchs processes
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
    result = ''
    inputs = ''

    try:
        timedata = Util.getCurrentTime()

        #***REQUESTING DATA
        params = {'pckg_id_list' : request.form.get("pckg_id_list")
                 }        

        #TODO todo esto hay que refactorizarlo***

        #***PERFORM ACTION
        idList = [x.strip() for x in params['pckg_id_list'].split(',')]
        inputs = repr(idList)
        app.logger.info('The IDs: ' + inputs)

        app.logger.info('**Updating input data**')
        with open('ConfigRoot.py') as f:
            lines = list(f)            

            with open('ConfigRoot.py.tmp', 'w') as output:
                for line in lines:
                    if line.startswith('packages_id_searchlist'):
                        output.write('packages_id_searchlist = ' + repr(idList) + '\n')
                    else:
                        output.write(line)
                #
            #
        #
        shutil.move('ConfigRoot.py.tmp', 'ConfigRoot.py')


        app.logger.info('**Launching Process**')
        process = subprocess.run(['D:/DEV/python3/python', 'main.py', '-o pckg_state'], 
                         stdout=subprocess.PIPE, 
                         universal_newlines=True,
                         bufsize=0)

        app.logger.info('process return code:' + str(process.returncode))        

        result = ''        
        for line in process.stdout.split('\n'):
            result += '<p>'
            result += line.strip()
            result += '</p>'
        #
        app.logger.info('process return stdout:' + result)

        #RESPONSE DATA
        app.logger.info('**Preparing output**')
        resultData['inputs'] = inputs
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

