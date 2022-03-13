#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)
#Orginal Refrence Link(https://geekscoders.com/courses/flask-crud/lessons/flask-crud-application-introduction/)
from flask import Flask,render_template,url_for,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY']="asd123!@#"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://dbadmin:Abc123Abc123@127.0.0.1/datarecord02'
db= SQLAlchemy(app)

class Customers(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(100))
    phone=db.Column(db.String(100))
    def __init__(self,name,email,phone):
        self.name = name
        self.email = email
        self.phone = phone

@app.route('/delete/<id>',methods=['GET','POST'])
def deletecustomer(id):
    customer_to_delete=Customers.query.get(id)
    db.session.delete(customer_to_delete)
    db.session.commit()
    flash("Customer record has been deleted successfully!")
    return redirect(url_for('index'))
      
@app.route('/updateuser',methods=['GET','POST'])
def updateuser():
    if request.method == 'POST':
        customer_to_update=Customers.query.get(request.form.get('id'))
        customer_to_update.name=request.form['editnm']
        customer_to_update.email=request.form['editemail']
        customer_to_update.phone=request.form['editphone']
        db.session.commit()
        flash("Customer record has been updated successfully!")
        return redirect(url_for('index'))
        
@app.route('/adduser',methods=['GET','POST'])
def adduser():
    if request.method == 'POST':
        name=request.form['nm']
        email=request.form['e-mail']
        phone=request.form['phone']
        customer_data=Customers(name,email,phone)
        db.session.add(customer_data)
        db.session.commit()
        flash("Customer added successfully!")
    return redirect(url_for('index'))

@app.route('/',methods=['GET'])
def index():
    customer_data_output=Customers.query.all()
    return render_template("index.html",customer_output=customer_data_output)

if __name__ == '__main__':
    app.run(debug=True)