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


@app.route("/")
def hello():
    return "Alfredo Tools."
#fin hello



@app.route("/vf/web/")
def helloWeb():
    return "Alfredo Web Tools"
#fin helloWeb


