import os
import requests
import sendgrid
from sendgrid.helpers.mail import *
import logging
from io import BytesIO
from flask import current_app
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from PIL import Image

from s3bucket import s3


def get_or_create(database: object, model: object, **kwargs: object) -> object:
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        create_instance = model(**kwargs)
        database.session.add(create_instance)
        return create_instance


def destination_open_or_save(photo):
    return '/'.join([current_app.config["UPLOADED_PHOTOS_DEST"], photo])


def upload_file_to_s3(file):
    filename = secure_filename(file.filename)
    image = Image.open(BytesIO(file.read()))
    image.thumbnail((2400, 1600))
    image_file = BytesIO()
    image.save(image_file, format=image.format)
    image_file.seek(0)

    try:
        s3.put_object(Body=image_file,
                      Bucket=current_app.config["S3_BUCKET_NAME"],
                      Key=filename,
                      ContentType=file.content_type)

    except Exception as e:
        print("something went wrong: ", e)
        return e

    return "{}{}".format(current_app.config["S3_LOCATION"], filename)


def show_image(filename):
    bucket = current_app.config["S3_BUCKET_NAME"]
    try:
        presigned_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket,
                                                                        'Key': filename}, ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return None

    return presigned_url


def get_unsplash_photo():
    headers = {"Authorization": f"Client-ID {current_app.config['UNSPLASH_API_KEY']}"}
    try:
        response = requests.get(current_app.config['UNSPLASH_API_URL'], headers=headers)
        unsplash_data = response.json()
    except Exception:
        return None
    image_url = unsplash_data['urls']['small']
    return image_url


def create_comment(sender, receiver, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = To(receiver)
    subject = f"Sending with SendGrid is Fun {subject}"
    content = Content("text/plain", f"and easy to do anywhere, even with Python {content}")
    mail = Mail(from_email, to_email, subject, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response