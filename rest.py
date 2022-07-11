
from fileinput import close
from colorama import Cursor
import pymysql
from sqlalchemy import true
from app import app
from db import mysql
from flask import request, jsonify
from flask import Flask
import jwt
import random
from flask import flash, request
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask_cors import CORS, cross_origin

application = Flask(__name__)
cors = CORS(application, resources={r"/api/v1/adminRoute/*": {"origins": "*"}})
app = application
@app.route("/test")
def hello():
	return 'Welcome to happygas'

if __name__ == "__main__":
    app.run(debug=true)
