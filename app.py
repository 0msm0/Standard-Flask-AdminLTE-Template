from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

app.secret_key = "nhjhnjjhvhbjngyvygvjxrxrd" # For encrept & decrept session data on a server
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

#Flask-SQLAlchemy will track modifications of objects and emit signals. The default is None , which enables tracking but issues a warning that it will be disabled by default in the future. This requires extra memory and should be disabled if not needed
