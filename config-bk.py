# -*- coding: utf-8 -*-
from os import path

# App details
BASE_DIRECTORY = path.abspath(path.dirname(__file__))
DEBUG = True
SECRET_KEY = 'keep_it_like_a_secret'

# Database details
SQLALCHEMY_DATABASE_URI = '{0}{1}'.format('sqlite:///', path.join(BASE_DIRECTORY, 'app.db'))

# Facebook app details
FB_APP_ID = ''
FB_APP_NAME = ''
FB_APP_SECRET = ''

# Twitter credentials
CONSUMER_KEY 		= 	''
CONSUMER_SECRET 	=	''
ACCESS_TOKEN 		= 	''
TOKEN_SECRET 		= 	''

