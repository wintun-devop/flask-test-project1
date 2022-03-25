#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)
from flask import Flask, render_template,request,flash,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config['SECRET_KEY']="asd123!@#"
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://dbadmin:Abc123Abc123@127.0.0.1/mylab03'
db = SQLAlchemy(app)

#student record database model
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(80), unique=True, nullable=False)
    password=db.Column(db.String(255), nullable=False)
    dob=db.Column(db.Date)
    contact=db.Column(db.String(30))
    gender=db.Column(db.String(10))
    joindate = db.Column(db.Date,default=datetime.utcnow().date())
    def __repr__(self):
        return f'<Student {self.firstname}>'



#delete record from system
@app.route("/deletestudent/<int:id>")
def studentdelete(id):
    student_to_delete=Students.query.get_or_404(id)
    try:
        db.session.delete(student_to_delete)
        db.session.commit()
        flash("Student record has been deleted successfully!")
        return redirect(url_for("students"))
    except:
        flash("Something went wrong on deleteing record.Try gain!")
            
            
#update student record from system
@app.route("/updatestudent/<int:id>",methods=["GET","POST"])
def studentupdate(id):
    student_to_update = Students.query.get_or_404(id)
    if request.method == "POST":
        student_to_update.firstname=request.form["update-fn"]
        student_to_update.lastname=request.form["update-ln"]
        student_to_update.dob=request.form["update-dob"]
        student_to_update.gender=request.form["update-gender"]
        student_to_update.contact=request.form["update-contact"]
        db.session.commit()
        flash("Student record has been updated successfully!")
        return redirect(url_for("students"))
    return render_template("update.html",update_student=student_to_update)
    
    
    
#add student record to system
@app.route("/addstudent",methods=["GET","POST"])
def addstudent():
    if request.method == 'POST':
        student_in_db = Students.query.order_by(Students.email)
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password=request.form['pass']
        dob=request.form['dob']
        contact=request.form['contact']
        gender = request.form['gender']
        password=generate_password_hash(password,"sha256")
        contact=str(contact)
        #Checking input user is already existed or not
        if email not in student_in_db:
            try:
                student_record = Students(firstname=firstname,
                          lastname=lastname,
                          email=email,password=password,dob=dob,contact=contact,gender=gender)
                db.session.add(student_record)
                db.session.commit()
                flash("Student record has been added successfully!")
                return redirect(url_for("students"))
            except:
                flash("Student reord existed in system!")
                return render_template("register.html")
    return render_template("register.html")

 
@app.route("/students",methods=["GET","POST"])
def students():
    student=Students.query.order_by(Students.joindate)
    return render_template("students.html",student=student)


@app.route("/")
def index():
    return render_template("index.html")
