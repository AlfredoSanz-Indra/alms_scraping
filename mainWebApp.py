#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, Response
from flask_restful import Api
from flask_restful import reqparse
from flask_cors import CORS, cross_origin
import urllib
import logging
import json

app = Flask(__name__)
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
    return "Alfredo Tools."
#fin hello



@app.route("/vf/web/")
def helloWeb():
        
    logging.info("Entering hello index")

    errormessage = '0'
    tem_values = {}
    resultData = {}

    try:
        logging.debug(request.url_root)

        #Call to Controller
        try:
            #controller = Mainpage_Controller()
            #errormessage, resultData = controller.datosBasicosPortada(request, u'PORTADA')

            resultData['fecha'] = "10-10-2019"
            
        except Exception as err:
            logging.error(str(err))            
            logging.exception("@Error")
        #

        tem_values = {'errormessage':  errormessage,
                      'domain': request.url_root[:-1],#quita la barra final
                      'fecha': resultData['fecha']
                     }

    except Exception as err:
        logging.error(str(err))
        logging.exception("@Error")
        errormessage = '*Error Redireting index: ' + str(err)
    #
    
    #logging.info('tem_values=' + repr(tem_values))
    logging.info("redirecting hello web index")
    return render_template('index.html', datas = tem_values)
#fin helloWeb


