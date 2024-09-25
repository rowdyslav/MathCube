import dns.resolver
from flask import current_app, g
from flask_pymongo import PyMongo
from icecream import ic
from werkzeug.local import LocalProxy


def get_db():
    db = getattr(g, "_database", None)
    ic(db)
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
    if db is None:
        dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
        dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
        db = g._database = PyMongo(current_app).cx["MathCube"]
        ic(current_app)
        ic(db)
        ic(g._database)
    return db


db = LocalProxy(get_db)
