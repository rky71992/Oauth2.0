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
db = get_db(RESOURCE_DB_NAME, client)

logpath = RESOURCE_LOG_PATH
logging.basicConfig(filename = logpath, level = logging.DEBUG)
