from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

#Assign application secret
app.config["SECRET_KEY"]="asd123!@#"
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://dbadmin:Abc123Abc123@127.0.0.1/cosmetic01"
#Assign database instance
db= SQLAlchemy(app)
from primary_module.products.models import Brand,Category,Products
from primary_module.products import routes
from primary_module.certs import routes

db.create_all()