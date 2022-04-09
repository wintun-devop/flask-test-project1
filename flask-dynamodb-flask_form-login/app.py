#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

from flask import Flask, redirect,render_template,redirect,url_for,flash
from webforms import Login,SignUp
import aws_config as awsdata
import boto3,application_data,datetime
from boto3.dynamodb.conditions import Key

#intital application instance(1)
app=Flask(__name__)
app.config['SECRET_KEY']=application_data.applicationSecret


#declare aws dynamodb resource(000000003)
awsResource=boto3.resource("dynamodb",region_name=awsdata.aws_region,aws_access_key_id=awsdata.aws_access_key,
                   aws_secret_access_key=awsdata.aws_secret_key
                    )

#login in process
@app.route("/login", methods=["GET","POST"])
def login():
    login_form=Login()
    if login_form.validate_on_submit():
        email=login_form.login_email.data
        password=login_form.login_password.data
        login_form.login_email.data=""
        login_form.login_password.data=""
        user_table=awsResource.Table("userdata")
        #query user by email address
        response = user_table.query(
                KeyConditionExpression=Key('userEmail').eq(email)
        )
        #check whether username and password are correct or not
        try:
            user = response['Items']
            name = user[0]['userName']
            print(user[0]['password'])
            if password == user[0]['password']:
                flash("login successfully!")
                return render_template("userdashboard.html",name=name)
            else:
                flash("Wrong password.Try Again!")
                return render_template("index.html",loginform=login_form)
        #check whether username and password are exited or not
        except:
               flash("There is no user in System!")
               return render_template("index.html",loginform=login_form)
    return render_template("index.html",loginform=login_form)


#add data to dynamodb table(000000004)
@app.route("/signup",methods=["POST","GET"])
def signup():
    signup_form=SignUp()
    if signup_form.validate_on_submit():
        user_table=awsResource.Table("userdata")
        try:
            name=signup_form.signup_name.data
            email=signup_form.signup_email.data
            password=signup_form.signup_password.data
            signup_form.signup_name.data=""
            signup_form.signup_email.data=""
            signup_form.signup_password.data=""
            current_datetime=datetime.datetime.utcnow()
            current_datetime=current_datetime.strftime("%m-%d-%Y %H:%M:%S")
            user_table.put_item(
                Item={
                    "userEmail":email,
                    "userName":name,
                    "password":password,
                    "registerTime":current_datetime
                }
            )
            flash("User add successfully!Please go ahead login!")
            return redirect(url_for("index"))
        except:
            flash("Password must be same!")
            return render_template("signup.html",signupform=signup_form)
    return render_template("signup.html",signupform=signup_form)

#define initial decorator index page for user login(000000004)
@app.route("/", methods=["GET"])
def index():
    return redirect(url_for("login"))

#running application instance(2)
if __name__ == "__main__":
    app.run(Debug=True)