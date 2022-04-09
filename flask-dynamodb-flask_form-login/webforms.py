#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,EqualTo

class Login(FlaskForm):
    login_email=StringField("Email:",validators=[DataRequired()])
    login_password=PasswordField("Password:",validators=[DataRequired()])
    submit=SubmitField("Login")
    
class SignUp(FlaskForm):
    signup_name=StringField("Name:",validators=[DataRequired()])
    signup_email=StringField("Email:",validators=[DataRequired()])
    signup_password=PasswordField("Password:",validators=[DataRequired(),EqualTo("confirm_password",message="Password must be same!")])
    confirm_password=PasswordField("Confirm Password:",validators=[DataRequired()])
    submit=SubmitField("SignUp")