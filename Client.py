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
db = get_db(CLIENT_DB_NAME, client)

logpath = CLIENT_LOG_PATH
logging.basicConfig(filename = logpath, level = logging.DEBUG)


success = False
@route("/login", method='POST')
def create_session():
    print "Client"
    errors = []
    global success
    username = None
    password = None
    db_user = None
    form = None
    session_id = None
    status = {}
    try:
        form = json.load(bottle.request.body)
        username = form.get('username', '').strip().lower()
        password = form.get('password', '')

        if not username:
            errors.append('empty.username')
        if not password:
            errors.append('empty.password')
    except Exception, ex1:
        status["create_session Exception"] = str(ex1)
        errors.append('error.parse')
    if errors:
        print "create_session : error : ", errors
        bottle.abort(400, json.dumps({ 'errors' : errors}))
    try:
        db_user = db.users.find_one({'username':username,
                                     'password':password})
        print db_user
        if db_user:
            print "DB user"
            session_id = random_string(16)
            db.users.update({"_id": db_user["_id"]}, {"$set":{"session_id":session_id, "logged_in":True}},upsert = True)
            logging.debug(db_user["username"] + "Logged in")
            client_id = db.users.find_one({"client_id":"F0:1F:AF:12:DE:D7"})
            if client_id:
                payload = {"client_id":client_id["client_id"]}
                #print payload
                #url = "http://127.0.0.1:11000/client/regestration?data="+json.dumps(payload)
                #print url
                r = requests.get("http://127.0.0.1:11000/client/regestration?data="+json.dumps(payload))
                #print r
            else:
                print "not working"


            db.user_log.insert({'username':db_user['username'],
                                'event_datetime':str(
                                datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
                               'description': 'Logged in: IP: %s' % request.remote_addr, 'action':'Log-in'})

        else:
            raise Exception ('Not a valid user')

    except Exception, ex:
        return str(ex)
        bottle.abort(500, json.dumps({ 'errors' : [str(ex)]}))


if __name__ == '__main__':
    run(host='127.0.0.1', port= CLIENT_PORT)