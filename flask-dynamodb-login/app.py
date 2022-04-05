#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)
from flask import Flask,render_template,request
import aws_config as awsdata
import boto3,datetime
from boto3.dynamodb.conditions import Key, Attr


#declare an application instance(000000001)
app = Flask(__name__)

#declare aws dynamodb resource(000000003)
awsResource=boto3.resource("dynamodb",region_name=awsdata.aws_region,aws_access_key_id=awsdata.aws_access_key,
                   aws_secret_access_key=awsdata.aws_secret_key
                    )


#define decorator for login(000000007)
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        password=request.form["password"]
        user_table=awsResource.Table("userdata")
        response = user_table.query(
                KeyConditionExpression=Key('userEmail').eq(email)
        )
        items = response['Items']
        name = items[0]['userName']
        print(items[0]['password'])
        if password == items[0]['password']:
            return render_template("userdashboard.html",name=name)
    return render_template("index.html")

#define decorator for user dashboard(000000006)
@app.route("/userdashboard",methods=["GET"])
def dashboard():
    return render_template("userdashboard.html")


#define decorator for user register(000000005)
@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["e-mail"]
        password=request.form["password"]
        current_datetime=datetime.datetime.utcnow()
        current_datetime=current_datetime.strftime("%m-%d-%Y %H:%M:%S")
        user_table=awsResource.Table("userdata")
        user_table.put_item(
            Item={
                "userEmail":email,
                "userName":name,
                "password":password,
                "registerTime":current_datetime
            }
        )
        msg = "Registration Complete. Please Login to your account !"
        return render_template("index.html",message=msg)
    return render_template("signup.html")


#define initial decorator index page for user login(000000004)
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


#declare to run appliction instance(000000002)
if __name__ == '__main__':
    app.run(debug=True)