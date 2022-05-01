#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

from flask import Flask,render_template
from webforms import UploadImage
from werkzeug.utils import secure_filename
import app_config,os
import uuid as uuid


app=Flask(__name__)
app.config["SECRET_KEY"]=app_config.applicationSecret
app.config["UPLOAD_FOLDER"]=app_config.uploadFolder


@app.route("/uploadimage",methods=["GET","POST"])
def imageupload():
    image_upload_form=UploadImage()
    if image_upload_form.validate_on_submit():
        #image file data
        image_file=image_upload_form.upload_image.data
        #image file name
        image_file_name=secure_filename(image_file.filename)
        #system secure file name
        image_name=str(uuid.uuid1())+"_"+image_file_name
        image_file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config["UPLOAD_FOLDER"],image_name))
        return f"image name:{image_name}."
    return render_template("upload/upload_image.html",imageuploadform=image_upload_form)


@app.route("/")
def index():
    return "hello world!"

if __name__=="__main__":
    app.run(debug=True)
