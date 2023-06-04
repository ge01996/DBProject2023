## This file is ran automatically the first time a Python program imports the package dbdemo
from flask import Flask
from flask_mysqldb import MySQL
from schooldb.users import users
from schooldb.book import book
from schooldb.school import school
'''from schooldb.writer import writer
from schooldb.category import category
from schooldb.keyword import keyword
from schooldb.rental import rental
from schooldb.reservation import reservation
from schooldb.rating import rating'''

## __name__ is the name of the module. When running directly from python, it will be 'dbdemo'
## Outside of this module, as in run.py, it is '__main__' by default
## Create an instance of the Flask class to be used for request routing
app = Flask(__name__)

## configuration of database

app.config["MYSQL_USER"] = 'root'
app.config["MYSQL_PASSWORD"] = 'zaq1xsw2'
app.config["MYSQL_DB"] = 'schooldb'
app.config["MYSQL_HOST"] = 'localhost'
app.config["SECRET_KEY"] = 'key' ## secret key for sessions (signed cookies). Flask uses it to protect the contents of the user session against tampering.
app.config["WTF_CSRF_SECRET_KEY"] = 'key' ## token for csrf protection of forms.
## secret keys can be generated by secrets.token_hex()

## initialize database connection object
db = MySQL(app)

## routes must be imported after the app object has been initialized
from schooldb import routes
from schooldb.users import routes
from schooldb.book import routes
from schooldb.school import routes
'''from schooldb.writer import routes
from schooldb.category import routes
from schooldb.keyword import routes
from schooldb.rental import routes
from schooldb.reservation import routes
from schooldb.rating import routes'''
app.register_blueprint(users)
app.register_blueprint(book)
app.register_blueprint(school)
'''app.register_blueprint(writer)
app.register_blueprint(category)
app.register_blueprint(keyword)
app.register_blueprint(rental)
app.register_blueprint(reservation)
app.register_blueprint(rating)
'''

