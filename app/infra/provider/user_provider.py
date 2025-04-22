# app/infra/providers/customer_provider.py
from app import db
from app.infra.entities.user_entity import user_entity

def get_all():
    return user_entity.query.all()

def get_by_id(user_id):
    return user_entity.query.filter_by(id=user_id).first()

def get_by_username_password(username : str):
    return user_entity.query.filter_by(username=username).first()


def create(data: dict):
    user = user_entity(**data)
    db.session.add(user)
    db.session.commit()
    return user

def update(user_id, data: dict):
    user = get_by_id(user_id)
    if not user:
        return None
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return user

def delete(user_id):
    user = get_by_id(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True
