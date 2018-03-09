import pymongo
import random
import string
import os
from config import *
import socket
import requests
import datetime
import json
#from mwlogger import get_logger
import subprocess
#from constants import *


def random_string(length):
    return "".join([random.choice(string.ascii_letters +
                                  string.digits) for i in range(length)])

def get_db_connection():
    info = None
    status = {}
    while info == None:
        try:
            client = pymongo.MongoClient(MONGO_DB_IP, MONGO_DB_PORT, fsync=True)
            info = client.admin.command('ismaster')
            return client
        except Exception, e:
            status["Error"] = str(e)
            return status


def get_db(db_name, client):
    return client[db_name]