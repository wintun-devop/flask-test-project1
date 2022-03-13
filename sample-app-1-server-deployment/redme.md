#requried packages
pip install flask flask-sqlalchemy flask-wtf flask-api flask_restful
pip install mysql-connector pymysql cryptography
pip install Flask-Migrate


#flask form
https://flask.palletsprojects.com/en/2.0.x/patterns/wtforms/

#from python command line
from app import db
db.create_all()

#flask migrate package for project migration from flask command line
flask db init
flask db migrate -m "Migrate first time."
flask db upgrade


#flask migrate package for project migration from flask command line
flask db migrate -m "Migrate second time-add password field."
flask db upgrade


