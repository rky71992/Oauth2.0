import os
import sys
import bottle
from bottle import route, run, request, response, error
import json
import bottle
import datetime
import time
import shutil
import logging
from config import *
from utils import *
import requests

client = get_db_connection()
db = get_db(AUTH_DB_NAME, client)

logpath = AUTH_LOG_PATH
logging.basicConfig(filename=logpath, level=logging.DEBUG)


@route('/client/regestration', method="GET")
def client_reg():
    #print "ac"
    form = json.loads(bottle.request.query.data)
    print form
    client_id = form.get("client_id")
    #print client_id
    try:
        client_user = db.clients.find_one({'client_id': client_id})
        #print client_user
        if client_user:
            print "there"
            db.clients.update({"client_id": client_id}, {"$set": {"logged_in": True, 'login_time':str(
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))}}, upsert=True)
            logging.debug("Client-logged-in--" + client_id + "--" + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            print "loggingdone"
            return "yes"

        else:
            db.clients.insert({'client_id': client_id, "logged_in": True})
            logging.info("Client-regestered--" + client_id)
            #return "yes"
    except Exception, ex:
        return str(ex)


if __name__ == "__main__":
    run(host="127.0.0.1", port = AUTH_PORT)