import sys
import json
import babel
from flask import (
Flask, 
render_template, 
request, 
Response, 
flash, 
redirect, 
url_for)
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)