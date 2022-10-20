import os
from flask import current_app


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


def check_if_image_exist():
    pass


