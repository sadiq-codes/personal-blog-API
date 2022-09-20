

def get_or_create(database: object, model: object, **kwargs: object) -> object:
    instance = model.query.filter_by(**kwargs).first()
    print("instanmce :", instance)
    if instance:
        return instance
    else:
        create_instance = model(**kwargs)
        database.session.add(create_instance)
        return create_instance


