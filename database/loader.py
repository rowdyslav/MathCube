import bson
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import current_app, g
from flask_pymongo import PyMongo
from pymongo.errors import DuplicateKeyError, OperationFailure
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db
    return db


db = LocalProxy(get_db)
