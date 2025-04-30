import os
import logging
from utils.constants import CONDUCTOR_SERVER_URL, CONDUCTOR_AUTH_KEY, CONDUCTOR_AUTH_SECRET


def initialize():
    logging.info('Initializing local development')
    os.environ[CONDUCTOR_SERVER_URL] = 'https://developer.orkescloud.com/api'
    os.environ[CONDUCTOR_AUTH_KEY] = '<your auth key>'
    os.environ[CONDUCTOR_AUTH_SECRET] = '<your auth secret>'

