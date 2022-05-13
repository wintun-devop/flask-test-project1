#https://github.com/wintun-devop
#https://www.youtube.com/channel/UCz9ebjc-_3t3p49gGpwyAKA (Please subscribe my channel.Thank You!)

from flask import Flask,render_template
from webforms import UploadImage
from werkzeug.utils import secure_filename
import app_config,boto3
import uuid as uuid


app=Flask(__name__)
app.config["SECRET_KEY"]=app_config.applicationSecret


@app.route("/uploadimage",methods=["GET","POST"])
def imageupload():
    image_upload_form=UploadImage()
    awsS3client = boto3.client("s3",
                        aws_access_key_id=app_config.aws_access_key_id,
                        aws_secret_access_key=app_config.aws_secret_access_key,
                        region_name=app_config.aws_region
                        )
    if image_upload_form.validate_on_submit():
        #image file data
        image_file=image_upload_form.upload_image.data
        #image file name
        image_file_name=secure_filename(image_file.filename)
        #system secure file name
        image_name=str(uuid.uuid1())+"_"+image_file_name
        #image file save on s3 and destination file is file path inside of bucket
        destination_file="flask-upload/"+image_name
        awsS3client.put_object(Body=image_file,
                      Bucket=app_config.s3Bucket,
                      Key=destination_file)
        return f"image name:{image_name}."
    return render_template("upload/upload_image.html",imageuploadform=image_upload_form)


@app.route("/")
def index():
    return "hello world!"

if __name__=="__main__":
    app.run(debug=True)