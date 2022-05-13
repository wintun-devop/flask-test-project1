#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from flask_wtf.file import FileField,FileAllowed,FileRequired



class UploadImage(FlaskForm):
    upload_image=FileField("Upload Image:",validators=[FileRequired(),FileAllowed(["jpg","png","gif","jpeg"])])
    submit=SubmitField("Submit")