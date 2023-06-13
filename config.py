import os
import platform

SECRET_KEY = os.urandom(32)

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True
HOST = '127.0.0.1'
PORT = 3000

if platform.system() == 'Windows':
    BASE_PATH = 'C:\\'
    PATH_SEPARATOR = '\\'

elif platform.system() == 'Linux':
    BASE_PATH = '/'
    PATH_SEPARATOR = '/'

else:
    BASE_PATH = ''

DB_DIR = f'static/images/db'
LOG_PATH = f'static/log.txt'

if not os.path.exists(DB_DIR):
    os.mkdir(DB_DIR)

if not os.path.exists(LOG_PATH):
    with open(LOG_PATH, 'w') as f:
        f.close()