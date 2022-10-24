import os
import logging
from io import BytesIO
from flask import current_app, send_from_directory
from werkzeug.utils import secure_filename
from botocore.exceptions import ClientError
from PIL import Image

from spaces import client


def get_or_create(database: object, model: object, **kwargs: object) -> object:
    instance = model.query.filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        create_instance = model(**kwargs)
        database.session.add(create_instance)
        return create_instance


def destination_open(photo):
    return '/'.join([current_app.config["UPLOADED_PHOTOS_DEST"], photo])


def destination_save(photo):
    return '/'.join([current_app.config["UPLOADED_THUMBNAIL_DEST"], photo])


def add_to_digitalocean(file):
    filename = secure_filename(file.filename)
    image = Image.open(BytesIO(file.read()))
    image.thumbnail((2400, 1600))
    image_file = BytesIO()
    image.save(image_file, format=image.format)
    image_file.seek(0)
    client.put_object(Body=image_file,
                      Bucket=current_app.config["SPACE_NAME"],
                      Key=filename,
                      ContentType=file.content_type)


def show_image(filename):
    bucket = current_app.config["SPACE_NAME"]
    try:
        presigned_url = client.generate_presigned_url('get_object', Params={'Bucket': bucket,
                                                                            'Key': filename}, ExpiresIn=3600)
    except ClientError as e:
        logging.error(e)
        return None

    return presigned_url
