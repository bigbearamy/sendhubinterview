# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpResponseServerError
from django.http import HttpResponseRedirect
from django.conf import settings
from django.utils import simplejson
from jsonschema import validate
from django.core import serializers
from django.shortcuts import render_to_response
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth import authenticate, login, logout
from contextlib import closing
import urllib
import urllib2
import tempfile
import shutil
from urlparse import urlparse
import datetime, random, sha
from django.core.mail import send_mail
from django.template import RequestContext
from md5 import md5
from string import whitespace
import time
from django.utils import timezone
import subprocess
import os
import ftplib
from os import listdir
import traceback
import sys

routingTable = {
    "smallCategory" : {"subnet":"10.0.1.0/24", "throughput":1, "cost":0.01},
    "mediumCategory" : {"subnet":"10.0.2.0/24", "throughput":5, "cost":0.05},
    "largeCategory" : {"subnet":"10.0.3.0/24", "throughput":10, "cost":0.10},
    "superCategory" : {"subnet":"10.0.4.0/24", "throughput":25, "cost":0.25},
}
schema = {
        "title": "SendHub Challenge Schema",
        "type": "object",
        "properties": {
            "message": {"type": "string"},
            "recipients": {"type": "array","minItems": 1,"items": {"type": "string"},"uniqueItems": True}
        },
        "required": ["message", "recipients"]
        }

@require_http_methods(["GET", "POST"])
def index(request):
    return render_to_response('home.html', {})


@csrf_exempt
@require_http_methods(["GET", "POST"])
def submitjob_user(request):
    errormsg = ''
    json = ''
    json_dict = None
    try:
        if request.method == "POST":
            print (str(request.body))
            mydata = simplejson.loads(str(request.body))
            validate(mydata, schema)
            #print out all possible routes
            json_dict = findAllPossibleRoutes(mydata, routingTable)
    except:
        errormsg = 'error' + str(sys.exc_info())
        print str(sys.exc_info())
        json_dict = {"error":errormsg}
        raise
    json = simplejson.dumps(json_dict)
    print json
    return HttpResponse(json, mimetype='application/json')

def findAllPossibleRoutes(mydata, routingTable):
    totalLen = len(mydata['recipients'])
    phoneList = mydata['recipients']
    routes = []
    route = None
    while (totalLen > 0):
        print totalLen
        if  (totalLen >= routingTable['superCategory']['throughput']):
            totalLen = totalLen - routingTable['superCategory']['throughput']
            route = {"ip":routingTable['superCategory']['subnet'], "recipients":phoneList[0: routingTable['superCategory']['throughput']]}
            del phoneList[0:routingTable['superCategory']['throughput']]
        elif (totalLen >= routingTable['largeCategory']['throughput']):
            totalLen = totalLen - routingTable['largeCategory']['throughput']
            route = {"ip":routingTable['largeCategory']['subnet'], "recipients":phoneList[0: routingTable['largeCategory']['throughput']]}
            del phoneList[0:routingTable['largeCategory']['throughput']]
        elif (totalLen >= routingTable['mediumCategory']['throughput']):
            totalLen = totalLen - routingTable['mediumCategory']['throughput']
            route = {"ip":routingTable['mediumCategory']['subnet'], "recipients":phoneList[0: routingTable['mediumCategory']['throughput']]}
            del phoneList[0:routingTable['mediumCategory']['throughput']]
        elif (totalLen >= routingTable['smallCategory']['throughput']):
            totalLen = totalLen - routingTable['smallCategory']['throughput']
            route = {"ip":routingTable['smallCategory']['subnet'], "recipients":phoneList[0: routingTable['smallCategory']['throughput']]}
            del phoneList[0:routingTable['smallCategory']['throughput']]
        routes.append(route)
    return_json = {
                    "message":"SendHubRocks",
                    "routes":routes,
                  }
    return return_json