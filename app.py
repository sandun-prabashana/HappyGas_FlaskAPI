from flask import Flask

application = Flask(__name__)
application.config['SECRET_KEY'] = 'your secret key'