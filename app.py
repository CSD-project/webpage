from flask import Flask, render_template, request
import boto3
from dotenv import dotenv_values

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# to keep the access keys a secret stored it in .env file and .env in .gitignore
secrets = dotenv_values(".env")

# for the page to upload the image
@app.route('/')
def home_page():
    return render_template("index.html")


# to route the image after uploading
@app.route('/uploaded', methods=["POST"])
def uploader():
    # declaring the S3 bucket secret keys
    s3 = boto3.client('s3', aws_access_key_id=secrets["AWS_ACCESS_KEY_ID"], aws_secret_access_key=secrets["AWS_SECRET_ACCESS_KEY"])
    f = request.files['filename']

    # only if the image uploaded is a .png, .jpeg, .jpg file only then will it upload the image
    if f.content_type in ['image/png', 'image/jpeg', 'image/jpg']:
        s3.upload_fileobj(f, 'shreyas01', f.filename)
        return render_template("uploaded.html")

    # if file is not chosen or other file format in entered then take them to error page to upload again option
    else:
        return render_template("Tryagain.html")
    

# for the gallery page to show all the images of the product
@app.route('/gallery')
def gallery():
    # Retrieve a list of image keys from your S3 bucket
    s3 = boto3.client('s3', aws_access_key_id=secrets["AWS_ACCESS_KEY_ID"], aws_secret_access_key=secrets["AWS_SECRET_ACCESS_KEY"])
    bucket_name = 'shreyas002'

    # to list all the object in the bucket
    objects = s3.list_objects(Bucket=bucket_name)
    contents = []  # to store all the keys
    for i in objects['Contents']:  # to retrieve all the keys in S3 bucket
        contents.append(i['Key'])

    # Render the gallery template with the list of image keys
    return render_template('gallery.html', contents=contents)


if __name__ == "__main__":
    app.run(debug=True)
